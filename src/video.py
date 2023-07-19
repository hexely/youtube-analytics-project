import os
from googleapiclient.discovery import build

api_key: str = os.getenv('YUOTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


#class ServerNotFoundError(Exception):
    #def __init__(self)


class Video:

    def __init__(self, video_id: str) -> None:
        try:
            test = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
            self.test_title = test['items'][0]['snippet']['title']
        except:
            self.__video_id = video_id
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None
        else:
            self.__video_id = video_id
            video_response = youtube.videos().list(part='snippet,statistics',id=video_id).execute()
            self.title = video_response['items'][0]['snippet']['title']
            self.video_url = 'https://www.youtube.com/watch?v=' + video_id
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.title}"

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id, plv_id):
        super().__init__(video_id)
        self.__plv_id = plv_id

    @property
    def plv_id(self):
        return self.__plv_id
