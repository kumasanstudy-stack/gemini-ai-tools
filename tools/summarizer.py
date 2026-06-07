from utils.gemini_client import generate


def summarize(text: str, style: str, length: str) -> str:
    prompt = f"""以下の文章を{style}形式で要約してください。
要約の長さの目安: {length}

## 元の文章
{text}

要約を出力してください。"""
    return generate(prompt, temperature=0.4)


def extract_key_points(text: str) -> str:
    prompt = f"""以下の文章から重要なポイントを箇条書きで抽出してください。
各ポイントは簡潔に、読者が素早く内容を把握できるようにまとめてください。

## 文章
{text}"""
    return generate(prompt, temperature=0.4)
