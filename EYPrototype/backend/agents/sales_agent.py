from typing import Dict, Any
from .base_agent import BaseAgent
import re

class SalesAgent(BaseAgent):
    """Sales Agent handles customer interactions, objection handling, and intent detection"""
    
    def __init__(self):
        super().__init__(
            agent_name="SalesAgent",
            system_prompt="""You are a Sales Agent for a loan processing system.
            Your responsibilities include:
            1. Detecting customer intent and interest level
            2. Handling objections and concerns
            3. Collecting basic customer information
            4. Identifying urgency and emergency cases
            5. Engaging customers in a friendly, professional manner
            
            Analyze customer messages for:
            - Loan interest and intent
            - Objections or concerns
            - Urgency indicators
            - Required information collection"""
        )
    
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process customer message through Sales Agent"""
        message = context.get("message", "").lower()
        customer_data = context.get("customer_data", {})
        
        # Detect intent and interest
        intent_analysis = self._detect_intent(message)
        
        # Check for objections
        objection_detected = self._detect_objections(message)
        objection_response = None
        
        if objection_detected:
            objection_response = self._handle_objection(message)
        
        # Extract customer information
        extracted_info = self._extract_customer_info(message)
        customer_data.update(extracted_info)
        
        # Detect urgency
        urgency_level = self._detect_urgency(message)
        
        # Determine interest level
        interested = intent_analysis.get("interest_score", 0) > 0.6
        
        result = {
            "intent": intent_analysis,
            "objection_detected": objection_detected,
            "objection_response": objection_response,
            "interested": interested,
            "urgency_level": urgency_level,
            "customer_data": customer_data,
            "next_action": self._determine_next_action(intent_analysis, objection_detected, interested)
        }
        
        self.log_action("Sales Processing", result)
        return result
    
    def _detect_intent(self, message: str) -> Dict[str, Any]:
        """Detect customer intent using NLP"""
        loan_keywords = ["loan", "credit", "borrow", "finance", "emi", "interest rate"]
        inquiry_keywords = ["information", "details", "how", "what", "tell me"]
        application_keywords = ["apply", "application", "need", "want", "require"]
        
        has_loan_intent = any(keyword in message for keyword in loan_keywords)
        is_inquiry = any(keyword in message for keyword in inquiry_keywords)
        is_application = any(keyword in message for keyword in application_keywords)
        
        # Calculate interest score
        interest_score = 0.0
        if is_application:
            interest_score = 0.9
        elif has_loan_intent and not is_inquiry:
            interest_score = 0.7
        elif has_loan_intent:
            interest_score = 0.5
        
        return {
            "type": "application" if is_application else ("inquiry" if is_inquiry else "general"),
            "interest_score": interest_score,
            "has_loan_intent": has_loan_intent
        }
    
    def _detect_objections(self, message: str) -> bool:
        """Detect customer objections or concerns"""
        objection_keywords = [
            "expensive", "high interest", "too much", "not sure", "doubt",
            "worried", "concerned", "problem", "issue", "difficult",
            "complicated", "long process", "too slow"
        ]
        
        negative_words = ["no", "don't", "won't", "can't", "cannot", "refuse"]
        
        has_objection_keywords = any(keyword in message for keyword in objection_keywords)
        has_negative_words = any(word in message for word in negative_words)
        
        return has_objection_keywords or has_negative_words
    
    def _handle_objection(self, message: str) -> str:
        """Generate response to handle objections"""
        # Use LLM to generate personalized objection handling response
        prompt = f"""Customer message: {message}
        
        Generate a professional, empathetic response that addresses the customer's concern
        and highlights the benefits of our loan process (fast approval, transparent process,
        competitive rates, easy application). Keep it concise and friendly."""
        
        response = self._call_llm(prompt)
        return response
    
    def _extract_customer_info(self, message: str) -> Dict[str, Any]:
        """Extract customer information from message"""
        info = {}
        
        # Extract phone number
        phone_pattern = r'\b\d{10}\b'
        phone_match = re.search(phone_pattern, message)
        if phone_match:
            info["phone"] = phone_match.group()
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message)
        if email_match:
            info["email"] = email_match.group()
        
        # Extract loan amount
        amount_pattern = r'(?:rs\.?|₹|rupees?)\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakh|lac|thousand|k)?'
        amount_match = re.search(amount_pattern, message, re.IGNORECASE)
        if amount_match:
            info["requested_amount"] = amount_match.group(1).replace(',', '')
        
        return info
    
    def _detect_urgency(self, message: str) -> str:
        """Detect urgency level in customer message"""
        urgent_keywords = ["urgent", "emergency", "immediate", "asap", "quickly", "fast", "critical"]
        moderate_keywords = ["soon", "quick", "prefer", "would like"]
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in urgent_keywords):
            return "high"
        elif any(keyword in message_lower for keyword in moderate_keywords):
            return "medium"
        else:
            return "low"
    
    def _determine_next_action(self, intent: Dict[str, Any], objection: bool, interested: bool) -> str:
        """Determine next action based on analysis"""
        if objection:
            return "handle_objection"
        elif not interested:
            return "engage_customer"
        elif intent.get("type") == "application":
            return "collect_documents"
        else:
            return "provide_information"

