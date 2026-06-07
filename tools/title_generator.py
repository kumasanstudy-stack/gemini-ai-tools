from utils.gemini_client import generate


def generate_titles(topic: str, content_type: str, count: int, tone: str) -> str:
    prompt = f"""あなたはコピーライターの専門家です。以下の条件でタイトル・見出しを{count}個生成してください。

## 条件
- テーマ・内容: {topic}
- コンテンツの種類: {content_type}
- トーン: {tone}

## 要件
- クリックされやすく、内容を的確に表すタイトルを生成すること
- バリエーションを持たせること（疑問形・数字入り・メリット訴求など）
- 各タイトルに一言コメントを添えること

番号付きリスト形式で出力してください。"""
    return generate(prompt, temperature=0.85)


def generate_headings(article_outline: str) -> str:
    prompt = f"""以下の記事概要に基づいて、記事の見出し構成（H2/H3）を提案してください。

## 記事概要
{article_outline}

Markdown の見出し記法（## / ###）で出力してください。各見出しに一行の説明を添えてください。"""
    return generate(prompt, temperature=0.7)
