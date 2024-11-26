from enum import Enum

class ModelType(Enum):
    SENTIMENT = "SENTIMENT"
    LETTER = "LETTER"

MODEL_NAME = {
    ModelType.SENTIMENT: "ko-gemma-9b",
    ModelType.LETTER: "ko-gemma-9b"
}

MODEL_SYSTEM = {
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
""",
    
    ModelType.LETTER: """###역할###
너는 감성적이고 자연스러운 편지 작성 전문가야. 특히 원본 편지를 수정하여 감정과 키워드를 포함하는 일을 잘하지. 

###지시###
다음 요구 사항을 기반으로 원본 편지에 감정과 키워드를 자연스럽게 통합하여 편지를 완성해줘.
1. 원본 편지의 흐름과 의도를 정확히 파악하고, 제시된 감정과 키워드를 자연스럽게 편지에 녹아들게 해줘.
2. 편지를 생성할 때는 무조건 한국어를 사용하고, 이모티콘 쓰지 말아줘.
3. 반드시 원본 편지의 말투와 똑같이 작성해줘.
4. 반드시 하나의 완성된 편지로 만들어줘.
5. "만약" 감정들과 키워드들 중 원본 편지와 자연스럽게 어울리지 않는 감정과 키워드가 있다면 해당 감정과 키워드는 포함하지마.
    """
}

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
        "num_ctx": 8192,   
        "temperature": 0.6,     
        "top_p": 0.85,          
        "top_k": 40,            
        "num_predict": 4096,   
        "frequency_penalty": 0.3,
        "presence_penalty": 0.3,  
        "repeat_penalty": 1.1,    
        "stop": ["\n\n\n", "###"] 
    },
}