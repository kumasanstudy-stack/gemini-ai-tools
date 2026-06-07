from utils.gemini_client import generate


def write_blog(
    topic: str,
    tone: str,
    target_audience: str,
    word_count: str,
    keywords: str,
) -> str:
    keywords_line = f"- キーワード: {keywords}" if keywords.strip() else ""
    prompt = f"""あなたはプロのブログライターです。以下の条件でブログ記事を執筆してください。

## 条件
- テーマ: {topic}
- 文体・トーン: {tone}
- ターゲット読者: {target_audience}
- 目標文字数: {word_count}
{keywords_line}

## 出力形式
- タイトル（H1）
- リード文（導入部）
- 本文（H2/H3 で章立て）
- まとめ

Markdown 形式で出力してください。"""
    return generate(prompt, temperature=0.75)
