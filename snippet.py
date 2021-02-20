from apiclient.discovery import build

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_API_KEY = "AIzaSyAVKnfeGxZe3fMlpvNrlkrhD8hEs4DU6jE"
youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=YOUTUBE_API_KEY
    )

error_snippet = 0

def get_published_at(video_id):
    global error_snippet
    error_snippet = 0
    try:
        published_at = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["publishedAt"]
        return published_at
    except:
        error_snippet = 1

def get_channel_id(video_id):
    global error_snippet
    error_snippet = 0
    try:
        channel_id = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["channelId"]
        return channel_id
    except:
        error_snippet = 1

def get_title(video_id):
    global error_snippet
    error_snippet = 0
    try:
        title = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["title"]
        return title
    except:
        error_snippet = 1

def get_description(video_id):
    global error_snippet
    error_snippet = 0
    try:
        description = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["description"]
        return description
    except:
        error_snippet = 1

def get_channel_title(video_id):
    global error_snippet
    error_snippet = 0
    try:
        channel_title = youtube.videos().list(part = "snippet", id = video_id).execute()["items"][0]["snippet"]["channelTitle"]
        return channel_title
    except:
        error_snippet = 1

def get_duration(video_id):
    global error_snippet
    error_snippet = 0
    try:
        duration = youtube.videos().list(part = "contentDetails", id = video_id).execute()["items"][0]["contentDetails"]["duration"]
        return duration
    except:
        error_snippet = 1

'''
video_id = "J9zp5D6JddI"
print(get_published_at(video_id))
print("")
print(get_channel_id(video_id))
print("")
print(get_title(video_id))
print("")
print(get_description(video_id))
print("")
print(get_channel_title(video_id))
print("")
print(get_duration(video_id))
print("")
'''