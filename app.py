import streamlit as st

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── サイドバー ────────────────────────────────────────────
st.sidebar.title("✍️ AI ライティングツール")
st.sidebar.markdown("---")

tool = st.sidebar.radio(
    "ツールを選択",
    [
        "🏠 ホーム",
        "📝 ブログ記事執筆",
        "📧 メール作成",
        "📋 文章要約",
        "🔍 文章校正・改善",
        "💡 タイトル・見出し生成",
        "📱 SNS投稿文作成",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by Gemini API")

# ─── API キー確認 ──────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    st.warning("⚠️ GEMINI_API_KEY が設定されていません。`.env` ファイルに API キーを設定してください。")

# ─── ページルーティング ────────────────────────────────────

if tool == "🏠 ホーム":
    # ── ホーム ──────────────────────────────────────────────
    st.title("✍️ AI ライティングツール")
    st.markdown("""
個人用のオールインワン AI ライティングアシスタントです。
左のサイドバーからツールを選んで使ってください。

---

| ツール | 概要 |
|--------|------|
| 📝 ブログ記事執筆 | テーマや条件を指定して記事を自動生成 |
| 📧 メール作成 | 返信文の作成 / ゼロからのメール作成 |
| 📋 文章要約 | 長文の要約・重要ポイント抽出 |
| 🔍 文章校正・改善 | 誤字脱字・表現の改善・文体の書き直し |
| 💡 タイトル・見出し生成 | クリックされるタイトルを複数案生成 |
| 📱 SNS投稿文作成 | 各プラットフォーム向け投稿文を生成 |
""")

elif tool == "📝 ブログ記事執筆":
    # ── ブログ記事執筆 ────────────────────────────────────────
    from tools.blog_writer import write_blog

    st.title("📝 ブログ記事執筆")
    st.caption("テーマや条件を入力して、ブログ記事を自動生成します。")

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_area("記事のテーマ・内容", placeholder="例: 初心者向け Python 入門 〜変数と関数の基礎〜", height=80)
        keywords = st.text_input("キーワード（任意・カンマ区切り）", placeholder="例: Python, 初心者, プログラミング学習")
    with col2:
        tone = st.selectbox("文体・トーン", ["わかりやすく親しみやすい", "フォーマル・専門的", "カジュアル・砕けた", "ユーモラス", "情報的・中立"])
        target_audience = st.text_input("ターゲット読者", placeholder="例: プログラミング初心者の社会人")
        word_count = st.select_slider("目標文字数", options=["500字", "800字", "1,200字", "2,000字", "3,000字以上"], value="1,200字")

    if st.button("記事を生成", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("記事のテーマを入力してください。")
        else:
            with st.spinner("記事を生成中..."):
                result = write_blog(topic, tone, target_audience, word_count, keywords)
            st.markdown("---")
            st.markdown(result)
            st.download_button("📥 テキストをダウンロード", result, file_name="blog_article.md", mime="text/markdown")

elif tool == "📧 メール作成":
    # ── メール作成 ─────────────────────────────────────────
    from tools.email_reply import write_email_reply, write_email_from_scratch

    st.title("📧 メール作成")

    tab1, tab2 = st.tabs(["返信文を作成", "ゼロから作成"])

    with tab1:
        st.caption("受け取ったメールを貼り付けると、返信文を生成します。")
        original_email = st.text_area("受信メール（本文を貼り付け）", height=200, placeholder="ここに受信したメールの本文を貼り付けてください...")
        col1, col2 = st.columns(2)
        with col1:
            reply_intent = st.text_area("返信の意図・要件", height=100, placeholder="例: 了承の返信をしたい。日程は来週月〜水なら可能。")
            sender_name = st.text_input("自分の名前（署名用・任意）", placeholder="例: 田中 太郎")
        with col2:
            tone = st.selectbox("文体", ["丁寧なビジネス敬語", "ややカジュアルな敬語", "フレンドリー（社内向け）"], key="reply_tone")
        if st.button("返信文を生成", type="primary", use_container_width=True):
            if not original_email.strip() or not reply_intent.strip():
                st.error("受信メールと返信の意図を入力してください。")
            else:
                with st.spinner("返信文を生成中..."):
                    result = write_email_reply(original_email, reply_intent, tone, sender_name)
                st.markdown("---")
                st.text_area("生成されたメール", result, height=300)
                st.download_button("📥 テキストをダウンロード", result, file_name="email_reply.txt")

    with tab2:
        st.caption("目的・宛先・要点からメールを一から生成します。")
        col1, col2 = st.columns(2)
        with col1:
            purpose = st.text_area("メールの目的", height=80, placeholder="例: 先方へのミーティングのお礼と次回の日程調整")
            key_points = st.text_area("伝えたい要点（箇条書き可）", height=120, placeholder="例:\n・今日のミーティングのお礼\n・次回の候補日は来週月〜水\n・資料は明日中に送付予定")
        with col2:
            recipient = st.text_input("宛先の役職・関係性", placeholder="例: 取引先の部長")
            sender_name2 = st.text_input("自分の名前（署名用・任意）", placeholder="例: 田中 太郎", key="scratch_name")
            tone2 = st.selectbox("文体", ["丁寧なビジネス敬語", "ややカジュアルな敬語", "フレンドリー（社内向け）"], key="scratch_tone")
        if st.button("メールを生成", type="primary", use_container_width=True):
            if not purpose.strip() or not key_points.strip():
                st.error("目的と要点を入力してください。")
            else:
                with st.spinner("メールを生成中..."):
                    result = write_email_from_scratch(purpose, recipient, key_points, tone2, sender_name2)
                st.markdown("---")
                st.text_area("生成されたメール", result, height=300)
                st.download_button("📥 テキストをダウンロード", result, file_name="email.txt")

elif tool == "📋 文章要約":
    # ── 文章要約 ───────────────────────────────────────────
    from tools.summarizer import summarize, extract_key_points

    st.title("📋 文章要約")

    tab1, tab2 = st.tabs(["要約する", "重要ポイント抽出"])

    with tab1:
        st.caption("長い文章を指定したスタイルと長さで要約します。")
        text = st.text_area("要約したい文章を貼り付け", height=300, placeholder="ここに要約したい文章を貼り付けてください...")
        col1, col2 = st.columns(2)
        with col1:
            style = st.selectbox("要約スタイル", ["箇条書き", "一段落の散文", "段落ごとのまとめ", "ニュース記事風"])
        with col2:
            length = st.selectbox("要約の長さ", ["3〜5文", "100字程度", "200〜300字", "500字程度"])
        if st.button("要約する", type="primary", use_container_width=True):
            if not text.strip():
                st.error("文章を入力してください。")
            else:
                with st.spinner("要約中..."):
                    result = summarize(text, style, length)
                st.markdown("---")
                st.markdown(result)
                st.download_button("📥 テキストをダウンロード", result, file_name="summary.txt")

    with tab2:
        st.caption("文章から重要なポイントを箇条書きで抽出します。")
        text2 = st.text_area("文章を貼り付け", height=300, key="keypoints_text", placeholder="ここに文章を貼り付けてください...")
        if st.button("ポイントを抽出", type="primary", use_container_width=True):
            if not text2.strip():
                st.error("文章を入力してください。")
            else:
                with st.spinner("抽出中..."):
                    result2 = extract_key_points(text2)
                st.markdown("---")
                st.markdown(result2)
                st.download_button("📥 テキストをダウンロード", result2, file_name="key_points.txt")

elif tool == "🔍 文章校正・改善":
    # ── 文章校正・改善 ────────────────────────────────────────
    from tools.proofreader import proofread, improve_style

    st.title("🔍 文章校正・改善")

    tab1, tab2 = st.tabs(["校正・改善", "文体の書き直し"])

    with tab1:
        st.caption("文章の誤字・脱字・表現の改善点を指摘し、修正済みの文章を返します。")
        text = st.text_area("校正したい文章", height=250, placeholder="ここに文章を貼り付けてください...")
        focus = st.multiselect(
            "改善の観点（複数選択可）",
            ["誤字・脱字の修正", "文法の修正", "表現の自然さ", "読みやすさの改善", "論理の流れ", "語彙の豊かさ"],
            default=["誤字・脱字の修正", "表現の自然さ"],
        )
        if st.button("校正する", type="primary", use_container_width=True):
            if not text.strip():
                st.error("文章を入力してください。")
            else:
                with st.spinner("校正中..."):
                    result = proofread(text, focus)
                st.markdown("---")
                st.markdown(result)
                st.download_button("📥 テキストをダウンロード", result, file_name="proofread.txt")

    with tab2:
        st.caption("文章の意味はそのままに、指定した文体・スタイルに書き直します。")
        text2 = st.text_area("書き直したい文章", height=200, key="style_text", placeholder="ここに文章を貼り付けてください...")
        target_style = st.selectbox(
            "目標の文体",
            ["ビジネス敬語", "カジュアル・口語体", "学術的・論文調", "簡潔・箇条書き風", "ニュース記事調", "ポップ・フレンドリー"],
        )
        if st.button("書き直す", type="primary", use_container_width=True):
            if not text2.strip():
                st.error("文章を入力してください。")
            else:
                with st.spinner("書き直し中..."):
                    result2 = improve_style(text2, target_style)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**元の文章**")
                    st.text_area("", text2, height=200, disabled=True, label_visibility="collapsed")
                with col2:
                    st.markdown("**書き直した文章**")
                    st.text_area("", result2, height=200, label_visibility="collapsed")
                st.download_button("📥 書き直し文をダウンロード", result2, file_name="rewritten.txt")

elif tool == "💡 タイトル・見出し生成":
    # ── タイトル・見出し生成 ──────────────────────────────────
    from tools.title_generator import generate_titles, generate_headings

    st.title("💡 タイトル・見出し生成")

    tab1, tab2 = st.tabs(["タイトル生成", "見出し構成の提案"])

    with tab1:
        st.caption("テーマから魅力的なタイトル案を複数生成します。")
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_area("テーマ・内容", height=100, placeholder="例: 在宅ワークの生産性を上げる方法")
            tone = st.selectbox("トーン", ["興味をそそる・キャッチー", "専門的・信頼性重視", "実用的・具体的", "感情に訴える", "ユーモラス"])
        with col2:
            content_type = st.selectbox("コンテンツの種類", ["ブログ記事", "YouTube タイトル", "ニュースレター", "プレスリリース", "SNS 投稿"])
            count = st.slider("生成数", 3, 10, 5)
        if st.button("タイトルを生成", type="primary", use_container_width=True):
            if not topic.strip():
                st.error("テーマを入力してください。")
            else:
                with st.spinner("生成中..."):
                    result = generate_titles(topic, content_type, count, tone)
                st.markdown("---")
                st.markdown(result)

    with tab2:
        st.caption("記事の概要から H2/H3 の見出し構成を提案します。")
        outline = st.text_area("記事の概要・アウトライン", height=200, placeholder="例:\n・対象: 中小企業の経営者\n・内容: DX（デジタルトランスフォーメーション）の基礎と最初のステップ\n・伝えたいこと: 難しくないこと、小さな取り組みから始められること")
        if st.button("見出し構成を提案", type="primary", use_container_width=True):
            if not outline.strip():
                st.error("記事の概要を入力してください。")
            else:
                with st.spinner("生成中..."):
                    result2 = generate_headings(outline)
                st.markdown("---")
                st.markdown(result2)

elif tool == "📱 SNS投稿文作成":
    # ── SNS 投稿文作成 ────────────────────────────────────────
    from tools.sns_writer import write_sns_post, PLATFORM_SPECS

    st.title("📱 SNS投稿文作成")
    st.caption("各プラットフォームの特性に合わせた投稿文を生成します。")

    col1, col2 = st.columns([1, 1])
    with col1:
        platform = st.selectbox("プラットフォーム", list(PLATFORM_SPECS.keys()))
        topic = st.text_area("投稿のテーマ・内容", height=100, placeholder="例: 新しいカフェを開店しました。こだわりのコーヒーと静かな空間が特徴です。")
    with col2:
        tone = st.selectbox("トーン", ["親しみやすい・カジュアル", "プロフェッショナル", "ポジティブ・明るい", "情報提供・教育的", "感情的・共感を誘う"])
        count = st.slider("生成パターン数", 1, 5, 3)
        include_hashtags = st.checkbox("ハッシュタグを含める", value=True)

    spec = PLATFORM_SPECS[platform]
    st.info(f"**{platform}** — 目安文字数: {spec['max_chars']}字以内 / {spec['note']}")

    if st.button("投稿文を生成", type="primary", use_container_width=True):
        if not topic.strip():
            st.error("投稿のテーマを入力してください。")
        else:
            with st.spinner("生成中..."):
                result = write_sns_post(platform, topic, tone, include_hashtags, count)
            st.markdown("---")
            st.markdown(result)
            st.download_button("📥 テキストをダウンロード", result, file_name="sns_posts.txt")
