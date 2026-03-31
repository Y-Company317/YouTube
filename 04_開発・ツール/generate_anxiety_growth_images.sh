#!/bin/bash

# 画像生成スクリプト
# 記事: 02_SNS運用/X/みこさわX/ポスト/記事/不安と成長曲線について 記事.md
# 生成枚数: 20枚
# モデル: Nano Banana Pro (Gemini)

SCRIPT_PATH="04_開発・ツール/nano_banana_generate.py"
PROVIDER="gemini"
MODEL="flash"

# 出力先ディレクトリ
OUTPUT_DIR="04_開発・ツール/generated_images/年収300万の会社員より、年収数千万の起業家の方が不安を抱えている"

# ディレクトリ作成
mkdir -p "$OUTPUT_DIR"

# 共通スタイル
STYLE="Flat vector illustration, simple, clean, orange and white color scheme, infographic style, Japanese text."

echo "画像生成を開始します..."
echo "保存先: $OUTPUT_DIR"

# 1. Intro: 3M vs 30M
python3 "$SCRIPT_PATH" "A flat vector illustration comparing two people. Left: Sad office worker with text '年収300万'. Right: Anxious entrepreneur with text '年収3000万'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 2. Intro: Mikosawa Stats
python3 "$SCRIPT_PATH" "A bar graph showing revenue going up and down wildly. Silver play buttons icon. Text '銀盾4枚' and '最高月商2000万'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 3. Section 1: Ideal Growth Curve
python3 "$SCRIPT_PATH" "A graph showing a straight line going up diagonally. Text '理想の成長'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 4. Section 1: Real Growth Curve
python3 "$SCRIPT_PATH" "A graph showing a volatile stock chart style line, going up in the long run but with many dips. Text '現実の成長'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 5. Section 1: The Dip (Despair)
python3 "$SCRIPT_PATH" "A magnifying glass focusing on a downward dip in a graph. Text '絶望'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 6. Section 2: Bad Comparison
python3 "$SCRIPT_PATH" "A person at the bottom of a dip looking up at the highest peak of the graph. Text '最高到達点と比較'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 7. Section 2: Good Comparison
python3 "$SCRIPT_PATH" "A person at the bottom of a dip looking back at the start (zero point). Text '過去の自分と比較'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 8. Section 2: Skill Assets
python3 "$SCRIPT_PATH" "A shield labeled 'SKILL' protecting a person. Money falling down, but shield remains. Text 'スキルは奪われない'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 9. Section 3: Flat Line Life
python3 "$SCRIPT_PATH" "A person walking on a completely flat, straight road. Looking bored. Text: '安定 = 停滞'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 10. Section 3: Volatile Life
python3 "$SCRIPT_PATH" "A person climbing a rugged, rocky mountain path. Looking tired but moving up. Text: '不安 = 成長'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 11. Section 3: Equation
# python3 "$SCRIPT_PATH" "Mathematical equation style. Text '不安 ＝ 成長痛'. Simple typography. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 12. Section 4: Panic Selling
# python3 "$SCRIPT_PATH" "A person panicking and selling stocks at the bottom of a crash. Text '狼狽売り'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 13. Section 4: Holding
# python3 "$SCRIPT_PATH" "A person holding on tight to a rope during a storm. Text 'ガチホ'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 14. Section 4: RPG Metaphor
# python3 "$SCRIPT_PATH" "A pixel art style hero facing a dragon. Text '人生はRPG'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 15. Section 5: Standard Value (Batteries)
# python3 "$SCRIPT_PATH" "Two batteries. One is 10% charged (labeled '弱小'). One is 100% charged (labeled '強豪'). Text '基準値の違い'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 16. Section 5: Speed Difference
# python3 "$SCRIPT_PATH" "Comparison: A person walking slowly vs a person in a fast taxi. Text 'スピードの差'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 17. Section 6: Harsh Environment
# python3 "$SCRIPT_PATH" "A person training in a storm, lifting weights. Strong and focused. Text '厳しい環境'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 18. Section 6: Comfort Zone
# python3 "$SCRIPT_PATH" "A person sleeping in a warm, cozy bed. Weak and soft. Text 'ぬるい環境'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 19. Section 7: Type 1 Anxiety (Inaction)
# python3 "$SCRIPT_PATH" "A person sitting on a chair, looking worried, doing nothing. Text '行動していない不安'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

# 20. Section 7: Type 2 Anxiety (Action)
# python3 "$SCRIPT_PATH" "A person climbing a wall, looking worried but moving. Text '行動している不安'. $STYLE" --provider $PROVIDER --model $MODEL --output "$OUTPUT_DIR"

echo "10枚の生成が完了しました。"
