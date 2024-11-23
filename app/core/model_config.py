from enum import Enum

class ModelType(Enum):
    LETTER = "ko-llama-letter-generator"
    SENTIMENT = "ko-llama-sentiment-analyzer"
    SUMMARY = "ko-llama-diary-summarizer"
    
MODEL_OPTIONS = {
    ModelType.SENTIMENT: {
        "num_ctx": 8096,
        "temperature": 0.2,
        "top_p": 0.3, 
        "top_k": 20,
        "num_predict": 1024,
        "repeat_penalty": 1.5,
        "presence_penalty": 0.5,
        "frequency_penalty": 0.3,
        "mirostat": 1,
        "mirostat_tau": 0.5,
        "stop": ["\n\n\n","\n\n","\n"]
    },
    ModelType.LETTER: {
        "num_ctx": 8096,
        "temperature": 0.5,
        "top_p": 0.7,
        "top_k": 20,
        "num_predict": 4048,
        "frequency_penalty": 0.5,
    },
}