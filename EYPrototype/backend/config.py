import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/loan_system')
    FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS', '')
    
    # External API Keys
    GOOGLE_VISION_API_KEY = os.getenv('GOOGLE_VISION_API_KEY', '')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '')
    
    # Credit Bureau & Offer Mart APIs
    CREDIT_BUREAU_API_KEY = os.getenv('CREDIT_BUREAU_API_KEY', '')
    CREDIT_BUREAU_API_URL = os.getenv('CREDIT_BUREAU_API_URL', 'https://api.creditbureau.com')
    OFFER_MART_API_KEY = os.getenv('OFFER_MART_API_KEY', '')
    OFFER_MART_API_URL = os.getenv('OFFER_MART_API_URL', 'https://api.offermart.com')
    
    # Risk Scoring Thresholds
    LOW_RISK_THRESHOLD = 0.75
    MEDIUM_RISK_THRESHOLD = 0.50
    HIGH_RISK_THRESHOLD = 0.25
    
    # Verification Confidence Thresholds
    VERIFICATION_CONFIDENCE_HIGH = 0.65
    VERIFICATION_CONFIDENCE_LOW = 0.50
    
    # EMI Threshold
    EMI_SALARY_RATIO_THRESHOLD = 0.50
    
    # WebSocket Configuration
    SOCKETIO_CORS_ALLOWED_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

