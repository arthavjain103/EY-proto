from typing import Dict, Any
from .base_agent import BaseAgent
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import io
import os
from config import Config
import requests

class SanctionLetterAgent(BaseAgent):
    """Sanction Letter Agent generates and delivers sanction letters"""
    
    def __init__(self):
        super().__init__(
            agent_name="SanctionLetterAgent",
            system_prompt="""You are a Sanction Letter Generator Agent.
            Your role is to:
            1. Generate professional PDF sanction letters
            2. Include all loan terms and conditions
            3. Deliver via multiple channels (Email, WhatsApp, SMS)
            4. Update customer status in the system"""
        )
    
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate and deliver sanction letter"""
        customer_data = context.get("customer_data", {})
        loan_details = context.get("loan_details", {})
        decision = context.get("decision", "approve")
        
        if decision == "reject":
            return {
                "status": "skipped",
                "reason": "Loan rejected, no sanction letter generated"
            }
        
        # Generate PDF
        pdf_path = await self._generate_pdf(customer_data, loan_details, decision)
        
        # Deliver via multiple channels
        delivery_results = await self._deliver_sanction_letter(
            customer_data,
            pdf_path,
            loan_details
        )
        
        result = {
            "status": "delivered",
            "pdf_path": pdf_path,
            "delivery_channels": delivery_results,
            "customer_id": customer_data.get("customer_id"),
            "loan_amount": loan_details.get("loan_amount", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        self.log_action("Sanction Letter Generated", result)
        return result
    
    async def _generate_pdf(self, customer_data: Dict[str, Any], 
                           loan_details: Dict[str, Any], decision: str) -> str:
        """Generate PDF sanction letter"""
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
        # Container for PDF elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Add title
        elements.append(Paragraph("LOAN SANCTION LETTER", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Date
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=2  # Right alignment
        )
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%d %B, %Y')}", date_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Customer details
        customer_name = customer_data.get("name", "Customer")
        customer_address = customer_data.get("address", "Address not provided")
        
        elements.append(Paragraph(f"Dear {customer_name},", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Sanction letter content
        if decision == "counter_offer":
            sanction_text = f"""
            <para>We are pleased to inform you that your loan application has been reviewed. 
            While we cannot approve your requested amount, we are pleased to offer you a 
            counter-proposal as detailed below.</para>
            """
        else:
            sanction_text = f"""
            <para>We are pleased to inform you that your loan application has been reviewed 
            and we are pleased to sanction a loan to you subject to the terms and conditions 
            mentioned below.</para>
            """
        
        elements.append(Paragraph(sanction_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Loan details table
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0) * 100
        tenure_months = loan_details.get("tenure_months", 0)
        emi_amount = loan_details.get("emi_amount", 0)
        
        loan_data = [
            ['Loan Amount', f'₹{loan_amount:,.0f}'],
            ['Interest Rate (Annual)', f'{interest_rate:.2f}%'],
            ['Loan Tenure', f'{tenure_months} months ({tenure_months//12} years)'],
            ['EMI Amount', f'₹{emi_amount:,.2f}'],
        ]
        
        if decision == "counter_offer":
            loan_data.insert(0, ['Requested Amount', f'₹{customer_data.get("requested_amount", 0):,.0f}'])
        
        loan_table = Table(loan_data, colWidths=[3*inch, 3*inch])
        loan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(loan_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Terms and conditions
        terms_text = """
        <b>Terms and Conditions:</b><br/>
        1. This sanction is valid for 30 days from the date of this letter.<br/>
        2. Final approval is subject to verification of all submitted documents.<br/>
        3. The loan will be disbursed after completion of all formalities.<br/>
        4. Interest rates are subject to change as per market conditions.<br/>
        5. Please contact us for any queries or clarifications.<br/>
        """
        
        elements.append(Paragraph(terms_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Closing
        closing_text = """
        <para>We look forward to serving you and hope this loan helps you achieve your financial goals.</para>
        <para>Thank you for choosing our services.</para>
        """
        elements.append(Paragraph(closing_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Signature
        elements.append(Paragraph("Sincerely,<br/><b>Loan Processing Team</b>", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        # Save PDF to file
        pdf_filename = f"sanction_letter_{customer_data.get('customer_id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join("sanction_letters", pdf_filename)
        
        # Create directory if it doesn't exist
        os.makedirs("sanction_letters", exist_ok=True)
        
        # Write PDF to file
        with open(pdf_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        return pdf_path
    
    async def _deliver_sanction_letter(self, customer_data: Dict[str, Any], 
                                      pdf_path: str, loan_details: Dict[str, Any]) -> Dict[str, Any]:
        """Deliver sanction letter via multiple channels"""
        results = {}
        
        # Email delivery
        email = customer_data.get("email")
        if email:
            email_result = await self._send_email(email, pdf_path, loan_details)
            results["email"] = email_result
        
        # WhatsApp delivery
        phone = customer_data.get("phone")
        if phone:
            whatsapp_result = await self._send_whatsapp(phone, pdf_path, loan_details)
            results["whatsapp"] = whatsapp_result
        
        # SMS notification
        if phone:
            sms_result = await self._send_sms(phone, loan_details)
            results["sms"] = sms_result
        
        return results
    
    async def _send_email(self, email: str, pdf_path: str, loan_details: Dict[str, Any]) -> Dict[str, Any]:
        """Send sanction letter via email"""
        # Placeholder - would integrate with Gmail API or SMTP
        return {
            "status": "sent",
            "channel": "email",
            "recipient": email,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _send_whatsapp(self, phone: str, pdf_path: str, loan_details: Dict[str, Any]) -> Dict[str, Any]:
        """Send sanction letter via WhatsApp using Twilio"""
        # Placeholder - would integrate with Twilio WhatsApp API
        from twilio.rest import Client
        
        try:
            # client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
            # message = client.messages.create(
            #     from_=f'whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}',
            #     body=f'Your loan of ₹{loan_details.get("loan_amount", 0):,.0f} has been sanctioned. Please check your email for the sanction letter.',
            #     to=f'whatsapp:{phone}'
            # )
            
            return {
                "status": "sent",
                "channel": "whatsapp",
                "recipient": phone,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "failed",
                "channel": "whatsapp",
                "error": str(e)
            }
    
    async def _send_sms(self, phone: str, loan_details: Dict[str, Any]) -> Dict[str, Any]:
        """Send SMS notification"""
        # Placeholder - would integrate with Twilio SMS
        return {
            "status": "sent",
            "channel": "sms",
            "recipient": phone,
            "message": f"Loan sanctioned: ₹{loan_details.get('loan_amount', 0):,.0f}. Check email/WhatsApp for details.",
            "timestamp": datetime.now().isoformat()
        }

