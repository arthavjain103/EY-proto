from typing import Dict, Any
from config import Config
import requests

class OfferMartService:
    """Service for Offer Mart API integration"""
    
    def __init__(self):
        self.api_key = Config.OFFER_MART_API_KEY
        self.api_url = Config.OFFER_MART_API_URL
    
    async def get_pre_approval_data(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get pre-approval limit from Offer Mart API"""
        # Placeholder implementation
        # In production, this would make actual API call
        
        pan_number = customer_data.get("pan_number", "")
        phone = customer_data.get("phone", "")
        
        # Simulate API call
        # response = requests.get(
        #     f"{self.api_url}/pre-approval",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     params={"pan": pan_number, "phone": phone}
        # )
        
        # Placeholder response
        return {
            "pre_approval_limit": 500000,
            "eligibility": True,
            "offers": [
                {"type": "personal_loan", "amount": 500000, "interest_rate": 12},
                {"type": "business_loan", "amount": 1000000, "interest_rate": 14}
            ]
        }

