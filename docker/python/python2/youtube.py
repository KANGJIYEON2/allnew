from googleapiclient.discovery import build

api_key = "AIzaSyBuSBP7wVQalqBHmxTm1msro7pMmr3c5Ao"
youtube = build("youtube", "v3", developerKey=api_key)

video_ids = ["일본 여행", "러시아 여행", "중국여행"]

for video_id in video_ids:
    request = youtube.videos().list(part="snippet,statistics", id=video_ids)
    response = request.execute()

    video_title = response["items"][0]["snippet"]["title"]
    view_count = response["items"][0]["statistics"]["viewCount"]

    print(f"Title: {video_title}")
    print(f"View Count: {view_count}")
