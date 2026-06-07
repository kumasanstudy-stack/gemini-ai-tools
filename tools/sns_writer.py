from utils.gemini_client import generate

PLATFORM_SPECS = {
    "Twitter / X": {"max_chars": 140, "note": "ハッシュタグ2〜3個推奨"},
    "Instagram": {"max_chars": 300, "note": "絵文字・ハッシュタグ多め推奨"},
    "LinkedIn": {"max_chars": 700, "note": "プロフェッショナルなトーン推奨"},
    "Facebook": {"max_chars": 500, "note": "親しみやすいトーン推奨"},
    "Threads": {"max_chars": 500, "note": "カジュアルなトーン推奨"},
}


def write_sns_post(
    platform: str,
    topic: str,
    tone: str,
    include_hashtags: bool,
    count: int,
) -> str:
    spec = PLATFORM_SPECS.get(platform, {"max_chars": 300, "note": ""})
    hashtag_instruction = "ハッシュタグを含めてください。" if include_hashtags else "ハッシュタグは不要です。"

    prompt = f"""{platform} 向けの投稿文を{count}パターン作成してください。

## 条件
- 投稿テーマ: {topic}
- トーン・雰囲気: {tone}
- 目安文字数: {spec["max_chars"]}文字以内
- {spec["note"]}
- {hashtag_instruction}

各パターンを「--- パターン N ---」で区切って出力してください。"""
    return generate(prompt, temperature=0.8)
