from django.conf import settings
from textblob import TextBlob
import googleapiclient.discovery
from django.core.mail import send_mail
from MovieReview import settings
from .models import User
import random

def get_video_details(video_id):
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBN0j5kuM_y_l0Gd8uI68XsBjWHNy1qz2E")
        return youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        ).execute()

def info(video_id):
    try:
        video_info = get_video_details(video_id)
        # print(video_info)
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
                'channel_name' : item['snippet']['channelTitle'],
                'tags':item['snippet']['tags'],
                'discription':item['snippet']['description'][:2000],
                'thumbnail':item['snippet']['thumbnails']['medium']['url']
            }
            return vid_data
        else:
            return "Video not found."
    except Exception as e:
        return f"Error fetching video details: {str(e)}"
# print(info("C-6Dhsi_Yb0"))
def senti(video_id):
    try:    
        youtube =googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBN0j5kuM_y_l0Gd8uI68XsBjWHNy1qz2E")
        request= youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            textFormat='plainText',
            maxResults=1000
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



def senEmail(email):
    uname=User.objects.get(gmail=email)
    try:
     num=random.randint(1000,9999)
     
     uname.otp=num
     uname.save()
     subject="Your One-Time Password (OTP)"
     message=f"""Hello,

    Your OTP for account verification is:{num}.

    Thank you for using our service!

    Regards,
    VidStats"""
     from_email=settings.EMAIL_HOST_USER
     recipient_list=[email]
     send_mail(subject,message,from_email,recipient_list)
    except Exception as e:
        print(e)
































































# def get_video(channel_id):
#     youtube=googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBN0j5kuM_y_l0Gd8uI68XsBjWHNy1qz2E")
#     res=youtube.channels().list(id=channel_id,part='contentDetails').execute()
#     playlist=res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#     video=[]
#     next_page_token=None
    
#     while 1:
#         res=youtube.playlistItems().list(
#             playlistId=playlist,
#             part='snippet',
#             maxResults=100,
#             pageToken=next_page_token
#             ).execute()
        
#         video+=res['items']
#         next_page_token=res['nextPageToken']
#         if next_page_token is None:
#             break 
        
#     return video
# def channel(channel_name):
#     youtube=googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyBN0j5kuM_y_l0Gd8uI68XsBjWHNy1qz2E")
#     request=youtube.channels().list(
#           part='statistics',
#           forUsername=channel_name
#     )
#     response=request.execute()
    # viewcount=response['items'][0]['statistics']['viewCount']
    # subs=response['items'][0]['statistics']['subscriberCount']
    # vid_count=response['items'][0]['statistics']['videoCount']
    # channel_id=response['items'][0]['id']
    # video=get_video(channel_id)
    # idList=id(video)
    # viewList=[]
    
    # print(idList)
    # print(response)
    

# channel('aajtak')