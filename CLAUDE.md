# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 起動方法

```bash
python3 -m streamlit run app.py
```

初回起動時に Streamlit がメール入力を求めて止まる場合は以下で回避する。

```bash
python3 -m streamlit run app.py --server.headless true
```

または `~/.streamlit/config.toml` に以下を設定する（一度だけ）。

```toml
[browser]
gatherUsageStats = false
```

## アーキテクチャ

`app.py` が唯一のエントリポイントで、Streamlit のサイドバー radio でツールを切り替えるシングルファイル・ルーター構造になっている。各ツールのロジックは `tools/` に分離されており、`app.py` は選択されたツールのモジュールをその場で `import` して呼び出す。

```
app.py              # UI・ルーティング（サイドバー radio → elif チェーン）
tools/              # ツールごとのプロンプト生成関数
  blog_writer.py
  email_reply.py    # 返信（write_email_reply）とゼロから作成（write_email_from_scratch）の2関数
  summarizer.py
  proofreader.py
  title_generator.py
  sns_writer.py     # PLATFORM_SPECS 定数も公開している
utils/
  gemini_client.py  # Gemini API の薄いラッパー。generate(prompt, temperature) が唯一の公開関数
```

## Gemini API

- モデル: `gemini-2.5-flash`（`utils/gemini_client.py` の `get_client()` 内で指定）
- `utils/gemini_client.py` の `generate(prompt, temperature)` を通じて全ツールが API を呼ぶ
- API キーは `.env` の `GEMINI_API_KEY` から読む（`python-dotenv` 使用）

## 新しいツールの追加手順

1. `tools/` に新しいファイルを作成し、生成関数を実装する（`utils.gemini_client.generate` を呼ぶだけでよい）
2. `app.py` のサイドバー radio のリストに項目を追加する
3. `app.py` の `elif` チェーンに対応する UI ブロックを追加する
