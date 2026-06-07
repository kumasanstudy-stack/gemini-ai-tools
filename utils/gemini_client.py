import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_client() -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate(prompt: str, temperature: float = 0.7) -> str:
    model = get_client()
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(temperature=temperature),
    )
    return response.text
