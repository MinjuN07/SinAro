from enum import Enum

class ModelType(Enum):
    LETTER = "ko-llama-letter-generator"
    SENTIMENT = "ko-llama-sentiment-analyzer"
    SUMMARY = "ko-llama-diary-summarizer"