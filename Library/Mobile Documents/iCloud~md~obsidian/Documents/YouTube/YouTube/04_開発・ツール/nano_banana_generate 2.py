#!/usr/bin/env python3
"""
AI画像生成ツール - Cursor連携用
Pollinations.ai (無料・認証不要) と Google Gemini API に対応。

使い方:
  python3 nano_banana_generate.py "プロンプト"
  python3 nano_banana_generate.py "プロンプト" --model flux --width 1920 --height 1080
  python3 nano_banana_generate.py "プロンプト" --provider gemini --model pro

プロバイダー:
  - pollinations (デフォルト): 完全無料・APIキー不要
  - gemini: Google Gemini API (要 GEMINI_API_KEY + 課金設定)
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path

POLLINATIONS_MODELS = {
    "flux": "flux",
    "turbo": "turbo",
    "gptimage": "gpt-image",
    "seedream": "seedream",
}

GEMINI_MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "nano-banana-pro-preview",
}

OUTPUT_DIR = Path(__file__).parent / "generated_images"


def generate_pollinations(prompt, model="flux", width=1024, height=1024, enhance=True):
    """Pollinations.ai で画像生成（無料・APIキー不要）"""
    model_id = POLLINATIONS_MODELS.get(model, model)
    print(f"プロバイダー: Pollinations.ai (無料)")
    print(f"モデル: {model_id}")
    print(f"サイズ: {width}x{height}")
    print(f"プロンプト: {prompt}")
    print("画像を生成中...")

    encoded_prompt = urllib.parse.quote(prompt)
    params = {
        "width": str(width),
        "height": str(height),
        "model": model_id,
        "nologo": "true",
        "enhance": "true" if enhance else "false",
    }
    query = urllib.parse.urlencode(params)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{query}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"img_{model_id}_{timestamp}.jpg"
    filepath = OUTPUT_DIR / filename

    result = subprocess.run(
        ["curl", "-s", "-L", "-o", str(filepath), "-w", "%{http_code}", url],
        capture_output=True, text=True, timeout=180,
    )
    http_code = result.stdout.strip()

    if http_code != "200" or not filepath.exists() or filepath.stat().st_size < 1000:
        print(f"エラー: HTTP {http_code}")
        if filepath.exists():
            filepath.unlink()
        sys.exit(1)

    size_kb = filepath.stat().st_size / 1024
    print(f"\n生成完了!")
    print(f"  保存先: {filepath}")
    print(f"  サイズ: {size_kb:.1f} KB")
    return [filepath]


def generate_gemini(prompt, model_key="flash", reference_image_path=None):
    """Google Gemini API で画像生成（要APIキー + 課金設定）"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("エラー: GEMINI_API_KEY が設定されていません。")
        print("  export GEMINI_API_KEY='your-key' を設定してください。")
        print("  また、Google AI Studio で課金を有効にする必要があります。")
        sys.exit(1)

    model_id = GEMINI_MODELS.get(model_key, model_key)
    print(f"プロバイダー: Google Gemini API")
    print(f"モデル: {model_id}")
    print(f"プロンプト: {prompt}")
    print("画像を生成中...")

    parts = [{"text": prompt}]
    if reference_image_path:
        ref_path = Path(reference_image_path)
        if not ref_path.exists():
            print(f"エラー: 参照画像が見つかりません: {reference_image_path}")
            sys.exit(1)
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        mime_type = mime_map.get(ref_path.suffix.lower(), "image/png")
        with open(ref_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        parts.append({"inline_data": {"mime_type": mime_type, "data": img_b64}})

    payload = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"APIエラー ({e.code}): {error_body}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []
    idx = 0
    for cand in result.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "text" in part:
                print(f"\nAI: {part['text']}")
            elif "inlineData" in part:
                data = base64.b64decode(part["inlineData"]["data"])
                mime = part["inlineData"].get("mimeType", "image/png")
                ext = ".png" if "png" in mime else ".jpg"
                fp = OUTPUT_DIR / f"gemini_{timestamp}_{idx}{ext}"
                with open(fp, "wb") as f:
                    f.write(data)
                saved.append(fp)
                idx += 1

    if saved:
        print(f"\n生成完了! {len(saved)} 枚:")
        for fp in saved:
            print(f"  {fp}")
    else:
        print("画像が生成されませんでした。")
    return saved


def main():
    parser = argparse.ArgumentParser(
        description="AI画像生成ツール (Pollinations.ai / Google Gemini)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本（Pollinations.ai - 無料・即使える）
  python3 nano_banana_generate.py "可愛い猫がラーメンを食べている"

  # モデル指定
  python3 nano_banana_generate.py "東京タワーの夕暮れ" --model flux

  # 横長サムネイル用
  python3 nano_banana_generate.py "YouTube thumbnail" --width 1280 --height 720

  # Gemini API（要課金設定）
  python3 nano_banana_generate.py "ロゴ" --provider gemini --model pro

利用可能モデル (Pollinations):
  flux     - 高品質（デフォルト）
  turbo    - 高速
  gptimage - GPT Image
  seedream - Seedream

利用可能モデル (Gemini):
  flash    - Nano Banana (Gemini 2.5 Flash Image)
  pro      - Nano Banana Pro
""",
    )
    parser.add_argument("prompt", help="画像生成プロンプト")
    parser.add_argument("--provider", "-p", choices=["pollinations", "gemini"], default="pollinations", help="APIプロバイダー (デフォルト: pollinations)")
    parser.add_argument("--model", "-m", default="flux", help="モデル名 (デフォルト: flux)")
    parser.add_argument("--width", "-W", type=int, default=1024, help="画像幅 (デフォルト: 1024)")
    parser.add_argument("--height", "-H", type=int, default=1024, help="画像高さ (デフォルト: 1024)")
    parser.add_argument("--edit", "-e", metavar="IMAGE", help="参照画像パス (Geminiのみ)")
    parser.add_argument("--output", "-o", metavar="DIR", help="出力ディレクトリ")
    parser.add_argument("--no-enhance", action="store_true", help="プロンプト自動改善を無効化")

    args = parser.parse_args()

    if args.output:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output)

    if args.provider == "gemini":
        generate_gemini(args.prompt, model_key=args.model, reference_image_path=args.edit)
    else:
        generate_pollinations(args.prompt, model=args.model, width=args.width, height=args.height, enhance=not args.no_enhance)


if __name__ == "__main__":
    main()
