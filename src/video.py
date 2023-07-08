import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YUOTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id
        video_response = youtube.videos().list(part='snippet,statistics',id=video_id).execute()
        self.video_title = video_response['items'][0]['snippet']['title']
        self.video_url = 'https://www.youtube.com/watch?v=' + video_id
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.video_title}"

    @property
    def name(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id, plv_id):
        super().__init__(video_id)
        self.__plv_id = plv_id

    @property
    def name(self):
        return self.__video_id
