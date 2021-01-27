from googleapiclient.discovery import build

api_key= "< Paste the Google API Key here >"
youtube = build("youtube","v3", developerKey=api_key)

## Copy the URL of any Yotube video paste it in the "url" variable to get the stats of the channel that published the video.
url="< Paste the URL of a Youtube video >"

## Splitting the channel_id from the video URL that was provided on the "url" variable.
single_video_id = url.split("=")[1].split("&")[0]
channel_id= youtube.videos().list(part="snippet",id=single_video_id).execute()["items"][0]["snippet"]["channelId"]

#Get the "Upload" playlist. This playlist includes all the videos of the channel.
upload = str(youtube.channels().list(
    part="contentDetails",
    id= channel_id
    ).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"])

#Basic Information of the Channel
channel_stats = youtube.channels().list(
    part=["statistics","snippet"],
    id=channel_id
    ).execute()


## View Counts
number_of_views= int(channel_stats["items"][0]["statistics"]["viewCount"])

## Number of Videos in the Channel
number_of_videos= int(channel_stats["items"][0]["statistics"]["videoCount"])

## Approx. Number of Subsribers
amount_of_subscribers= int(channel_stats["items"][0]["statistics"]["subscriberCount"])

## Title of the Channel
title_of_channel = channel_stats["items"][0]["snippet"]["title"]

## Time of Existance
created_at= channel_stats["items"][0]["snippet"]["publishedAt"]

## Print the Stats of the channel.
print(f"Name of the channel: {title_of_channel}")
print(f"Created On: {created_at}")
print(f"{'{:,}'.format(number_of_views)} total views.") 
print(f"{'{:,}'.format(number_of_videos)} published videos.")
print(f"{'{:,}'.format(amount_of_subscribers)} subscribers.")

