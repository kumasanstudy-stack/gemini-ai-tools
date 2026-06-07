from utils.gemini_client import generate


def proofread(text: str, focus: list[str]) -> str:
    focus_str = "・".join(focus) if focus else "全般"
    prompt = f"""あなたはプロの校正者・編集者です。以下の文章を校正・改善してください。

## 校正・改善の観点
{focus_str}

## 元の文章
{text}

## 出力形式
1. **修正後の文章**（全文）
2. **主な修正点・改善点**（箇条書き）

の順で出力してください。"""
    return generate(prompt, temperature=0.5)


def improve_style(text: str, target_style: str) -> str:
    prompt = f"""以下の文章を「{target_style}」のスタイルに書き直してください。
意味・内容は変えずに、文体・表現のみを変更してください。

## 元の文章
{text}

書き直した文章のみを出力してください。"""
    return generate(prompt, temperature=0.65)
