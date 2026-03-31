#!/usr/bin/env python3
"""
LP漫画30パネル バッチ生成スクリプト
みこさわストーリーに基づく漫画パネルを一括生成
"""
import subprocess
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).parent / "nano_banana_generate.py"
OUTPUT_DIR = Path(__file__).parent / "generated_images" / "manga_panels"

STYLE_PREFIX = (
    "Japanese seinen manga panel, high quality illustration, "
    "young Japanese man late 20s with short messy black hair, "
    "realistic proportions, clean line art with screen-tone shading, "
    "muted color palette with selective color accents, "
    "professional manga quality, cinematic composition. "
)

PANELS = [
    # === ACT 1: 原点 (1-5) ===
    {
        "num": 1,
        "prompt": STYLE_PREFIX +
            "A tired single mother in work clothes arriving home at night, seen from a child's perspective looking up. "
            "Dark apartment entrance, dim lighting. The mother looks exhausted, bags under her eyes. "
            "Large Japanese speech bubble text: '大人になるって、こういうことなのか？' "
            "Smaller text below: 'シングルマザーだった母は、毎晩21時頃に帰宅し、泥のように眠る毎日だった' "
            "Bottom text: '手取りはおそらく20万円ほど。贅沢なんてできるはずもない'",
    },
    {
        "num": 2,
        "prompt": STYLE_PREFIX +
            "A teenage boy sitting in the corner of a high school classroom, looking down with a forced smile. "
            "Other students in background laughing. Harsh fluorescent lighting. "
            "Large speech bubble from off-screen: 'お前、本当に何も考えてないよな' "
            "Inner monologue text: '何も言い返せず、ただ愛想笑いを浮かべることしかできない' "
            "Small text: '悔しさでいっぱいなのに'",
    },
    {
        "num": 3,
        "prompt": STYLE_PREFIX +
            "Split panel: left side shows intense high school baseball practice, muddy field, exhausted players. "
            "Right side shows the same boy years later in a suit on a crowded morning train, looking defeated. "
            "Large text on left: '全てを犠牲にした野球部時代' "
            "Large text on right: '手取り17万の会社員' "
            "Bottom text: 'あと40年、これを続けるのか？'",
    },
    {
        "num": 4,
        "prompt": STYLE_PREFIX +
            "Young man sitting at a desk late at night with a laptop, dim room lit only by screen glow. "
            "Coffee cup beside him, disheveled hair, determined expression. Clock shows 2:00 AM. "
            "Text overlay: 'Webライター開始。副業という名の孤独な戦い' "
            "Speech bubble: 'とにかく金が欲しい。会社に依存せずに生きていきたい'",
    },
    {
        "num": 5,
        "prompt": STYLE_PREFIX +
            "Young man frustrated at his desk, looking at a bank statement or spreadsheet showing income plateau. "
            "Graphs showing flat line around 10-15万 mark. Crumpled papers around. "
            "Large bold text: '月収10万〜15万の壁' "
            "Speech bubble: 'これだけ犠牲にしても…限界なのか？'",
    },
    # === ACT 2: 転機 (6-10) ===
    {
        "num": 6,
        "prompt": STYLE_PREFIX +
            "Two young men talking in a casual meeting room or cafe. One (the protagonist with messy black hair) "
            "looks shocked with wide eyes. The other man speaks casually. "
            "Speech bubble from other man: '副業で月25万くらい行ってますね' "
            "Large dramatic text: '耳を疑った'",
    },
    {
        "num": 7,
        "prompt": STYLE_PREFIX +
            "Dramatic close-up of the protagonist's face with an epiphany expression, eyes wide, background shattered "
            "like breaking glass. Speed lines radiating outward. "
            "Large bold text: '努力の量が足りないんじゃない' "
            "Even larger text below: '努力する場所が間違っていたんだ'",
    },
    {
        "num": 8,
        "prompt": STYLE_PREFIX +
            "Young man working intensely at multiple monitors, YouTube analytics visible on screens. "
            "Sticky notes and notebooks scattered. Dark room, focused expression. "
            "Text overlay: 'YouTubeディレクターに転向' "
            "Small text: '平日5時間、土日8時間。週40時間を副業に注いだ'",
    },
    {
        "num": 9,
        "prompt": STYLE_PREFIX +
            "Multiple failed YouTube channel screens overlapping, all showing low view counts and declining graphs. "
            "Red X marks over each. The protagonist sits among them, head in hands. "
            "Large text: '全く鳴かず飛ばず' "
            "Speech bubble: 'やっぱり甘くないか…'",
    },
    {
        "num": 10,
        "prompt": STYLE_PREFIX +
            "Dark scene showing the protagonist alone, staring at YouTube Studio showing zero revenue. "
            "Empty wallet on desk. Calendar pages flying showing months passing. "
            "Bold text: '半年間、収益ゼロ' "
            "Smaller text: '貯金を切り崩す日々'",
    },
    # === ACT 3: 横ばいの苦悩 (11-16) ===
    {
        "num": 11,
        "prompt": STYLE_PREFIX +
            "Three-panel split layout. Left panel: YouTube Studio analytics screen showing '月収30万円' with a flat "
            "horizontal graph line. Center panel: a flat line graph labeled '12ヶ月' with text 'この1年、横ばい…' "
            "Right panel: close-up of protagonist's face with sweat drop, thinking '…これが、俺の天井か？'",
    },
    {
        "num": 12,
        "prompt": STYLE_PREFIX +
            "The protagonist grabbing his head with both hands in frustration, tears forming, "
            "laptop open on desk in front of him. Orange/warm background suggesting sunset. "
            "Large speech bubble: '何が足りないんだ…？'",
    },
    {
        "num": 13,
        "prompt": STYLE_PREFIX +
            "Four-panel grid layout. Top-left: thumbnail editing software with green checkmark and text 'サムネ改善 ✅'. "
            "Top-right: video editing timeline with green checkmark 'タイトル改善 ✅'. "
            "Bottom-left: online school interface with green checkmark 'スクール ✅'. "
            "Bottom-right: protagonist looking at declining graph with speech bubble '全部やったのに…'",
    },
    {
        "num": 14,
        "prompt": STYLE_PREFIX +
            "Split composition. Main image: protagonist looking at smartphone showing Twitter/X feed with posts saying "
            "'月100万達成しました！🎉'. Second part: close-up of protagonist's frustrated face with sweat. "
            "Speech bubble: '後から始めた奴が…'",
    },
    {
        "num": 15,
        "prompt": STYLE_PREFIX +
            "Chaotic composition. The protagonist at center with spiral eyes, overwhelmed, surrounded by floating "
            "advice cards and speech bubbles: 'AIを使え！' '外注しろ！' 'ショートが伸びる！' '長尺で勝負！' "
            "'TTPしろ！' 'オリジナリティを出せ！' '毎日投稿！' '質より量！' '量より質！' "
            "Question marks floating everywhere.",
    },
    {
        "num": 16,
        "prompt": STYLE_PREFIX +
            "The protagonist sitting on the floor of a dark room at night, back against the wall, "
            "laptop glowing nearby, scattered papers. Clock shows 2:00 AM. Moonlight through window. "
            "Large speech bubble: '…このまま一生30万か' "
            "Text below: 'サムネの問題じゃない。投稿頻度の問題でもない。' "
            "Text: 'じゃあ…何が問題なんだ…'",
    },
    # === ACT 4: 覚醒と戦略 (17-20) ===
    {
        "num": 17,
        "prompt": STYLE_PREFIX +
            "Dynamic scene of the protagonist walking outdoors with earbuds in, sunrise background, "
            "determined expression. Thought bubbles showing self-improvement audio waveforms. "
            "Bold text: '自分を洗脳した' "
            "Text: '散歩中も、筋トレ中も、自己啓発を聴き続けた'",
    },
    {
        "num": 18,
        "prompt": STYLE_PREFIX +
            "The protagonist intensely watching YouTube videos on multiple screens, taking notes, "
            "eyes focused and analytical. Screen reflections on his face. "
            "Bold text: '視聴者心理になりきれ' "
            "Text: '半年間、動画を見続けた'",
    },
    {
        "num": 19,
        "prompt": STYLE_PREFIX +
            "Dramatic moment of realization. The protagonist standing, papers flying around him, "
            "golden light rays bursting from behind. A whiteboard with strategy notes visible. "
            "Bold text: '凡人の戦略を見つけた' "
            "Text: '勝てるジャンルで、クオリティで殴る'",
    },
    {
        "num": 20,
        "prompt": STYLE_PREFIX +
            "Triumphant scene. YouTube Studio showing monetization approved notification with confetti effects. "
            "The protagonist's hand clenched in victory fist. Bright warm lighting. "
            "Bold text: '2024年1月 収益化達成' "
            "Smaller text: '手取り15万円を突破'",
    },
    # === ACT 5: 爆発的成長 (21-25) ===
    {
        "num": 21,
        "prompt": STYLE_PREFIX +
            "Dramatic rising graph showing explosive revenue growth: 15万→50万→100万→730万. "
            "The protagonist silhouetted against the rising chart, arms slightly spread. "
            "Bold gold text: '副業月収730万円'",
    },
    {
        "num": 22,
        "prompt": STYLE_PREFIX +
            "The protagonist at a YouTube creators' event, surrounded by people looking at him with respect. "
            "Warm lighting, confident smile on his face. "
            "Bold text: '周りの視線が変わった' "
            "Text: 'かつて教室の隅で、誰にも相手にされなかった僕が'",
    },
    {
        "num": 23,
        "prompt": STYLE_PREFIX +
            "Professional scene. The protagonist in a modern office, video call with multiple team members "
            "shown on screen. Confident posture, leading a meeting. "
            "Bold text: '法人化。チーム8名' "
            "Text: '最高月商2,000万円'",
    },
    {
        "num": 24,
        "prompt": STYLE_PREFIX +
            "Four YouTube Silver Play Button awards displayed on a wall, gleaming under spotlights. "
            "The protagonist standing in front, looking at them with quiet satisfaction. "
            "Bold gold text: '銀盾4枚' "
            "Large text: '累計収益1億円突破'",
    },
    {
        "num": 25,
        "prompt": STYLE_PREFIX +
            "The protagonist looking out from a high-rise window at a city skyline, sunrise. "
            "Peaceful expression, cup of coffee in hand. Freedom embodied. "
            "Bold text: '自由を、手に入れた'",
    },
    # === ACT 6: 危機と復活、メッセージ (26-30) ===
    {
        "num": 26,
        "prompt": STYLE_PREFIX +
            "Dramatic dark panel. A smartphone showing 'チャンネルBAN' notification with red warning icon. "
            "Cracking/shattering effect around the screen. The protagonist's shocked face reflected. "
            "Bold red text: '2025年8月 チャンネルBAN' "
            "Text: '月収50万まで暴落'",
    },
    {
        "num": 27,
        "prompt": STYLE_PREFIX +
            "The protagonist standing up from his desk, fist clenched, intense determined eyes glowing. "
            "Dark background with single spotlight. Papers and plans spread on desk. "
            "Bold text: 'ここで終わるわけにはいかない'",
    },
    {
        "num": 28,
        "prompt": STYLE_PREFIX +
            "V-shaped recovery graph, dramatic upward arrow in gold. "
            "The protagonist's confident silhouette overlaid. Bright hopeful lighting. "
            "Bold gold text: 'V字回復' "
            "Text: '月500万円以上を継続'",
    },
    {
        "num": 29,
        "prompt": STYLE_PREFIX +
            "The protagonist with his team of 8 people, all standing together looking forward. "
            "Sunrise/dawn background. Team unity and determination. "
            "Bold text: '仲間と共に、這い上がった'",
    },
    {
        "num": 30,
        "prompt": STYLE_PREFIX +
            "Close-up of the protagonist looking directly at the viewer with a confident, encouraging expression. "
            "Hand extended toward camera. Bright, warm golden light behind him. "
            "Single large bold text: '次は、あなたの番だ'",
    },
]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    ref_image = None
    ref_candidates = [
        Path(__file__).parent.parent / ".cursor/projects/Users-mikosawayuudai-Library-Mobile-Documents-iCloud-md-obsidian-Documents-YouTube-YouTube/assets/__________2026-03-29_22.49.44-8feb1d3a-64ad-4abc-b998-6adafc1a14cf.png",
    ]

    total = len([p for p in PANELS if p["num"] >= start_from])
    done = 0

    for panel in PANELS:
        if panel["num"] < start_from:
            continue

        num = panel["num"]
        prompt = panel["prompt"]
        done += 1
        print(f"\n{'='*60}")
        print(f"  パネル {num}/30 を生成中... ({done}/{total})")
        print(f"{'='*60}")
        sys.stdout.flush()

        cmd = [
            sys.executable, str(SCRIPT),
            prompt,
            "--provider", "gemini",
            "--model", "pro",
            "--output", str(OUTPUT_DIR),
        ]

        try:
            result = subprocess.run(cmd, timeout=360)

            if result.returncode != 0:
                print(f"  [警告] パネル {num} の生成に失敗。スキップします。")

        except subprocess.TimeoutExpired:
            print(f"  [警告] パネル {num} がタイムアウト。スキップします。")

        if num < 30:
            print("  5秒待機中...")
            time.sleep(5)

    print(f"\n{'='*60}")
    print(f"  全パネルの生成が完了しました！")
    print(f"  保存先: {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
