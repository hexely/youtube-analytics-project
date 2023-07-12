import datetime
import os
from googleapiclient.discovery import build
import isodate


api_key: str = os.getenv('YUOTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    #Словарь где ключ - id видео, значение - количество лайков
    video_ids_dict = {}

    def __init__(self, playlist_id):
        self.playlist = youtube.playlists().list(part='snippet', id=playlist_id).execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails'
                                                            ).execute()
        self.title = self.playlist['items'][0]["snippet"]["title"]
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id

        #Заполнение словаря video_ids_dict ключами и значениями всех видео из плейлиста
        for item in self.playlist_videos['items']:
            id_video = item['contentDetails']['videoId']
            response = youtube.videos().list(part='statistics', id=id_video).execute()
            video_likes = int(response['items'][0]['statistics']['likeCount'])
            PlayList.video_ids_dict[id_video] = video_likes

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta`
        с суммарной длительность плейлиста"""
        video_ids = list(PlayList.video_ids_dict.keys())
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        total_second = 0

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_second += datetime.timedelta.total_seconds(duration)

        duration = datetime.timedelta(seconds=total_second)
        return duration

    @staticmethod
    def show_best_video():
        sorted_video_ids_dict = dict(sorted(PlayList.video_ids_dict.items(), key=lambda item: item[1], reverse = True))
        video_ids = list(sorted_video_ids_dict.keys())
        url_video = ('https://youtu.be/'+ str(video_ids[0]))
        return url_video
