import streamlit as st
import time
import json
import os

TEMPLATE_FILE = "my_templates.json"

def load_templates():
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_templates(templates):
    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)

if "my_templates" not in st.session_state:
    st.session_state.my_templates = load_templates()

st.set_page_config(page_title="Nano Banana AI Visualizer", layout="wide")
st.title("Nano Banana プロンプトシミュレーター")
st.write("初心者からプロまで直感的に使える、高品質な画像生成プロンプトを作成します。")

# --- 🔰 はじめての方へ（使い方ガイド） ---
with st.expander("🔰 はじめての方へ：このアプリの超カンタンな使い方", expanded=False):
    st.markdown("""
    **たった3ステップで、プロ級の画像生成用プロンプト（魔法の呪文）が完成します！**
    
    1. 📝 **作りたい画像の設定**
       - サムネイルか図解かを選び、ターゲット層（誰に見せたいか）を選びます。（例：「美容」「ビジネス」など）
       - スマホ用かPC用かでキャンバス（画像）の形も選びましょう。

    2. 🎨 **全体のテイスト・構成の設定**
       - パキッとしたアニメ風か、写真のようなリアル風かなど、画像の「絵柄（メインテイスト）」を選択します。
       - 文字力（ジャンプ率）や細かい色味の指定なども直感的に選べます。

    3. ✏️ **スライド内容の入力 ～ プロンプト錬成！**
       - 画像の中に入れたい「タイトル」や「テキスト」をそのまま入力します。（何枚も連続で作るカルーセルにも対応！）
       - 最後に画面を下までスクロールして **「オリジナル・プロンプトを錬成する 🍌」** ボタンをポチッ！

    💡 **【完成したらどうするの？】**
    画面の一番下に出力される **「英語の呪文（プロンプト）」** の右上のコピーボタン（📋マーク）を押して、
    そのまま **Geminiなどの画像生成AI** の入力欄にペーストして送信するだけで、超高品質な画像が完成します！
    
    💾 **【便利機能】**
    「この設定、よく使うから保存しておきたい！」と思ったら、一番下で「マイテンプレート」として名前をつけて保存できます。
    次回からはページ一番上の「マイテンプレートからロード」で一瞬で復元できますよ！
    """)

# プルダウン（Selectbox）が上ではなく必ず下に開くように、画面下部に十分な余白を設定するハック
st.markdown(
    """
    <style>
    /* ドロップダウンが下に開くための余白 */
    .block-container {
        padding-bottom: 50vh !important;
        max-width: 1200px !important;
    }
    
    /* レスポンシブ対応：スマホ表示時の最適化 */
    @media (max-width: 768px) {
        /* タイトルサイズ調整 */
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.4rem !important; }
        
        /* カラムの余白調整 */
        .st-emotion-cache-16txtl3 { padding: 1rem 0; }
        
        /* 入力エリアの高さ調整 */
        textarea { min-height: 80px !important; }
        
        /* ボタンのパディング調整 */
        button { padding: 0.5rem 1rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === 究極の選択肢定義（Ultimate Options） ===
use_cases = ["サムネイル（YouTube・記事用）", "図解（SNS・プレゼン用）", "汎用画像生成（自由設定）"]
aspect_ratios = ["1:1（正方形）", "16:9（横長）", "3:4（縦長）", "9:16（縦長フル）", "21:9（シネマティック）", "4:3（クラシック）"]
char_usages = ["入れない（キャラなし）", "自分のキャラクターを使う（画像アップロード）"]
char_positions = [
    "指定なし（標準）",
    # ベーシック
    "1. 案内役（画面の端に小さく配置。文字がメイン）", "2. バランス（中央寄りに中サイズ。文字と同じ存在感）", "3. メインビジュアル（中央に大きく配置。文字は見出し中心で少なめ）",
    # 動き・ストーリー
    "4. ストーリー主役（表情・動きで語らせる）", "5. パルクール・アクション（躍動的なポーズで視線を誘導）", "6. リフレクション（水面や鏡に映る姿を効果的に配置）",
    # 抽象・コンセプチュアル
    "7. シルエット配置（逆光で輪郭だけを見せる）", "8. 巨大化（風景を覆い尽くすような巨大なスケールで配置）", "9. ミニチュア化（巨大な文字やオブジェクトの上に立たせる）",
    # その他
    "10. 周囲配置（中央は小さめ、周りに情報を配置）", "11. おまかせ（テーマと構造から最適化）"
]

main_tastes = [
    # 王道・定番
    "1. かわいい系（ちびキャラ・パステル・丸み）", "2. かっこいい系（シャープ・モノトーン・エッジ）", "3. おしゃれ系（余白・抜け感・流行色）", "4. シンプル系（フラット・ミニマル・情報整理）",
    # ビジネス・教育
    "5. ビジネス系（誠実・青基調・信頼感）", "6. 教育・知育系（カラフル・親しみやすさ・わかりやすさ）", "7. お仕事系（制服・現場感・リアリティ）", "8. インフォグラフィック系（データ可視化・クリーン）",
    # カルチャー・ホビー
    "9. アニメ・漫画系（セル画風・トーン・集中線）", "10. ゲーム系（ドット絵・UI風・ファンタジー）", "11. 映画・シネマティック系（レターボックス・ドラマチックな光）", "12. 音楽アーティスト系（MV風・グランジ・エモい）",
    # アート・表現
    "13. レトロ・ヴィンテージ系（色褪せ・ノイズ・昭和/アメリカーナ）", "14. ポップアート系（ビビッド・網点・アメコミ風）", "15. サイバーパンク系（ネオン・暗闇・メカニカル）", "16. スチームパンク系（真鍮・歯車・ビクトリア朝）",
    "17. 和風系（浮世絵・和柄・墨絵風）", "18. 水彩画系（にじみ・透明感・優しいタッチ）", "19. 油絵系（厚塗り・重厚感・筆跡）", "20. 3D・クレイアニメ系（粘土・立体感・温かみ）",
    # その他
    "21. 季節・イベント系（春夏秋冬・行事）", "22. ホラー・ダーク系（不気味・コントラスト強・不安感）", "23. 添付画像から分析（AIにおまかせ）", "24. その他（自由入力）"
]

sub_tastes = [
    "指定なし（標準）",
    # UI/デザイン系
    "1. モダンUI系（グラスモーフィズム・ニューモーフィズム）", "2. マテリアルデザイン系（影・階層構造・はっきりした色）", "3. フラットデザイン系（影なし・ベタ塗り・アイコン化）", "4. スイス・スタイル系（グリッド・巨大なタイポグラフィ・大胆な余白）",
    # 質感・素材系
    "5. ノート・紙面デザイン系（罫線・紙のテクスチャ・手書き文字）", "6. クラフト・切り絵系（紙の重なり・アナログ感・影の落ち方）", "7. ザラザラ・グリッチ系（ノイズ・バグ表現・VHS風）", "8. メタリック・光沢系（金属の反射・ツヤ・ラグジュアリー）",
    # 雰囲気・情景系
    "9. ミニマル・余白重視系（究極まで情報を削ぎ落とす）", "10. 北欧デザイン系（くすみカラー・有機的な形・温もり）", "11. 白黒タイポグラフィ系（文字だけで魅せる・力強さ）", "12. 余白×写真引き立て系（メインビジュアルを最高に目立たせる）",
    "13. ネオンサイン系（暗闇に光る管・サイバー・夜の街）", "14. ヴェイパーウェイヴ系（ピンク＆水色・彫像・レトロPC）", "15. ローファイ・チル系（ノスタルジー・少しぼやけた輪郭・夕暮れ）", "その他（自由入力）"
]

structures_thumbnail = [
    # サムネイル・広告向け
    "1. 左右分割（左: テキスト / 右: 画像）", "2. 左右分割（左: 画像 / 右: テキスト）",
    "3. 上下分割（上: 画像 / 下: テキスト）", "4. 上下分割（上: テキスト / 下: 画像）",
    "5. 中央配置（シンプルで強いメッセージ）", "6. Zの法則（視線を左上から右下へ誘導）",
    "7. 全面タイポグラフィ（文字をデザインの一部として強調）", "8. フレーム囲み（中央への集中効果）", "9. 対角線・斜め分割（躍動感・スピード感）"
]

structures_diagram = [
    # 論理・整理系
    "8. フロー・ステップ系（手順、流れ、1→2→3）", "9. 比較系（AとB、ビフォーアフター、VS）", "10. リスト・箇条書き系（並列、ポイント一覧）",
    "11. マトリクス系（2軸で4分割、ポジショニング）", "12. サイクル・循環系（ぐるぐる回る、PDCAなど）", "13. ピラミッド・階層系（上下関係、重要度順）",
    "14. 中心放射系（真ん中から広がる、マインドマップ風）", "15. タイムライン系（時系列、年表、過去→未来）", "16. ベン図・交差系（共通項目・重なり合う要素）",
    # 抽象・コンセプチュアル系
    "17. 氷山モデル（見えている部分と隠れた本質）", "18. 天秤・バランス系（2つの要素の釣り合い・葛藤）", "19. パズル・ピース系（欠けたピースがピタッとハマる瞬間）",
    "20. 迷路・ゴール系（複雑な道筋から正解を見つける）", "21. 扉・アンベール系（新しい世界が開かれる・ベールを脱ぐ）", "22. その他（自由入力）"
]

lighting_styles = [
    "指定なし（標準）", "1. おまかせ（テイストに合わせる）", "2. スタジオ照明（柔らかく均一な光・商品撮影風）", "3. ドラマチック（強いコントラスト・深い影・印象的）",
    "4. バックライト・逆光（後光が差す・シルエット強調・神々しさ）", "5. ネオン・サイバー光（発光体・カラフルなハイライト）", "6. シネマティック（映画のような色温度・時間帯の表現）",
    "7. ゴールデンアワー（夕暮れの暖かで柔らかい黄金色の光）", "8. ブルーアワー（夜明け前の冷たく静寂な青い光）", "9. スポットライト（主題を一筋の光で照らし出す・舞台風）"
]

camera_angles = [
    "指定なし（標準）", "1. おまかせ（構造に合わせる）", "2. アイレベル（人間の目線の高さ・親しみやすさ）", "3. ハイアングル（上から見下ろす・全体像の把握・可愛らしさ）",
    "4. ローアングル（下から見上げる・巨大さ・権威・迫力）", "5. 俯瞰・鳥瞰図（真上から見下ろす・マップ風・情報の網羅）", "6. 魚眼レンズ（中央が歪んで強調される・ダイナミック）",
    "7. マクロ・クローズアップ（極端に近づく・質感の強調・一部の切り取り）", "8. ダッチアングル（カメラを傾ける・不安感・躍動感・狂気）", "9. アイソメトリック（斜め上から見下ろす・ゲーム風・箱庭感）"
]

emotion_colors = [
    "指定なし（標準）", "1. 信頼・誠実・知的（ブルー系×グレー・白）", "2. 情熱・緊急・エネルギー（レッド系×黒・白）", 
    "3. 親しみ・温もり・安心（オレンジ系×ブラウン）", "4. 先進的・サイバー・未来（ネオン×暗黒背景）",
    "5. 高級感・ラグジュアリー（ゴールド・シルバー×黒）", "6. エコ・自然・癒やし（グリーン系×アースカラー）",
    "7. エレガント・優しさ（ピンク系・パステルカラー）", "8. 恐怖・ミステリアス（ダークパープル・深い青×黒）"
]

font_styles = [
    "指定なし（標準）", 
    "1. おまかせ（テイストに合わせる）", 
    "2. ゴシック体・サンセリフ（モダン・力強い・視認性高）", 
    "3. 特太ゴシック・インパクト（YouTuber風・目立たせたい文字）", 
    "4. 明朝体・セリフ（高級感・知的・伝統的）", 
    "5. 繊細な細ゴシック（洗練・ミニマル・美容系）",
    "6. 丸ゴシック（親しみやすい・ポップ・柔らかい）", 
    "7. 手書き風・マーカー風（パーソナル・エモい・温もり）",
    "8. 筆文字・行書体（和風・勢い・迫力・歴史）", 
    "9. ピクセル・レトロ（ゲーム風・サイバー・8bit）",
    "10. チョーク文字・黒板風（カフェ・オーガニック・手作り感）",
    "11. ネオン管風・アクリル文字（夜の街・サイバーパンク・近未来）",
    "12. 3D立体文字・メタリック（ゲームタイトル風・重厚感・派手）",
    "13. 雑誌風見出し・タイポグラフィ（ファッション誌・エディトリアル）",
    "14. 筆記体・カリグラフィー（おしゃれ・英字ロゴ風・エレガント）",
    "15. デザイン書体（個性的・尖った印象・タイトル向き）",
    "その他（自由入力）"
]

target_genres = [
    "指定なし（標準）",
    "1. 美容・コスメ（透明感・洗練・女性向け）",
    "2. 健康・ダイエット（爽やか・エネルギッシュ・清潔感）",
    "3. 恋愛・婚活（エモーショナル・温かみ・ピンク系）",
    "4. 育児・ファミリー（優しい・柔らかい・親しみ）",
    "5. スピリチュアル・占い（神秘的・宇宙・紫やゴールド系）",
    "6. マネー・投資（知的・信頼・図解多め）",
    "7. ビジネス・自己啓発（スタイリッシュ・説得力・シャープ）",
    "8. エンタメ・ゲーム（ポップ・派手・コントラスト強）",
    "9. 料理・グルメ（シズル感・温かみ・食欲促進）",
    "10. 旅行・Vlog（エモい・風景美・シネマティック）",
    "11. ガジェット・テック（近未来的・クール・無機質）",
    "12. ペット・動物（かわいい・もふもふ・癒やし）",
    "13. ハンドメイド・DIY（ナチュラル・手作り感・クラフト）",
    "14. ファッション・アパレル（トレンド・抜け感・雑誌風）",
    "15. 不動産・インテリア（清潔感・広さ・ライフスタイル）",
    "16. 語学・教育（ポップ・分かりやすい・親しみやすさ）",
    "17. スポーツ・フィットネス（躍動感・力強さ・爽快感）",
    "18. メンタルヘルス・心理（安心感・マインドフルネス・癒やし）",
    "19. ヨガ・ピラティス（リラックス・しなやかさ・オーガニック）",
    "その他（自由入力）"
]

# --- セッションステートのクリーンアップ（選択肢追加に伴うクラッシュ防止） ---
for state_key, option_list in [
    ("sel_font_style", font_styles),
    ("sel_genre", target_genres),
    ("sel_use_case", use_cases),
    ("sel_ratio", aspect_ratios)
]:
    if state_key in st.session_state and st.session_state[state_key] not in option_list:
        del st.session_state[state_key]

st.header("1. 作りたい画像の設定")

# --- テンプレート呼び出し ---
with st.expander("📁 マイテンプレートからロード", expanded=False):
    my_templates = st.session_state.my_templates
    if not my_templates:
        st.write("保存されているテンプレートはありません。（プロンプト生成後に下部から保存できます）")
    else:
        template_names = ["-- 選択してください --"] + [t["template_name"] for t in my_templates]
        selected_template_name = st.selectbox("読み込むテンプレートを選択:", template_names)
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            apply_clicked = st.button("テンプレートを適用する", use_container_width=True)
        with col_btn2:
            delete_clicked = st.button("🗑️ このテンプレートを削除", type="secondary", use_container_width=True)
            
        if apply_clicked:
            if selected_template_name != "-- 選択してください --":
                # Find the template
                selected_t = next((t for t in my_templates if t["template_name"] == selected_template_name), None)
                if selected_t and "raw_ui_state" in selected_t:
                    raw_state = selected_t["raw_ui_state"]
                    # Update session state for all keys saved in the raw_ui_state
                    for k, v in raw_state.items():
                        if k == "input_contents_raw":
                            # We need to set the dynamic text area keys based on this payload
                            for slide in v:
                                idx = slide["slide_number"] - 1
                                if "lead_text" in slide:
                                    st.session_state[f"lead_{idx}"] = slide["lead_text"]
                                    st.session_state[f"title_{idx}"] = slide["main_title"]
                                    st.session_state[f"highlight_{idx}"] = slide["highlight_text"]
                                    st.session_state[f"sub_{idx}"] = slide["sub_text"]
                                else:
                                    st.session_state[f"title_{idx}"] = slide["title"]
                                    st.session_state[f"details_{idx}"] = slide["details"]
                        else:
                            st.session_state[k] = v
                            if k == "num_slides_input":
                                st.session_state["num_slides_input_alt"] = v
                    st.success(f"'{selected_template_name}' の設定をすべて復元しました！🍌✨")
                elif selected_t:
                    st.warning("このテンプレートは古い形式のため、画面への自動入力機能はサポートされていません。")
            else:
                st.warning("適用するテンプレートを選択してください。")
                
        elif delete_clicked:
            if selected_template_name != "-- 選択してください --":
                st.session_state.my_templates = [t for t in my_templates if t["template_name"] != selected_template_name]
                save_templates(st.session_state.my_templates)
                st.success(f"'{selected_template_name}' を削除しました！")
                st.rerun()
            else:
                st.warning("削除するテンプレートを選択してください。")

col0, col1, col2 = st.columns(3)
with col0:
    sel_use_case = st.selectbox("用途", use_cases, key="sel_use_case")
with col1:
    sel_ratio = st.selectbox("キャンバス比率", aspect_ratios, key="sel_ratio")
with col2:
    slide_counts = ["1枚（単一画像）", "2〜4枚（ショートカルーセル）", "5〜10枚（ロングカルーセル）"]
    sel_count = st.selectbox("出力枚数", slide_counts, key="sel_count")

sel_genre = st.selectbox("ターゲットジャンル・世界観", target_genres, key="sel_genre")
custom_genre = ""
if "その他" in sel_genre:
    custom_genre = st.text_input("任意のジャンル", key="custom_genre")

st.header("2. 伝える内容と被写体")
num_slides = 1
num_slides_selected = False

if "2〜4枚" in sel_count:
    num_slides_input = st.selectbox("作成するスライドの正確な枚数", ["", "2", "3", "4"], key="num_slides_input")
    if num_slides_input:
        num_slides = int(num_slides_input)
        num_slides_selected = True
elif "5〜10枚" in sel_count:
    num_slides_input = st.selectbox("作成するスライドの正確な枚数", ["", "5", "6", "7", "8", "9", "10"], key="num_slides_input_alt")
    if num_slides_input:
        num_slides = int(num_slides_input)
        num_slides_selected = True
else:
    num_slides_selected = True

input_contents = []
if not num_slides_selected:
    st.info("💡 スライドの正確な枚数を選択してください。指定した枚数分のテキスト入力欄が出現します。")
else:
    st.markdown(f"**【 {num_slides} 枚分のテキスト入力】**")
    for i in range(num_slides):
        with st.container(border=True):
            st.markdown(f"**■ {i+1}枚目**")
            
            if "サムネイル" in sel_use_case:
                lead = st.text_area(f"{i+1}枚目のリード文", value="", placeholder=f"【超重要】", height=68, key=f"lead_{i}")
                title = st.text_area(f"{i+1}枚目のタイトル", value="", placeholder=f"ファン化は才能じゃない", height=68, key=f"title_{i}")
                highlight = st.text_area(f"{i+1}枚目のハイライト（強調文字）", value="", placeholder=f"100万回読まれた", height=68, key=f"highlight_{i}")
                sub = st.text_area(f"{i+1}枚目のサブテキスト", value="", placeholder=f"今すぐ使える3つの思考法", height=68, key=f"sub_{i}")
                
                input_contents.append({
                    "slide_number": i+1,
                    "lead_text": lead,
                    "main_title": title,
                    "highlight_text": highlight,
                    "sub_text": sub
                })
            else:
                title = st.text_area(f"{i+1}枚目のタイトル・見出し", value="", placeholder=f"タイトル例 {i+1}", height=68, key=f"title_{i}")
                details = st.text_area(f"{i+1}枚目の具体的なテキスト", value="", placeholder=f"詳細テキスト例 {i+1}...", height=80, key=f"details_{i}")
                
                input_contents.append({
                    "slide_number": i+1, 
                    "title": title, 
                    "details": details
                })

sel_char_usage = st.selectbox("メインの被写体（キャラクター）", char_usages, key="sel_char_usage")
if sel_char_usage == "自分のキャラクターを使う（画像アップロード）":
    st.info("💡 **重要:** 生成プロンプトをAI（Gemini等）に入力する際に、**使いたいキャラクター画像を忘れずに添付**してください。")
    uploaded_char_image = st.file_uploader("キャラクター画像をアップロード（AIへのプロンプト指示用）", type=["png", "jpg", "jpeg", "webp"])

st.header("3. デザインの方向性")
col3, col4 = st.columns(2)
with col3:
    if "サムネイル" in sel_use_case:
        current_structures = structures_thumbnail
    elif "図解" in sel_use_case:
        current_structures = structures_diagram
    else:
        current_structures = structures_thumbnail + structures_diagram
        
    sel_structure = st.selectbox("図解・構図の構造", current_structures, key="sel_structure")
    custom_structure = ""
    if "その他" in sel_structure:
        custom_structure = st.text_input("任意の構造", key="custom_structure")
with col4:
    sel_main_taste = st.selectbox("メインテイスト（画風）", main_tastes, key="sel_main_taste")
    custom_main = ""
    if "その他" in sel_main_taste:
        custom_main = st.text_input("任意のメインテイスト", key="custom_main")

# --- 出力モードの選択 (複数枚の時のみ表示) ---
sel_output_mode = "1枚のみ生成"
if "1枚" not in sel_count:
    st.markdown("##### 複数枚の出力形式")
    sel_output_mode = st.radio(
        "複数枚のフォーマット",
        ["個別に複数枚出力（カルーセル等）", "1枚の画像に分割してまとめて出力（グリッド等）"],
        horizontal=True,
        label_visibility="collapsed",
        key="sel_output_mode"
    )

with st.expander("⚙️ 詳細設定（プロ向け・こだわりたい方へ）", expanded=False):
    st.markdown("さらに細かくデザインを指定したい場合のオプションです。（入力しなくても綺麗な画像は作成できます）")
    
    sel_sub_taste = st.selectbox("サブテイスト", sub_tastes, key="sel_sub_taste")
    custom_sub = ""
    if "その他" in sel_sub_taste:
        custom_sub = st.text_input("任意のサブテイスト", key="custom_sub")
        
    sel_char_pos = st.selectbox("キャラクターの配置位置・アクション", char_positions, key="sel_char_pos")
    
    sel_lighting = st.selectbox("ライティング（照明・光の演出）", lighting_styles, key="sel_lighting")
    sel_camera = st.selectbox("カメラアングル・構図", camera_angles, key="sel_camera")
    
    sel_emotion_color = st.selectbox("ターゲットに与えたい印象（感情カラーパレット）", emotion_colors, key="sel_emotion_color")
    sel_font_style = st.selectbox("フォント・タイポグラフィ（文字の書体）", font_styles, key="sel_font_style")
    
    input_additional_details = st.text_area("そのほか細かい指示があれば（任意）", placeholder="例: 背景は白、文字は黒メイン、アイコンは3Dで", height=60, key="input_additional_details")
    input_avoid = st.text_area("避けたい要素（任意）", placeholder="例: カラフルすぎる装飾、PowerPoint風レイアウト", height=60, key="input_avoid")

submitted = st.button("オリジナル・プロンプトを錬成する 🍌", use_container_width=True, type="primary")

if submitted:
    if not num_slides_selected:
        st.error("⚠️ まずは「スライドの正確な枚数」を選択してください。")
        st.stop()
        
    final_main_taste = custom_main if "その他" in sel_main_taste and custom_main else sel_main_taste.split("（")[0].split(". ")[-1]
    final_sub_taste = custom_sub if "その他" in sel_sub_taste and custom_sub else sel_sub_taste.split("（")[0].split(". ")[-1]
    final_structure = custom_structure if "その他" in sel_structure and custom_structure else sel_structure.split("（")[0].split(". ")[-1]
    final_genre = custom_genre if "その他" in sel_genre and custom_genre else sel_genre.split("（")[0].split(". ")[-1]
    final_char_pos = sel_char_pos.split("（")[0].split(". ")[-1]
    final_lighting = sel_lighting.split("（")[0].split(". ")[-1]
    final_camera = sel_camera.split("（")[0].split(". ")[-1]
    final_ratio = sel_ratio.split("（")[0]
    
    char_instruction = ""
    if "入れない" in sel_char_usage:
        char_info = "None"
    elif "自分のキャラクターを使う" in sel_char_usage:
        if uploaded_char_image is not None:
            char_info = "Use uploaded character image"
            char_instruction = (
                "An image of the character is attached. STRICTLY MAINTAIN AND REPRODUCE the character's physical appearance, facial features, and clothing. EXTREME CHANGES TO THE CHARACTER'S DESIGN ARE STRICTLY PROHIBITED. "
                "However, you MUST flexibly change the character's 'pose' and 'facial expression' to perfectly match the context, emotion, and composition of the requested scene. "
                "Place this character optimally into the generated world, adapting only the lighting, shading, and artistic texture to blend naturally with the specified style."
            )
        else:
            char_info = "Image missing warning"
            char_instruction = (
                "CRITICAL RULE: The user selected to use their own character, but FORGOT to attach an image. "
                "DO NOT generate any image. Instead, you must only reply with the exact phrase: '添付画像を添付し忘れてませんか？'."
            )

    count_instruction = ""
    # 選択された正確な枚数をプロンプトに反映（未選択の場合は処理をブロックするか範囲文字列を渡す）
    output_count_str = f"{num_slides}" if "1枚" not in sel_count and num_slides_selected else sel_count.split('（')[0]
    output_format_mode = "1 single image"
    
    if "1枚" not in sel_count:
        if "個別" in sel_output_mode:
            count_instruction = (
                f"=== CRITICAL INTERACTIVE MODE PROTOCOL ({output_count_str} IMAGES TOTAL) ===\n"
                f"You MUST generate EXACTLY {output_count_str} images in sequence, BUT YOU MUST NEVER GENERATE THEM ALL AT ONCE.\n"
                "You are bound by the following STRICT step-by-step rules:\n"
                "1. Understand the full request, but DO NOT GENERATE ANYTHING YET.\n"
                "2. First, reply with: 'ご依頼の内容を理解しました。世界観を統一して1枚目から作成しますか？' (I understand the request. Shall I create the first image with a consistent world-building?).\n"
                "3. WAIT for the user to reply 'はい' (Yes).\n"
                "4. Once the user says yes, GENERATE ONLY IMAGE 1 using your image generation tool. STOP IMMEDIATELY after Image 1 is displayed.\n"
                "5. Ask the user: '問題なければ、次の画像を生成しますか？' (If there are no issues, shall we generate the next image?).\n"
                "6. WAIT for the user to reply 'はい' (Yes) or request changes.\n"
                "7. If requested, fix the image. If 'Yes', GENERATE ONLY THE NEXT IMAGE.\n"
                "8. Repeat steps 5-7 strictly one-by-one until all images are done. ABSOLUTE CONSISTENCY in character, style, and lighting is required across all images."
            )
            output_format_mode = f"Strict Interactive 1-by-1 Generation (Total: {output_count_str} images)"
        else:
            count_instruction = f"Output all {output_count_str} scenes combined into a single unified image layout (e.g., divided into a grid, split panels, or a cohesive single canvas)."
            output_format_mode = f"1 combined image containing {output_count_str} panels/sections"

    # --- プロンプト組み立て補助関数 ---
    def format_optional_line(label, value):
        if not value or "指定なし" in value:
            return ""
        return f"- {label}: {value}\n"

    # --- プロンプト構築 (JSONフォーマット) ---
    import json
    
    design_concept = {
        "overall_vibe_and_genre": final_genre,
        "style": f"{final_main_taste} > {final_sub_taste}" if "指定なし" not in final_sub_taste else final_main_taste,
        "composition_structure": final_structure
    }
    if "指定なし" not in final_camera:
        design_concept["camera_angle"] = final_camera
    if "指定なし" not in final_lighting:
        design_concept["lighting"] = final_lighting
    if "指定なし" not in sel_emotion_color:
        design_concept["emotional_color_palette"] = sel_emotion_color.split("（")[0].split(". ")[-1]
    if "指定なし" not in sel_font_style:
        design_concept["typography_style"] = sel_font_style.split("（")[0].split(". ")[-1]
    if input_additional_details:
        design_concept["additional_details"] = input_additional_details
    if input_avoid:
        design_concept["avoid_elements"] = input_avoid
        
    character_setting = {
        "usage": char_info
    }
    if "指定なし" not in final_char_pos and char_info != "None":
        character_setting["position_and_action"] = final_char_pos
    if char_instruction:
        character_setting["instructions"] = char_instruction
        
    format_setting = {
        "use_case": sel_use_case.split("（")[0],
        "aspect_ratio": final_ratio,
        "output_format": output_format_mode
    }
    if count_instruction:
        format_setting["carousel_instructions"] = count_instruction
        
    prompt_dict = {
        "role": "Exclusive AI Creative Director",
        "objective": "Generate a highly engaging, professional, and visually stunning image.",
        "format": format_setting,
        "design_concept": design_concept,
        "content_list": input_contents,
        "character": character_setting,
        "execution_rules": [
            "ULTRA HIGH RESOLUTION & RENDER QUALITY: Generate the final image in pristine 4K or 8K resolution. Ensure hyper-detailed textures, anti-aliased clean edges, and absolute clarity across the entire canvas.",
            "Prioritize text readability.",
            "Maximize the appeal of the specified style, structure, angle, and lighting.",
            "RESPECT USER INPUT: The text provided in 'details' must be prioritized and used as the primary content. Only make minor, supplementary copywriting adjustments to fit the design layout. Do NOT completely rewrite the user's input.",
            "PREVENT TEXT CORRUPTION & UNAUTHORIZED TRANSLATION: You MUST NOT generate garbled text, gibberish, or hallucinated characters. Furthermore, if the user input is in Japanese, DO NOT automatically translate it into English unless explicitly requested. Maintain the original language with perfect typographical accuracy.",
            "TONE RESTRICTION: The text MUST NOT sound like it was generated by AI. Avoid clichés, overly formal academic tones, or generic AI buzzwords.",
            "APPLY RESPONSIVE DESIGN PRINCIPLES: The composition must be flexible, ensuring key elements remain fully legible across different screen sizes and aspect ratios without being cropped.",
            "APPLY COMPOSITIONAL GRID: Strictly utilize the Rule of Thirds or Golden Ratio to place the main subject and focal points for maximum visual impact and structural balance.",
            "APPLY THE 4 DESIGN PRINCIPLES: 1. Proximity (Group related elements), 2. Alignment (Align edges for high visibility), 3. Repetition (Repeat design traits for consistency), 4. Contrast (Create clear visual hierarchy).",
            "APPLY COLOR THEORY: Ensure color scheme matches the purpose and target audience, considering hue, value, and saturation.",
            "APPLY TYPOGRAPHY: Focus on font selection and kerning to maximize readability and aesthetics.",
            "CRITICAL TYPOGRAPHY RULE: If a specific typography style is requested in the design_concept, you MUST STRICTLY execute and feature that exact font style (e.g., Mincho, Gothic, Handwritten, Pixel). DO NOT substitute it.",
            "APPLY LAYOUT & WHITESPACE: Master the spatial arrangement to control the flow of information and elevate the overall quality.",
            "SOLVE PROBLEMS VIA DESIGN: Construct the image to solve visual communication challenges, focusing on user empathy.",
            "NEGATIVE PROMPT (PROHIBITED ELEMENTS): Under NO circumstances should you include cheap 3D corporate art styles, floating random geometric objects, excessive lens flares, unnatural glowing silhouettes, or generic stock-photo aesthetics. Ensure a highly realistic, refined, and professional finish.",
            "CRITICAL EXCEPTION HANDLING: If multiple images are requested, you MUST process and output them reliably without memory errors or cutting out early. Output each prompt request completely separately before moving to the next.",
            "CRITICAL PROHIBITION: NEVER include the text 'Nano Banana', 'NANO BANANA PRO', 'ナノバナナ', or any variation of the tool name within the generated image or textual output under any circumstances."
        ]
    }
        
    final_prompt = json.dumps(prompt_dict, ensure_ascii=False, indent=2)

    # --- UIの生データを保存（テンプレート復元用） ---
    raw_ui_state = {
        "sel_use_case": sel_use_case,
        "sel_ratio": sel_ratio,
        "sel_count": sel_count,
        "sel_genre": sel_genre,
        "custom_genre": custom_genre,
        "sel_char_usage": sel_char_usage,
        "sel_structure": sel_structure,
        "custom_structure": custom_structure,
        "sel_main_taste": sel_main_taste,
        "custom_main": custom_main,
        "sel_output_mode": sel_output_mode,
        "sel_sub_taste": sel_sub_taste,
        "custom_sub": custom_sub,
        "sel_char_pos": sel_char_pos,
        "sel_lighting": sel_lighting,
        "sel_camera": sel_camera,
        "sel_emotion_color": sel_emotion_color,
        "sel_font_style": sel_font_style,
        "input_additional_details": input_additional_details,
        "input_avoid": input_avoid,
        "num_slides_input": num_slides_input if "1枚" not in sel_count else ""
    }
    # スライド内容も生の入力値として保存
    raw_ui_state["input_contents_raw"] = input_contents

    # 生成した内容をセッションステートに保持して、リロード後も保存ボタンが消えないようにする
    st.session_state.current_generated_prompt = prompt_dict
    st.session_state.current_final_prompt_json = final_prompt
    st.session_state.current_use_case = sel_use_case
    st.session_state.current_main_taste = final_main_taste
    st.session_state.current_raw_ui_state = raw_ui_state

# --- テンプレート保存機能 (submittedブロックの外に配置して再描画時の消失を防ぐ) ---
if "current_generated_prompt" in st.session_state:
    st.markdown("---")
    
    st.success("✨ **あなただけのオリジナルプロンプトが完成しました！**")
    st.code(st.session_state.current_final_prompt_json.strip(), language="json")
    
    st.markdown("---")
    
    with st.expander("💾 この設定をマイテンプレートに保存（最大20個まで）", expanded=False):
        template_name = st.text_input("テンプレート名を入力してください", placeholder="例：YouTube汎用サムネ（教育系）", key="save_template_name")
        if st.button("テンプレートを保存する"):
            if not template_name:
                st.warning("テンプレート名を入力してください。")
            else:
                if len(st.session_state.my_templates) >= 20:
                    st.error("保存できるテンプレートは最大20個までです。ページ上部の「マイテンプレートからロード」メニューから不要なテンプレートを選択し、削除してください。")
                else:
                    new_template = {
                        "template_name": template_name,
                        "timestamp": time.time(),
                        "prompt_data": st.session_state.current_generated_prompt,
                        "raw_ui_state": st.session_state.current_raw_ui_state
                    }
                    st.session_state.my_templates.append(new_template)
                    save_templates(st.session_state.my_templates)
                    st.success(f"テンプレート「{template_name}」を保存しました！ページ上部から呼び出せます。")
                    
                    
