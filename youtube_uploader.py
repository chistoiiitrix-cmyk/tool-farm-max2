"""
YOUTUBE UPLOADER v11 — Автозаливка Shorts/Reels на YouTube (и TikTok/Reels вручную)
0₽, работает в РФ, использует YouTube Data API v3 (бесплатно, квота 10k/день ~ 6 видео)

Настройка 1 раз (5 мин):
1. https://console.cloud.google.com → Новый проект ToolFarm → Включи YouTube Data API v3
2. OAuth consent screen → External → Email, название ToolFarm → Save
3. Credentials → Create Credentials → OAuth Client ID → Application type: Desktop App → Name: ToolFarmUploader → Download JSON → сохрани как credentials.json в корень проекта
4. Локально запусти: python youtube_uploader.py --auth
   Откроется браузер → выбери Google аккаунт → Разреши → создастся token.json
5. Для GitHub Actions: закодируй файлы в base64 и добавь в Secrets:
   echo -n '{"installed":...}' | base64 -w0 → YOUTUBE_CREDENTIALS_JSON
   cat token.json | base64 -w0 → YOUTUBE_TOKEN_JSON
   Workflow сам декодирует и зальет видео

Запуск: python youtube_uploader.py — зальет все mp4 из dist/videos/ как Shorts

Если нет credentials — просто логирует что залил бы, без ошибки.
"""

import pathlib, json, os, sys

BASE = pathlib.Path(__file__).parent
VIDEOS_DIR = BASE / "dist" / "videos"
CRED_PATH = BASE / "credentials.json"
TOKEN_PATH = BASE / "token.json"

def get_creds_from_env():
    """Для GitHub Actions — декодирует из Secrets"""
    import base64
    cred_b64 = os.getenv("YOUTUBE_CREDENTIALS_JSON")
    token_b64 = os.getenv("YOUTUBE_TOKEN_JSON")
    if cred_b64:
        try:
            data = base64.b64decode(cred_b64).decode()
            CRED_PATH.write_text(data, encoding='utf-8')
            print("✅ credentials.json восстановлен из Secrets")
        except Exception as e:
            print(f"Cred decode fail: {e}")
    if token_b64:
        try:
            data = base64.b64decode(token_b64).decode()
            TOKEN_PATH.write_text(data, encoding='utf-8')
            print("✅ token.json восстановлен из Secrets")
        except Exception as e:
            print(f"Token decode fail: {e}")

def auth_flow():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import google.oauth2.credentials
    except ImportError:
        print("Установи: pip install google-api-python-client google-auth-oauthlib")
        return None

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None
    if TOKEN_PATH.exists():
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            if not CRED_PATH.exists():
                print("❌ Нет credentials.json — скачай из Google Cloud Console (см. инструкцию в файле)")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(str(CRED_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json(), encoding='utf-8')
    return creds

def upload_video(file_path, metadata):
    """Загружает 1 видео как Shorts"""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("Нет googleapiclient, пропуск загрузки — видео готово в dist/videos/ для ручной заливки")
        print(f"MOCK UPLOAD: {file_path} Title: {metadata.get('title')}")
        return True

    creds = auth_flow()
    if not creds:
        print(f"MOCK UPLOAD (нет creds): {file_path}")
        return False

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": metadata.get("title","ToolFarm Short #shorts")[:100],
            "description": metadata.get("description","1500 инструментов бесплатно https://tool-farm.github.io")[:5000],
            "tags": metadata.get("tags",["shorts","лайфхак"])[:10],
            "categoryId": "28"  # Howto & Style
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    media = MediaFileUpload(str(file_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    print(f"⏫ Заливаю {file_path.name} как Shorts: {body['snippet']['title']}")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"✅ Залито: https://youtu.be/{response['id']}")
    return True

def main():
    get_creds_from_env()
    if len(sys.argv)>1 and sys.argv[1]=="--auth":
        auth_flow()
        print("✅ Auth done, token.json создан")
        return

    if not VIDEOS_DIR.exists():
        print("Нет папки dist/videos/ — запусти video_auto_factory.py сначала")
        return

    mp4s = list(VIDEOS_DIR.glob("*.mp4"))
    if not mp4s:
        print("Нет mp4 для заливки — есть txt заглушки, для теста норм")
        # Покажем что есть
        for f in VIDEOS_DIR.glob("*"):
            print(f" - {f.name}")
        return

    for mp4 in mp4s[:3]:  # максимум 3 в день чтобы не сжечь квоту YouTube (6 видео/день лимит)
        meta_path = mp4.with_suffix('.json')
        meta = json.loads(meta_path.read_text(encoding='utf-8')) if meta_path.exists() else {"title": mp4.stem + " #shorts", "description": "ToolFarm 1500 tools", "tags": ["shorts"]}
        upload_video(mp4, meta)

if __name__ == "__main__":
    main()
