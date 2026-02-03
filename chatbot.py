from chatbotweb.chat_server import ChatServer
import random
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter

class MyChatClass():
    BOT_NAME = "F-BOT"
    html = None

class UserClass():
    # ----- 設定定数 -----
    REVERSE_QUESTION_PROB = 0.7   # 逆質問の出現確率
    KEYWORD_FULL_SCORE = 3         # 完全一致時の加点
    KEYWORD_PART_SCORE = 1         # 部分一致時の加点
    REVERSE_KEYWORD_SCORE = 3      # 逆質問で選択した場合の加点
    REVERSE_KEYWORD_NEG = 2        # 興味なし選択時の減点
    RECOMMEND_DIFF = 2             # 推薦判定の上位1位と2位の点差

    def __init__(self, chat_obj):
        self.chat_obj = chat_obj

        # 研究室辞書
        self.labs = {
            "数値計算研究室": [
                "相島 健助",
                [
                    "数値計算","シミュレーション","コンピュータハードウェア",
                    "スーパーコンピュータ", "分散システム","情報検索・サーチエンジン",
                    "アルゴリズム・計算理論","人工知能", "AI", "機械学習",
                    "画像処理", "コンピュータビジョン","音声処理・音楽情報処理",
                    "自然言語処理", "テキストマイニング","データサイエンス","コンピュータ",
                    "計算","数値計算","数理モデル","シミュレーション","スーパーコンピュータ","数学"
                ]
            ],

            "情報編纂研究室": [
                "赤石 美奈",
                [
                    "情報検索・サーチエンジン","データベース・知識処理基盤",
                    "人工知能", "AI", "機械学習","自然言語処理・テキストマイニング",
                    "可視化","データサイエンス","情報システム","情報編纂",
                    "知識化社会","情報圧縮技術","創造活動支援","情報","システム"
                ]
            ],

            "情報セキュリティ研究室": [
                "尾花 賢",
                [
                    "符号", "情報理論","セキュリティ", "暗号技術","OS", "ネットワーク技術",
                    "ユビキタスコンピューティング", "IoT","コンピュータ","情報","暗号",
                    "データ","数学","通信","安全"
                ]
            ],

            "プログラミング言語研究室": [
                "佐々木 晃",
                [
                    "プログラミング言語","数値計算", "シミュレーション","ソフトウェア工学",
                    "OS", "ネットワーク技術","ヒューマンコンピュータインタラクション",
                    "可視化","コンピュータ","プログラミング","情報","言語","ドメイン","特化言語"
                ]
            ],

            "知的進化システム研究室": [
                "佐藤 裕二",
                [
                    "人工知能", "AI", "機械学習","スーパーコンピュータ・分散システム","Webシステム",
                    "情報検索・サーチエンジン","データベース", "知識処理基盤",
                    "アルゴリズム・計算理論","ヒューマンコンピュータインタラクション",
                    "データサイエンス","コンピュータ","情報システム","ソフトコンピューティング",
                    "進化計算","機械学習","強化学習","ニューラルネット","最適化","群知能","検索"
                ]
            ],

            "アルゴリズム設計論研究室": [
                "首藤 裕一",
                [
                    "アルゴリズム・計算理論","人工知能", "AI", "機械学習","セキュリティ", "暗号技術",
                    "OS", "ネットワーク技術","コンピュータ","計算機","分散処理","理論計算機科学"
                ]
            ],

            "基盤ソフトウェア研究室": [
                "日高 宗一郎",
                [
                    "プログラミング言語","ソフトウェア工学","Webシステム",
                    "データベース・知識処理基盤","コンピュータ","基盤","ソフトウエア",
                    "プログラム","双方向変換","プログラミング","システム","プログラム変換"
                ]
            ],

            "分散システム研究室": [
                "廣津 登志夫",
                [
                    "OS", "ネットワーク技術","ユビキタスコンピューティング・IoT",
                    "スーパーコンピュータ", "分散システム","数値計算", "シミュレーション",
                    "セキュリティ", "暗号技術","Webシステム","コンピュータ","分散",
                    "システム","ソフトウエア","クラウド","情報","情報処理","ネットワーク"
                ]
            ],

            "人工知能研究室": [
                "黄 潤和",
                [
                    "人工知能", "AI", "機械学習","ユビキタスコンピューティング・IoT",
                    "Webシステム","情報検索・サーチエンジン","パターン認識",
                    "自然言語処理・テキストマイニング","システム","情報","自動","データ","サービス"
                ]
            ],

            "コンピュータアーキテクチャ研究室": [
                "李 亜民",
                [
                    "コンピュータハードウェア","スーパーコンピュータ", "分散システム",
                    "プログラミング言語","OS", "ネットワーク技術","グラフィックス", "アニメーション",
                    "アーキテクチャ","設計思想","集積回路","ソフトウェア","システム"
                ]
            ],

            "音・言語メディア研究室": [
                "伊藤 克亘",
                [
                    "パターン認識","音声処理・音楽情報処理","自然言語処理・テキストマイニング",
                    "数値計算・シミュレーション","情報検索・サーチエンジン","人工知能", "AI", "機械学習",
                    "ヒューマンコンピュータインタラクション","仮想現実", "VR", "拡張現実", "AR",
                    "可視化","データサイエンス","メディア","言語","音","ことば",
                    "コンピュータ","楽器","音声","音声認識","歌声","声優","裏声",
                    "演奏","能","能楽","音楽","1/f", "ゆらぎ","編曲","アレンジ"
                ]
            ],

            "量子コンピュータ研究室": [
                "川畑 史郎",
                [
                    "量子コンピュータ","数値計算・シミュレーション","アルゴリズム・計算理論",
                    "コンピュータハードウェア","符号・情報理論","プログラミング言語",
                    "セキュリティ・暗号技術","人工知能", "AI", "機械学習","データサイエンス",
                    "最適化","量子情報理論","量子アニーリング","量子情報処理",
                    "量子力学","量子アルゴリズム","計算物理","量子エラー訂正","超伝導", "量子"
                ]
            ],

            "実世界指向メディア研究室": [
                "小池 崇文",
                [
                    "仮想現実", "VR", "拡張現実", "AR","グラフィックス・アニメーション",
                    "画像処理・コンピュータビジョン","数値計算・シミュレーション",
                    "人工知能", "AI", "機械学習","ユビキタスコンピューティング・IoT",
                    "ヒューマンコンピュータインタラクション","可視化","パターン認識",
                    "データサイエンス","メディア","実世界指向","３次元","コンピュータ・グラフィックス",
                    "画像","画像認識","拡張現実","CG","映像","ソフトウェア","ハードウェア"
                ]
            ],

            "高次元データモデリング研究室": [
                "小西 克巳",
                [
                    "アルゴリズム・計算理論","人工知能", "AI", "機械学習","画像処理", "コンピュータビジョン",
                    "データサイエンス","数値計算", "シミュレーション","パターン認識",
                    "音声処理", "音楽情報処理","メディア","高次元データ","モデリング",
                    "情報化社会","数学モデル","データ","ビッグデータ","画像","映像","音声","生体情報"
                ]
            ],

            "コンピュータグラフィックス研究室": [
                "佐藤 周平",
                [
                    "数値計算", "シミュレーション","人工知能", "AI", "機械学習",
                    "グラフィックス", "アニメーション","画像処理", "コンピュータビジョン",
                    "仮想現実", "VR", "拡張現実", "AR","可視化","パターン認識",
                    "音声処理・音楽情報処理","データサイエンス","コンピュータ","画像"
                ]
            ],

            "計算物理研究室": [
                "善甫 康成",
                [
                    "スーパーコンピュータ", "分散システム","数値計算", "シミュレーション",
                    "プログラミング言語","アルゴリズム・計算理論","データサイエンス",
                    "メディア","計算物理","スーパーコンピュータ","第一原理計算",
                    "並列計算","材料","物性","科学","時系列解析","光"
                ]
            ],

            "メディア情報処理研究室": [
                "高村 誠之",
                [
                    "数値計算", "シミュレーション","符号・情報理論","画像処理", "コンピュータビジョン",
                    "人工知能", "AI", "機械学習","パターン認識","データサイエンス","メディア",
                    "情報処理","符号化","画像","映像","点群信号","マルチモーダル信号",
                    "撮像","光学"
                ]
            ],

            "多次元画像処理研究室": [
                "花泉 弘",
                [
                    "パターン認識","画像処理・コンピュータビジョン","可視化","データサイエンス",
                    "メディア","多次元画像","画像","画像処理","医療","自動車","衛星",
                    "衛星画像","個人認証","カメラ","医療画像"
                ]
            ],

            "サービスシステム研究室": [
                "藤田 悟",
                [
                    "Webシステム","人工知能", "AI", "機械学習","ユビキタスコンピューティング・IoT",
                    "数値計算・シミュレーション","情報検索・サーチエンジン",
                    "データベース・知識処理基盤","仮想現実", "VR", "拡張現実", "AR",
                    "データサイエンス","情報システム","サービス","システム","スマートフォン",
                    "3次元カメラ","3次元プリンタ","カメラ","プリンタ","情報","データ"
                ]
            ],

            "ユーザインタフェース研究室": [
                "細部 博史",
                [
                    "プログラミング言語","ヒューマンコンピュータインタラクション",
                    "可視化","Webシステム","データベース・知識処理基盤",
                    "人工知能", "AI", "機械学習","グラフィックス", "アニメーション",
                    "データサイエンス","情報システム","ユーザインタフェース","インタフェース",
                    "コンピュータ","システム","HCI","UI","プログラミング","ソフトウェア"
                ]
            ],

            "ユビキタスコンピューティング研究室": [
                "馬 建華",
                [
                    "人工知能", "AI", "機械学習","ユビキタスコンピューティング・IoT",
                    "ヒューマンコンピュータインタラクション","OS・ネットワーク技術",
                    "Webシステム","情報検索・サーチエンジン","可視化","パターン認識",
                    "自然言語処理", "テキストマイニング","データサイエンス","情報システム",
                    "アプリ","アプリケーション","情報処理"
                ]
            ]
        }

        self.scores = {lab: 0 for lab in self.labs}
        self.analyzer = Analyzer(token_filters=[POSKeepFilter(["名詞"])])
        self.expecting_reverse_answer = False
        self.reverse_words = None

        # 研究室ごとの固有キーワードを作成
        self.unique_keywords = {}
        all_kws = {lab: set(kws) for lab, (_, kws) in self.labs.items()}

        for lab, kws in all_kws.items():
            others = set().union(*(kw for l2, kw in all_kws.items() if l2 != lab))
            self.unique_keywords[lab] = kws - others

    # 初期化
    def init_function(self, query_params):
        self.scores = {lab: 0 for lab in self.labs}
        self.expecting_reverse_answer = False
        self.reverse_words = None
        return "どんな研究に興味がありますか？（例: 画像処理、AI など）「列挙」で途中経過を表示します。"

    # 名詞抽出
    def extract_nouns(self, text):
        tokens = self.analyzer.analyze(text)
        nouns = [getattr(t, "base_form", None) or t.surface for t in tokens]
        return [n for n in nouns if n]

    # スコア更新
    def update_score_maxonly(self, words):
        lab_hits = {lab: [] for lab in self.labs}

        for w in words:
            for lab, (_, keywords) in self.labs.items():
                for kw in keywords:

                    # 完全一致
                    if w == kw:
                        lab_hits[lab].append(self.KEYWORD_FULL_SCORE)
                        break

                    # 部分一致
                    if len(w) >= 3 and len(kw) >= 3:
                        if kw.startswith(w) or w.startswith(kw):
                            lab_hits[lab].append(self.KEYWORD_PART_SCORE)
                            break

        # 研究室ごとに最大スコアだけ採用
        for lab, hit_list in lab_hits.items():
            if hit_list:
                self.scores[lab] += max(hit_list)

    # 上位3研究室
    def get_top3_labs(self):
        return sorted(self.scores.items(), key=lambda x: -x[1])[:3]

    # 逆質問
    def maybe_ask_reverse_question(self):
        if random.random() > self.REVERSE_QUESTION_PROB:
            return None

        top3 = self.get_top3_labs()
        if len(top3) < 2:
            return None

        top1_lab, top2_lab = top3[0][0], top3[1][0]

        # 各研究室の固有キーワードを優先抽出
        uniq1 = list(self.unique_keywords.get(top1_lab, []))
        uniq2 = list(self.unique_keywords.get(top2_lab, []))

        # 固有キーワードから1つずつ選択。なければ上位3研究室のキーワードからランダム
        if uniq1 and uniq2:
            w1 = random.choice(uniq1)
            w2 = random.choice(uniq2)
        else:
            kws1 = set(self.labs[top1_lab][1])
            kws2 = set(self.labs[top2_lab][1])
            unique_kws = list((kws1 | kws2) - (kws1 & kws2))

            if len(unique_kws) < 2:
                combined_kws = set()
                for lab, _ in top3:
                    combined_kws.update(self.labs[lab][1])
                unique_kws = list(combined_kws)
                if len(unique_kws) < 2:
                    return None

            w1, w2 = random.sample(unique_kws, 2)

        self.reverse_words = (w1, w2)
        self.expecting_reverse_answer = True

        return (
            "ちなみに、どちらの分野に興味がありますか？ 半角数字でお答えください。\n"
            f"1. {w1}\n"
            f"2. {w2}\n"
            f"3. どちらも興味ない"
        )

    # 逆質問回答 (1〜3の選択肢)
    def handle_reverse_answer(self, text):
        ans = text.strip()
        if ans not in {"1", "2", "3"}:
            return "半角数字 1〜3 で答えてください。", True

        w1, w2 = self.reverse_words
        self.expecting_reverse_answer = False
        self.reverse_words = None

        if ans == "1":
            for lab, (_, keywords) in self.labs.items():
                if any(w1 == kw or w1 in kw or kw in w1 for kw in keywords):
                    self.scores[lab] += self.REVERSE_KEYWORD_SCORE
            return f"『{w1}』に興味があるんですね。反映しました。\n他にどんな研究に興味がありますか？", True

        if ans == "2":
            for lab, (_, keywords) in self.labs.items():
                if any(w2 == kw or w2 in kw or kw in w2 for kw in keywords):
                    self.scores[lab] += self.REVERSE_KEYWORD_SCORE
            return f"『{w2}』に興味があるんですね。反映しました。\n他にどんな研究に興味がありますか？", True

        # ans == 3
        for word in (w1, w2):
            for lab, (_, keywords) in self.labs.items():
                if any(word == kw or word in kw or kw in word for kw in keywords):
                    self.scores[lab] -= self.REVERSE_KEYWORD_NEG
        return "どちらにも興味ないのですね。了解しました。\n他にどんな研究に興味がありますか？", True

    def callback_method(self, text, response):
        text = text.strip()

        if self.expecting_reverse_answer:
            return self.handle_reverse_answer(text)

        # 列挙
        if "列挙" in text:
            top3 = self.get_top3_labs()
            msg = "スコア上位 3 研究室：\n"
            for lab, sc in top3:
                msg += f"- {lab}（{self.labs[lab][0]}）: {sc} 点\n"
            return msg, True

        # 名詞抽出
        nouns = self.extract_nouns(text)
        if not nouns:
            return "他に興味のある研究分野はありますか？", True

        # スコア更新
        self.update_score_maxonly(nouns)

        # 推薦判定
        sorted_scores = sorted(self.scores.items(), key=lambda x: -x[1])
        if len(sorted_scores) >= 2:
            top1, top2 = sorted_scores[0], sorted_scores[1]
            if top1[1] - top2[1] >= self.RECOMMEND_DIFF and top1[1] > 0:
                lab = top1[0]
                return f"{lab}（{self.labs[lab][0]}）がおすすめです！", False

        # 逆質問
        rev = self.maybe_ask_reverse_question()
        if rev:
            return rev, True

        # 継続
        return "他にはどんな分野に興味がありますか？（「列挙」で途中経過を表示できます）", True

if __name__ == "__main__":
    address = "0.0.0.0"
    port = 2000
    chat_server = ChatServer(MyChatClass, UserClass)
    chat_server.start(address, port)