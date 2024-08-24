from django.conf import settings
# import requests
# import json
# import os
from textblob import TextBlob

import googleapiclient.discovery

def get_video_details(video_id):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBN0j5kuM_y_l0Gd8uI68XsBjWHNy1qz2E")
        return youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        ).execute()

def info(video_id):
    try:
        print(video_id)
        video_info = get_video_details(video_id)
        # print(video_info['items'])
        if 'items' in video_info and video_info['items']:
            item=video_info['items'][0]
            stats=item['statistics']
            vid_data={
                'id':item['id'],
                'title':item['snippet']['title'],
                'like_count': stats["likeCount"],
                'view_count':stats['viewCount'],
                'comment_count': stats["commentCount"],
                'channel_id' : item['snippet']['channelId'],
                'channel_name' : item['snippet']['channelTitle']
            }
            return vid_data
        else:
            return "Video not found."
    except Exception as e:
        return f"Error fetching video details: {str(e)}"

def senti(video_id):
    try:    
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBN0j5kuM_y_l0Gd8uI68XsBjWHNy1qz2E")
        request= youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        )
        comments=[]
        video_response=request.execute()
        for item in video_response['items']:
             comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
        return comments
    except:
        return []

def sentAnal(video_id):
     
     posi=0
     negi=0
     neut=0
     list=senti(video_id)

     for i in list:
          blob=TextBlob(i)
          if blob.sentiment.polarity > 0:
               posi+=1
          elif blob.sentiment.polarity < 0:
               negi+=1
          else :
               neut+=1
     sent={
          'posi':posi,
          'negi':negi,
          'neut':neut
     }
     return sent


































    # comment=[]
    # reply_count=[]
    # while video_response:
    #     for item in video_response['items']:
    #         comment.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
    #         reply_count.append(item['snippet']['totalReplyCount'])
    #     # print(comment)
    #     if 'nextPageToken' in video_response:
    #         video_response = youtube.commentThreads().list(
    #             part='snippet,replies',
    #             videoId=video_id,
    #             pageToken=video_response['nextPageToken'],
    #             maxResults=100
    #         ).execute()
    #     else:
    #         break
    # return comment
        
# print(senti("9DAKh_XCk6g"))
# print(info(video_id))  