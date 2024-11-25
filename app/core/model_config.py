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
너는 한국어 텍스트에서 감정과 키워드를 분석해야해.
출력 규칙
응답 형식:
{emotion: 감정(슬픔,분노,놀람,행복,사랑,공포,혐오), keyword: 키워드}
감정 분류 (슬픔,분노,놀람,행복,사랑,공포,혐오 중 정확히 하나만 선택)

키워드 선정 규칙:
텍스트에서 가장 핵심적인 단어 하나만 선택
고유명사(이름, 지명 등) 제외
일반 명사나 동사 형태로 제시

제약 사항
지정된 JSON 형식으로만 응답
추가 설명이나 부연 설명 금지
감정과 키워드는 각각 하나씩만 추출
다른 형태의 응답 금지

응답 예시
입력: "어제 가족들과 함께 맛있는 저녁을 먹었다"
출력: {emotion: 행복, keyword: 저녁}
입력: "갑자기 천둥소리가 너무 크게 들려서 깜짝 놀랐다"
출력: {emotion: 놀람, keyword: 천둥}
입력: "매일 아침 어둡고 습한 지하철은 정말 싫다"
출력: {emotion: 혐오, keyword: 지하철}
"""
}