from pymongo import MongoClient
from config import Config
from typing import Dict, Any, Optional
from datetime import datetime

class DatabaseService:
    """Database service for MongoDB operations"""
    
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client.get_database()
        self.customers = self.db.customers
        self.loan_applications = self.db.loan_applications
        self.feedback_data = self.db.feedback_data
    
    def create_customer(self, customer_data: Dict[str, Any]) -> str:
        """Create a new customer record"""
        customer_data["created_at"] = datetime.now()
        customer_data["updated_at"] = datetime.now()
        result = self.customers.insert_one(customer_data)
        return str(result.inserted_id)
    
    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get customer by ID"""
        return self.customers.find_one({"_id": customer_id})
    
    def update_customer(self, customer_id: str, updates: Dict[str, Any]) -> bool:
        """Update customer record"""
        updates["updated_at"] = datetime.now()
        result = self.customers.update_one(
            {"_id": customer_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def create_loan_application(self, application_data: Dict[str, Any]) -> str:
        """Create a new loan application"""
        application_data["created_at"] = datetime.now()
        application_data["updated_at"] = datetime.now()
        application_data["status"] = "pending"
        result = self.loan_applications.insert_one(application_data)
        return str(result.inserted_id)
    
    def update_loan_application(self, application_id: str, updates: Dict[str, Any]) -> bool:
        """Update loan application"""
        updates["updated_at"] = datetime.now()
        result = self.loan_applications.update_one(
            {"_id": application_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def get_loan_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get loan application by ID"""
        return self.loan_applications.find_one({"_id": application_id})
    
    def get_all_applications(self) -> list:
        """Get all loan applications from database"""
        try:
            applications = list(self.loan_applications.find({}))
            return applications
        except Exception as e:
            print(f"Error fetching applications: {str(e)}")
            return []
    
