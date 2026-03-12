#!/usr/bin/env python3
"""記事用画像バッチ生成スクリプト"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "nano-banana-pro-preview"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
OUTPUT_DIR = Path(__file__).parent / "nanobanana画像" / "記事画像"

PROMPTS = [
    # === 副業時代（収益0円の6ヶ月間）===
    ("01_深夜のデスク", "A realistic photo of a young Japanese man in his 20s working alone late at night at a small desk in a tiny Japanese apartment. Only the laptop screen illuminates his tired face. Empty energy drink cans on the desk. Clock shows 11PM. Moody, lonely atmosphere. Shot on Sony A7III, 35mm lens, natural lighting from laptop screen only."),
    ("02_早朝の通勤電車", "A realistic photo taken inside a crowded Japanese morning commuter train. A tired young Japanese man in business casual standing, holding a smartphone showing YouTube Studio analytics with very low numbers. Early morning light through train windows. Other commuters around him. Candid street photography style, shot on Fujifilm X100V."),
    ("03_再生数1桁のアナリティクス", "A realistic close-up photo of a smartphone screen in a dark environment showing YouTube analytics dashboard with very low view counts (single digit numbers). The phone is held by a male hand. The screen glow reflects on a tired face slightly visible in the background. Moody, dark, cinematic."),
    ("04_孤独な夜の作業部屋", "A realistic photo of a small Japanese apartment room at night. A single desk lamp illuminates a laptop and editing workspace. The room is messy with notes and papers. A window shows the city lights outside. No person visible - just the empty chair pulled back as if someone just left. Lonely, melancholic atmosphere. Film photography aesthetic."),
    ("05_金曜の夜の対比", "A realistic photo taken from outside a Japanese izakaya (居酒屋) at night. Through the warm glowing window, silhouettes of friends laughing and drinking beer are visible. The street outside is dark and empty with rain puddles reflecting the neon signs. Shot from the perspective of someone walking alone past the bar. Cinematic, emotional contrast between warmth inside and cold outside."),
    # === 副業時代続き + 野球部 ===
    ("06_朝6時のアラーム", "A realistic close-up photo of an iPhone alarm screen showing 6:00 AM in a dark bedroom. The phone sits on a simple bedside table. Early blue dawn light barely visible through curtains. The bed sheets are rumpled. Photorealistic, intimate, quiet moment before a long day."),
    ("07_収益化達成の瞬間", "A realistic photo of a laptop screen showing YouTube Studio with a monetization approval notification. The screen shows 'Congratulations' message. A young man's hands are visible resting on the keyboard. The room is dimly lit. The mood is quiet relief rather than celebration. Subtle, understated emotional moment."),
    ("08_高校の野球グラウンド夕暮れ", "A realistic photo of an empty Japanese high school baseball field (グラウンド) at golden hour sunset. Dusty infield, worn bases, batting cage in the background. Long shadows stretch across the dirt. A single forgotten baseball glove lies near the pitcher's mound. Nostalgic, bittersweet atmosphere. Shot on film camera, warm tones."),
    ("09_真夏の練習風景", "A realistic photo of a Japanese high school baseball practice in intense summer heat. Dust rising from the dirt field, harsh sunlight creating strong shadows. Baseball equipment scattered around. Heat haze visible in the air. The scorching atmosphere is palpable. Shot from ground level, dramatic perspective. No faces clearly visible."),
    ("10_暗い夜道の自転車", "A realistic photo of a dark empty Japanese residential road at night. A single bicycle with a dim light is visible in the distance. Street lights create pools of light on the asphalt. Power lines overhead against a dark blue sky. The atmosphere conveys exhaustion and loneliness of riding home late after practice. Cinematic, moody, Fujifilm film simulation aesthetic."),
    # === 野球部続き + BAN ===
    ("11_ボロボロのグローブ", "A realistic close-up photo of a well-worn, beaten-up leather baseball glove sitting on a wooden bench in a Japanese high school locker room. The leather is cracked and stained with dirt and sweat. Afternoon light streaming through a small window. Nostalgic, story-telling still life photography."),
    ("12_教室の休憩", "A realistic photo of a Japanese high school classroom during break time. A male student is slumped over his desk, exhausted, sleeping with his head on his arms. Sunlight streams through the windows. Other empty desks around him. The scene conveys extreme physical exhaustion. Natural light photography."),
    ("13_BAN通知のPC画面", "A realistic photo of a laptop screen in a dark room showing multiple YouTube channel termination/policy violation notification emails. Red warning icons visible. The laptop screen is the only light source. A coffee cup sits untouched beside the laptop. The atmosphere is devastating and cold. Cinematic, dark."),
    ("14_絶望の暗い部屋", "A realistic photo of a young Japanese man sitting on the floor of a dark apartment, leaning against the wall, head down, hands on his knees. The only light comes from a laptop screen nearby showing error messages. The room is otherwise completely dark. The posture conveys complete devastation and despair. Cinematic, low-key lighting."),
    ("15_朝PCを開く恐怖", "A realistic photo from behind a young Japanese man sitting at a desk, about to open his laptop. Early morning light coming through the window blinds creating stripe shadows. His posture is tense and hesitant. The moment before receiving bad news. Suspenseful, cinematic atmosphere. Shot on 50mm lens, shallow depth of field."),
    # === BAN復活 ===
    ("16_チームメンバーとの再起", "A realistic photo of a small meeting room or co-working space in Japan. Several laptops open on a table. Coffee cups and notebooks scattered around. The atmosphere suggests a late-night strategy session. Warm overhead lighting. Collaborative, determined energy. No faces clearly visible, focus on the workspace and hands working."),
    ("17_ビジネス書の山", "A realistic close-up photo of a tall stack of Japanese business and self-help books piled on a desk. Some books are open with highlighted passages and sticky notes. A laptop is visible in the background. Warm desk lamp lighting. The image conveys years of dedicated study and self-improvement. Bookshelf photography style."),
    ("18_深夜の執筆作業", "A realistic photo of a young Japanese man working intensely at his desk late at night, typing on a laptop. Multiple monitors showing video editing software and scripts. The room is dark except for screen glow and a small desk lamp. Coffee and energy drinks nearby. The atmosphere conveys relentless work ethic. Cinematic, documentary style."),
    ("19_夜明けの窓際", "A realistic photo of early dawn light breaking through apartment window curtains. A laptop sits on a desk near the window, still open from overnight work. The transition from night to day symbolizes a new beginning. Purple and orange sky visible through the window. Peaceful yet determined atmosphere. Film photography aesthetic."),
    ("20_崖の上の夕日シルエット", "A realistic photo of a single person standing as a silhouette on a coastal cliff edge, looking out at a dramatic sunset over the ocean. The sky has rich orange, purple and gold tones. The person stands tall and confident, conveying resilience and determination. Wide angle landscape photography, dramatic natural lighting. Similar to a motivational poster but authentic and photojournalistic."),
]

def generate_one(name, prompt, retries=3):
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode("utf-8")
    url = f"{API_BASE}/{MODEL}:generateContent?key={API_KEY}"

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            for cand in result.get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    if "inlineData" in part:
                        data = base64.b64decode(part["inlineData"]["data"])
                        mime = part["inlineData"].get("mimeType", "image/png")
                        ext = ".png" if "png" in mime else ".jpg"
                        fp = OUTPUT_DIR / f"{name}{ext}"
                        with open(fp, "wb") as f:
                            f.write(data)
                        return fp
            print(f"  [{name}] 画像なし - テキストのみ返却")
            return None
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:200]
            print(f"  [{name}] APIエラー({e.code}) attempt {attempt+1}: {body}")
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"  レート制限 - {wait}秒待機...")
                time.sleep(wait)
            else:
                return None
        except Exception as e:
            print(f"  [{name}] エラー: {e}")
            if attempt < retries - 1:
                time.sleep(5)
    return None

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    total = len(PROMPTS)
    success = 0
    failed = []

    for i, (name, prompt) in enumerate(PROMPTS):
        print(f"\n[{i+1}/{total}] {name} を生成中...")
        fp = generate_one(name, prompt)
        if fp:
            size_kb = fp.stat().st_size / 1024
            print(f"  完了: {fp.name} ({size_kb:.0f}KB)")
            success += 1
        else:
            failed.append(name)
            print(f"  失敗: {name}")
        if i < total - 1:
            time.sleep(3)

    print(f"\n{'='*50}")
    print(f"生成完了: {success}/{total} 枚成功")
    if failed:
        print(f"失敗: {', '.join(failed)}")
    print(f"保存先: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
