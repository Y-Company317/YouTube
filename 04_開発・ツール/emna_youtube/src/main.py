import os
import pickle
import pandas as pd
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# APIの設定
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
ANALYTICS_SERVICE_NAME = 'youtubeAnalytics'
ANALYTICS_VERSION = 'v2'

# ファイルパスの設定
# 実行ディレクトリは 04_開発・ツール/emna_youtube/ を想定
CLIENT_SECRETS_FILE = '../client_secret1.json'
# キャッシュを回避するためにファイル名を変更
TOKEN_FILE = 'token_v3.pickle'
OUTPUT_DIR = '../../01_チャンネル運営/日本称賛/チャンネル情報/世界に誇るJAPAN'

def get_authenticated_services():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(f"クライアントシークレットファイルが見つかりません: {os.path.abspath(CLIENT_SECRETS_FILE)}")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            
            # デスクトップアプリ設定であれば、run_local_server が最も安定して動作します
            # ブラウザを自動で立ち上げ、アカウント選択画面を強制的に表示します
            creds = flow.run_local_server(port=0, prompt='select_account')
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
    analytics = build(ANALYTICS_SERVICE_NAME, ANALYTICS_VERSION, credentials=creds)
    return youtube, analytics

def get_channel_basic_info(youtube):
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        mine=True
    )
    response = request.execute()
    
    if not response['items']:
        return None

    item = response['items'][0]
    return {
        'id': item['id'],
        'title': item['snippet']['title'],
        'published_at': item['snippet']['publishedAt'],
        'subscriber_count': int(item['statistics'].get('subscriberCount', 0)),
        'view_count': int(item['statistics'].get('viewCount', 0)),
        'video_count': int(item['statistics'].get('videoCount', 0)),
        'upload_playlist_id': item['contentDetails']['relatedPlaylists']['uploads']
    }

def get_video_list(youtube, playlist_id, max_results=50):
    videos = []
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=max_results
    )
    
    while request and len(videos) < max_results:
        response = request.execute()
        
        video_ids = []
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        
        # 動画の詳細統計情報を取得
        stats_request = youtube.videos().list(
            part="statistics,snippet",
            id=','.join(video_ids)
        )
        stats_response = stats_request.execute()
        
        for item in stats_response['items']:
            videos.append({
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0))
            })
            
        request = youtube.playlistItems().list_next(request, response)
        
    return videos

def get_analytics_report(analytics, channel_id, start_date, end_date):
    reports = {}
    
    # 1. 日別再生数
    try:
        daily_views = analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='views,estimatedMinutesWatched,averageViewDuration',
            dimensions='day',
            sort='day'
        ).execute()
        reports['daily_views'] = daily_views.get('rows', [])
    except Exception as e:
        print(f"日別データの取得エラー: {e}")

    # 2. トラフィックソース
    try:
        traffic_source = analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='views',
            dimensions='insightTrafficSourceType',
            sort='-views'
        ).execute()
        reports['traffic_source'] = traffic_source.get('rows', [])
    except Exception as e:
        print(f"トラフィックソースの取得エラー: {e}")

    # 3. 視聴者属性（年齢・性別）
    try:
        demographics = analytics.reports().query(
            ids=f'channel=={channel_id}',
            startDate=start_date,
            endDate=end_date,
            metrics='viewerPercentage',
            dimensions='ageGroup,gender',
            sort='-viewerPercentage'
        ).execute()
        reports['demographics'] = demographics.get('rows', [])
    except Exception as e:
        print(f"視聴者属性の取得エラー: {e}")
        
    return reports

def save_to_markdown(channel_info, videos, analytics_data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# YouTubeチャンネル分析レポート: {channel_info['title']}\n\n")
        f.write(f"**作成日**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        # 1. 基本情報
        f.write("## 1. チャンネル基本情報\n\n")
        f.write(f"- **登録者数**: {channel_info['subscriber_count']:,} 人\n")
        f.write(f"- **総再生回数**: {channel_info['view_count']:,} 回\n")
        f.write(f"- **動画本数**: {channel_info['video_count']:,} 本\n")
        f.write(f"- **開設日**: {channel_info['published_at']}\n\n")
        
        # 2. アナリティクス詳細
        f.write("## 2. アナリティクス詳細 (過去30日間)\n\n")
        
        f.write("### トラフィックソース (上位)\n")
        f.write("| ソース | 再生回数 |\n")
        f.write("| --- | ---: |\n")
        if 'traffic_source' in analytics_data:
            for row in analytics_data['traffic_source']:
                source_name = row[0]
                views = row[1]
                f.write(f"| {source_name} | {views:,} |\n")
        f.write("\n")

        f.write("### 視聴者属性 (上位)\n")
        f.write("| 年齢層 | 性別 | 割合(%) |\n")
        f.write("| --- | --- | ---: |\n")
        if 'demographics' in analytics_data:
            for row in analytics_data['demographics']:
                age = row[0]
                gender = row[1]
                percentage = row[2]
                f.write(f"| {age} | {gender} | {percentage:.1f}% |\n")
        f.write("\n")
        
        # 3. 最新動画一覧
        f.write("## 3. 最新動画一覧 (直近50件)\n\n")
        f.write("| 公開日 | タイトル | 再生数 | 高評価 | コメント |\n")
        f.write("| --- | --- | ---: | ---: | ---: |\n")
        for video in videos:
            pub_date = video['published_at'][:10]
            title = video['title'].replace('|', '\|')
            f.write(f"| {pub_date} | {title} | {video['view_count']:,} | {video['like_count']:,} | {video['comment_count']:,} |\n")

def main():
    try:
        print("認証を開始します...")
        youtube, analytics = get_authenticated_services()
        
        print("チャンネル基本情報を取得中...")
        channel_info = get_channel_basic_info(youtube)
        if not channel_info:
            print("チャンネル情報が取得できませんでした。")
            return

        print("動画一覧を取得中...")
        videos = get_video_list(youtube, channel_info['upload_playlist_id'])
        
        print("アナリティクスデータを取得中...")
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        analytics_data = get_analytics_report(analytics, channel_info['id'], start_date, end_date)
        
        # 保存
        output_filename = f"チャンネル分析レポート_{datetime.now().strftime('%Y%m%d')}.md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        print(f"レポートを作成中: {output_path}")
        save_to_markdown(channel_info, videos, analytics_data, output_path)
        print("完了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()if __name__ == '__main__':
    main()