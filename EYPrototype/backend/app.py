from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from agents.master_agent import MasterAgent
from services.database import DatabaseService
from config import Config
import uuid
import asyncio
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
CORS(app, origins=Config.SOCKETIO_CORS_ALLOWED_ORIGINS)
socketio = SocketIO(app, cors_allowed_origins=Config.SOCKETIO_CORS_ALLOWED_ORIGINS)

# Initialize services
master_agent = MasterAgent()
db_service = DatabaseService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for loan processing"""
    try:
        data = request.json
        message = data.get('message', '')
        customer_id = data.get('customer_id')
        customer_data = data.get('customer_data', {})
        documents = data.get('documents', [])
        
        # Create customer if doesn't exist
        if not customer_id:
            customer_id = db_service.create_customer({
                "phone": customer_data.get("phone"),
                "email": customer_data.get("email"),
                "name": customer_data.get("name", ""),
                "status": "active"
            })
        
        # Process through Master Agent
        context = {
            "customer_id": customer_id,
            "message": message,
            "customer_data": customer_data,
            "documents": documents
        }
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(master_agent.process(context))
        loop.close()
        
        # Save application to database
        application_id = db_service.create_loan_application({
            "customer_id": customer_id,
            "message": message,
            "result": result,
            "status": result.get("status", "processing")
        })
        
        # Emit real-time update via WebSocket
        socketio.emit('loan_update', {
            "customer_id": customer_id,
            "application_id": application_id,
            "status": result.get("status"),
            "decision": result.get("final_decision"),
            "message": "Processing completed"
        })
        
        return jsonify({
            "success": True,
            "customer_id": customer_id,
            "application_id": application_id,
            "result": result,
            "response": generate_user_response(result)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def generate_user_response(result: dict) -> str:
    """Generate user-friendly response from agent result"""
    status = result.get("status", "processing")
    decision = result.get("final_decision", "")
    
    if decision == "approve":
        loan_amount = result.get("underwriting_result", {}).get("loan_amount", 0)
        return f"Congratulations! Your loan of ₹{loan_amount:,.0f} has been approved. You will receive the sanction letter shortly."
    elif decision == "counter_offer":
        counter_offer = result.get("underwriting_result", {}).get("counter_offer", {})
        offered_amount = counter_offer.get("offered_amount", 0)
        return f"We have a counter-offer for you. While we cannot approve your requested amount, we can offer ₹{offered_amount:,.0f}. Would you like to proceed?"
    elif decision == "reject":
        reason = result.get("underwriting_result", {}).get("reason", "Based on our assessment")
        return f"We regret to inform you that your loan application has been declined. Reason: {reason}. Please contact us for more details."
    else:
        return "Your application is being processed. We'll update you shortly."

@app.route('/api/upload-documents', methods=['POST'])
def upload_documents():
    """Handle document uploads"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        document_type = request.form.get('document_type', 'unknown')
        customer_id = request.form.get('customer_id')
        
        # In production, upload to cloud storage (AWS S3, Google Cloud Storage)
        # For now, save locally
        import os
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{customer_id}_{document_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        return jsonify({
            "success": True,
            "document": {
                "type": document_type,
                "filename": filename,
                "url": f"/uploads/{filename}"
            }
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/application-status/<application_id>', methods=['GET'])
def get_application_status(application_id):
    """Get loan application status"""
    try:
        application = db_service.get_loan_application(application_id)
        if not application:
            return jsonify({"success": False, "error": "Application not found"}), 404
        
        return jsonify({
            "success": True,
            "application": application
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/applications', methods=['GET'])
def get_applications():
    """Fetch all applications from database"""
    try:
        applications = db_service.get_all_applications()
        
        # Format applications for frontend
        formatted_apps = []
        if applications:
            for app in applications:
                formatted_apps.append({
                    'id': app.get('application_id', app.get('id', f"APP-{len(formatted_apps) + 1:03d}")),
                    'name': app.get('customer_name', 'Unknown'),
                    'type': app.get('loan_type', 'Personal Loan'),
                    'amount': f"₹{app.get('loan_amount', 0):,}",
                    'date': app.get('created_at', datetime.now().isoformat().split('T')[0]),
                    'progress': app.get('progress', 0),
                    'status': app.get('status', 'pending'),
                    'email': app.get('email', '')
                })
        
        return jsonify({
            "success": True,
            "applications": formatted_apps
        })
    
    except Exception as e:
        print(f"Error fetching applications: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "applications": []
        }), 500

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('connected', {'data': 'Connected to loan processing system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('subscribe')
def handle_subscribe(data):
    """Subscribe to loan updates for a customer"""
    customer_id = data.get('customer_id')
    print(f'Client subscribed to updates for customer: {customer_id}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=Config.DEBUG)

