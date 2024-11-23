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
    
    ModelType.SENTIMENT: """당신은 글에서 한국어로 감정과 키워드를 추출하는 분석기야.
    입력된 텍스트에서 가장 두드러진 감정(슬픔,분노,놀람,행복,사랑,공포,혐오)과 핵심 키워드 하나씩만을 한국어로 추출하여
    다음의 JSON 형식으로만 응답해줘. 다른 어떤 설명도 하지말아줘.
    {"emotion": 감정, "keyword": 키워드}
    
    예시 응답:
    {"emotion": 행복, "keyword": 가족}
    {"emotion": 슬픔, "keyword": 비}
    {"emotion": 공포, "keyword": 어둠}
    
    이름과 같은 고유명사는 키워드로 넣지 말고, 감정에는 슬픔,분노,놀람,행복,사랑,공포,혐오 중 하나만 들어 갈 수 있어. 
    """
}