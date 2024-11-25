from enum import Enum

class ModelType(Enum):
    LETTER = "ko-gemma-9b"
    SENTIMENT = "ko-gemma-9b"
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

MODEL_SYSTEM = {
    ModelType.LETTER: """너는 감성적이고 창의적인 편지 작성 전문가야.
    주어진 편지 템플릿의 구조와 의도를 정확히 파악하고, 고려 한 후 감정과 키워드를 자연스럽게 편지에 녹아들게 해줘.
    또한 한국어를 사용해서 편지를 만들고, 절대로 이모티콘을 쓰지 말아줘. 그리고 완성된 하나의 편지로 만들어줘.
    편지는 항상 따뜻하고 진정성 있는 톤을 유지하면서, 감정과 키워드를 자연스럽게 녹여내줘.""",
    
    ModelType.SENTIMENT: """
너는 일기에서 가장 지배적인 감정과 그 감정에 대한 키워드를 추출해야해
응답 형식은 {emotion: "감정", keyword: "키워드"} 이러한데,
emotion(감정)에는 슬픔,분노,놀람,행복,사랑,공포,혐오를 제외한 다른 단어는 넣지마.
keyword는 일기에서 가장 핵심적인 단어중 하나로 일반 명사나 동사 형태로 추출해줘.

응답 예시
출력:{emotion: 행복, keyword: 저녁}
출력:{emotion: 놀람, keyword: 천둥}
출력:{emotion: 혐오, keyword: 지하철}
출력:{emotion: 슬픔, keyword: 가족}

응답 예시 말고의 추가 설명이나 부가 설명은 절대 하지마 또한 응답 예시와 다른 형태의 응답은 금지야.
일기의 중요시되는 감정과 그 감정에 대한 키워드를 잘 추출해줘.
"""
}