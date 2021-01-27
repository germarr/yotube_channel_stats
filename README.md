# Youtube Channel Key Stats

This script is part of my research project called "What Topics Drives Youtube MX?". You can check the whole project [**here**](https://gmarr.com/).

The main purpose of this code is to get the most relevant statistics from any youtube channel. This is the first building block of a larger project that looks to get the most relevant statistics of all the videos that are published in a Youtube channel and export the result to a CSV. You can find the final version of the script [**here**]("").

Here's an example of the final result you can get after running the script:

```python
url_of_a_yotube_video = "https://www.youtube.com/watch?v=WNUtEAFiDE8"

Name of the channel: PewDiePie
Created On: 2010-04-29T10:54:00Z
26,863,436,311 total views.
4,282 published videos.
108,000,000 subscribers.
```

## **Tutorial**
---
### <ins>**1. General Concepts**</ins>
To follow the code in this tutorial I would recommend to have some knowledge of the next concepts:
* Python
    * `for` loops
    * functions
    * pip. 
        * [Here](https://realpython.com/what-is-pip/) you can find a really good article that expalins what is pip.
    * pandas. 
        * [This](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html) is a gentle introduction to the pandas library.
* JSON
    * The general structure of a JSON file
* API's
    * Specifically, the tutorial is going to make more sense if you know what is an API Key. To learn more about API's I recommend to watch this [video](https://www.youtube.com/watch?v=GZvSYJDk-us&t=4641s). The video shows the inner workings of the [Trello API](https://developer.atlassian.com/cloud/trello/rest/) however, the concepts that are shown can be applied to any API. This is my "go-to" reference guide when I'm stucked.

If you do not know how any of this concepts work I added resources troughout the tutorial so you can revised them at your own pace.

### <ins>**2. The Set Up**</ins>
In addition to the concepts mentioned above, before you start the tutorial be sure to have:

* A Youtube API Key
    * In order to retrieve the data from Youtube we're going to use the [Youtube API](https://developers.google.com/youtube/v3). All the API's from Google properties require a Google Account and autorization credentials.
    * To learn how to setup a Google Account and get this credentials you can follow this [tutorial](https://developers.google.com/youtube/registering_an_application).
    * Once you have your credentials, you need to request an API Key. You can follow [this instructions](https://cloud.google.com/resource-manager/docs/creating-managing-projects?visit_id=637472330160631271-1024614839&rd=1) to get your API Key.
    * If you want additional information about the API setup, Youtube offers a nice introduction [here](https://developers.google.com/youtube/v3/getting-started).
* A Code Editor
    * I use VS Code. You can download it [here](https://code.visualstudio.com/).
* Python
    * If you use a Mac you already have Python installed. If you use a Windows PC or Linux, you can download Python [here]("").
    * The `pandas` library. You can download it from [here](https://pandas.pydata.org/).

### <ins>**3. The Code**</ins>


1. Download the [google python client](https://github.com/googleapis/google-api-python-client) via pip. 

```python
pip install google-api-python-client
```
2. Import the “build” function from the Google Python Client. This function helps to abstract a lot of the code needed to use the Youtube API.

```python
from googleapiclient.discovery import build
```
3. Get your API Key from the [Google Developer Console](https://console.developers.google.com/) and copy it. 
4. Create a variable called `api_key` and paste the API Key that you copied from the Google Developer Console. Then create a variable called `youtube` and assign it the `build()` function with the parameters
 `youtube`, `v3` and `developerKey = api_key`

```python
api_key= "<Paste your API KEY here>"

youtube = build("youtube","v3", developerKey=api_key)
```

* [Here](https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.discovery-module.html#build) you can learn all the arguments that can be used in the `build()` function.
* I would also recommend to check all the different methods that the youtube API can use. You can find them [here](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html).


5. In addition to the variables we just created, to get the channel data we need acces to the `channel_id`. This piece of data will help us to get access to the channel data. To get it, is a three step process. First,  we need the url of any video that is published by a channel. Second, we split this url to get a piece of data that this url has. Third,  pass this result into an API call to Youtube and get the `channel_id`. 

```python
## Copy the URL of any Yotube video paste it in the "url" variable to get the stats of the channel that published the video.
url="< Paste the URL of a Youtube video >"

## Splitting the channel_id from the video URL that was provided on the "url" variable.
single_video_id = url.split("=")[1].split("&")[0]
```

6. To continue, we’re going to use the `videos()` method inside the `build()` function that we created. [Here]("https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html") you can find all the methods that can be used on `video()`. For this tutorial we’re going to use the `list()` method. [Here]("https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html#list") are all the parameters that can be used inside `list()`. By passing the `id` we got from the url splitting into this new function, we can finally get access to the `channel_id`. We're storing the result in a variable called `channel_id`.

```python
# part is a required parameter to make this method work. 
# Inside this parameter you can specify the resources you want the API to return. In this case we want to return "snippet" 
# Fore more information check the documentation that I shared for the list() method.
channel_id= youtube.videos().list(part="snippet",id=single_video_id).execute()["items"][0]["snippet"]["channelId"]

```

7. Once we have the `channel_id` we can continue our script. We’re going to use the `channels()` method inside the `build()` function that we created. [Here](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.channels.html) you can find all the methods that can be used on `channels()`. We’re going to use the `list()` method again. [Here](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.channels.html#list) are all the parameters that can be used inside `list()` when applied to the `channels()` method.


```python
# Key Stats of the Channel
# Part is a required parameter to make this method work.
# Fore more information check the documentation that I shared for the list() method.

channel_stats = youtube.channels().list(
    part=["statistics","snippet"],
    id=channel_id
    ).execute()
```

8. Now we have everything in place to get access to the main stats of a channel. The final step is just to print the results,in a way that makes sense to us, by splitting the JSON that we have in the `channel_stats` variable. If we print the variable `channel_stats` at this point, this is the result:

```javascript
{'kind': 'youtube#channelListResponse',
 'etag': 'WxjFActm0jKb9WzgVntykjTp_-0',
 'pageInfo': {'totalResults': 1, 'resultsPerPage': 5},
 'items': [{'kind': 'youtube#channel',
   'etag': '5bJvClFkoiNxHjCXpMaOtdwEW_A',
   'id': 'UC-lHJZR3Gqxm24_Vd_AJ5Yw',
   'snippet': {'title': 'PewDiePie',
    'description': 'I make videos.',
    'publishedAt': '2010-04-29T10:54:00Z',
    'thumbnails': {'default': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnicjOV8f1wuuYluOYqL4SEYE3PbxaVYK6_ODp5a6g=s88-c-k-c0x00ffffff-no-rj',
      'width': 88,
      'height': 88},
     'medium': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnicjOV8f1wuuYluOYqL4SEYE3PbxaVYK6_ODp5a6g=s240-c-k-c0x00ffffff-no-rj',
      'width': 240,
      'height': 240},
     'high': {'url': 'https://yt3.ggpht.com/ytc/AAUvwnicjOV8f1wuuYluOYqL4SEYE3PbxaVYK6_ODp5a6g=s800-c-k-c0x00ffffff-no-rj',
      'width': 800,
      'height': 800}},
    'localized': {'title': 'PewDiePie', 'description': 'I make videos.'},
    'country': 'US'},
   'statistics': {'viewCount': '26863436311',
    'subscriberCount': '108000000',
    'hiddenSubscriberCount': False,
    'videoCount': '4282'}}]}
```

9. Here's an example of how I splitted the JSON stored in `channel_stats`

```python
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
```
10. Here's an example of the entire code we build troughout this tutorial:
```python
from googleapiclient.discovery import build

api_key= "< Paste the Google API Key here >"

youtube = build("youtube","v3", developerKey=api_key)

url="< Paste the URL of a Youtube video >"

single_video_id = url.split("=")[1].split("&")[0]
channel_id= youtube.videos().list(part="snippet",id=single_video_id).execute()["items"][0]["snippet"]["channelId"]

channel_stats = youtube.channels().list(
    part=["statistics","snippet"],
    id=channel_id
    ).execute()


number_of_views= int(channel_stats["items"][0]["statistics"]["viewCount"])

number_of_videos= int(channel_stats["items"][0]["statistics"]["videoCount"])

amount_of_subscribers= int(channel_stats["items"][0]["statistics"]["subscriberCount"])

title_of_channel = channel_stats["items"][0]["snippet"]["title"]

created_at= channel_stats["items"][0]["snippet"]["publishedAt"]

print(f"Name of the channel: {title_of_channel}")
print(f"Created On: {created_at}")
print(f"{'{:,}'.format(number_of_views)} total views.") 
print(f"{'{:,}'.format(number_of_videos)} published videos.")
print(f"{'{:,}'.format(amount_of_subscribers)} subscribers.")
```





