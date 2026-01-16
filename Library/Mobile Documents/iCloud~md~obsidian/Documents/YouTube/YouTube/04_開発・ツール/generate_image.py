"""
画像生成スクリプト
横幅を広くして、左奥にお辞儀している人を増やした画像を生成します。
"""

import os

def generate_image():
    """
    横幅を広くして、左奥にお辞儀している人を増やした画像を生成
    """
    # APIキーを環境変数から取得（使用する場合は設定してください）
    api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        from openai import OpenAI
        
        if not api_key:
            print("OPENAI_API_KEY環境変数が設定されていません。")
            print("\n以下のプロンプトを画像生成AIサービスで使用してください：")
            return
        
        client = OpenAI(api_key=api_key)
        
        print("画像を生成中...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=get_image_prompt(),
            size="1792x1024",  # 横長のサイズ（横幅を広く）
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        print(f"\n画像が生成されました！")
        print(f"URL: {image_url}")
        print(f"\n画像をダウンロードするには、ブラウザで上記URLを開いてください。")
        
    except ImportError:
        print("OpenAIライブラリがインストールされていません。")
        print("\n以下のプロンプトを画像生成AIサービスで使用してください：")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("\n以下のプロンプトを画像生成AIサービスで使用してください：")


def get_image_prompt():
    """
    画像生成用の詳細なプロンプトを返す
    """
    prompt = """
A wide panoramic image of a formal procession in a modern, bright indoor hall. 

In the foreground, a line of approximately eight to ten East Asian men walking from left to right. They wear heavily soiled two-tone work uniforms: bright orange on the upper portion (shoulders and chest) transitioning to dark navy blue on the lower portion. Both sections are extensively covered in dried mud and dirt, giving them a mottled, earthy brown appearance. They wear dark, sturdy work boots and each carries a large olive-green canvas duffel bag. Their faces are serious and stoic, looking straight ahead, with expressions of weariness and determination. Their skin is also smudged with dirt.

In the background on the far left side, many additional East Asian men (approximately 15-20 people) are visible, dressed in clean white short-sleeved shirts with dark ties and dark pants, resembling formal office or service attire. They are standing in multiple rows, all bowing deeply with their heads lowered in respect and deference toward the passing line of workers. The bowing figures extend further back into the left background, creating depth.

The environment is clean and modern, with white or light-colored walls and a light gray, reflective floor. Large windows are visible in the upper right background, letting in natural light and showing a bright sky. The overall lighting is bright and even. The perspective is slightly low-angle, emphasizing the stature of the men in the foreground.

The image has a wide panoramic aspect ratio, emphasizing the breadth of the scene. The composition conveys a sense of a significant formal event or procession, highlighting the contrast between the arduous work implied by the dirty uniforms and the clean, respectful setting.
"""
    return prompt.strip()


if __name__ == "__main__":
    # プロンプトを表示してから生成を試みる
    print("画像生成プロンプト：")
    print("-" * 80)
    print(get_image_prompt())
    print("-" * 80)
    print()
    
    generate_image()

