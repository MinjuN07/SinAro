from fastapi import Depends
from app.services.sentiment_service import SentimentAnalysisService
from app.services.letter_service import LetterService

def get_sentiment_service():
    return SentimentAnalysisService()

def get_letter_service():
    return LetterService()