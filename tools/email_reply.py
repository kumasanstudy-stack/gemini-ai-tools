from utils.gemini_client import generate


def write_email_reply(
    original_email: str,
    reply_intent: str,
    tone: str,
    sender_name: str,
) -> str:
    sender_line = f"- 送信者名: {sender_name}" if sender_name.strip() else ""
    prompt = f"""あなたはビジネスメールの専門家です。以下の受信メールに対する返信文を作成してください。

## 受信メール
{original_email}

## 返信の意図・要件
{reply_intent}

## 文体
{tone}
{sender_line}

## 出力形式
件名と本文を含む完全なメール形式で出力してください。
署名欄は「---\\n[お名前]」のプレースホルダーを使用してください。"""
    return generate(prompt, temperature=0.6)


def write_email_from_scratch(
    purpose: str,
    recipient: str,
    key_points: str,
    tone: str,
    sender_name: str,
) -> str:
    sender_line = f"- 送信者名: {sender_name}" if sender_name.strip() else ""
    prompt = f"""あなたはビジネスメールの専門家です。以下の条件でメールを作成してください。

## 条件
- 目的: {purpose}
- 宛先（役職・関係性）: {recipient}
- 伝えたい要点: {key_points}
- 文体: {tone}
{sender_line}

件名と本文を含む完全なメール形式で出力してください。
署名欄は「---\\n[お名前]」のプレースホルダーを使用してください。"""
    return generate(prompt, temperature=0.6)
