import os
import yt_dlp

def downloadUser(archive_path, user_title):
    #seta o path da folder do user
    user_path = archive_path + user_title
    #see if the folder exist
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    #set url
    URL = 'https://www.tiktok.com/@' + user_title
    #get a dic of all videos with id and upload_date
    all_videos_id = getAllUserVideos(URL)

    videos_to_download = list({})
    ids_path = user_path + "/_ids"#path to folder with ids
    if os.path.isfile(ids_path):
        downloaded_videos = fileToList(ids_path)
        videos_to_download = getVideosToDownload(all_videos_id, downloaded_videos)
    else:
        f = open(ids_path, "x")
        f.close()
        videos_to_download = all_videos_id

    downloadUserVideos(videos_to_download, user_title, ids_path)
    # if videos_to_download:
    #     storageVideosDownloaded(videos_to_download, ids_path)

def getAllUserVideos(URl):
    videos_id = list({})
    # with yt_dlp.YoutubeDL() as ydl:
    #     info = ydl.extract_info(URl, download=False)
    info = yt_dlp.YoutubeDL().extract_info(URl, download=False)
    info_s = yt_dlp.YoutubeDL().sanitize_info(info)
    entries = info_s["entries"]
    for item in entries:
        video_info = {'id': item['id'], 'upload_date': item['upload_date']}
        videos_id.append(video_info)
    return videos_id

    # user_videos = ydl.extract_info(URL, download=False)
    # for v in user_videos:
    #     videos_id.append(v["id"])
    # return videos_id

def getVideosToDownload(all_videos_id, downloaded_videos):
    videos_to_download = list({})
    for video in all_videos_id:
        if not listContains(video['id'], downloaded_videos):
            videos_to_download.append({'id': video['id'], 'upload_date': video['upload_date']})
    return videos_to_download

def listContains(item, downloaded_videos):
    for itemd in downloaded_videos:
        if item == itemd:
            # print("item ja existe\n")
            return True
    return False

def fileToList(file_name):
    list_name = list(())
    f = open(file_name, "r")
    list_name = f.read().splitlines()
    f.close()
    return list_name

def downloadUserVideos(videos_to_download, user_title, ids_path):
    for video_id in videos_to_download:
        downloadVideo(video_id['id'], user_title)
        # video_path = user_title + "/" + video_id['upload_date'] + " - " + video_id['id'] + ".mp4"
        # if os.path.exists(video_path):
        #     print("Fui executado")
        #     print(video_path)
        #     videos_to_download.remove(video_id)
        storageVideoDownloaded(video_id['id'], ids_path)

def downloadVideo(video_id, user_name):
    command = "yt-dlp.exe https://www.tiktok.com/@" + user_name + "/video/" + video_id + " -o \"%(uploader)s/%(upload_date)s - %(id)s.%(ext)s\" -f \"(bv*+ba/b)[vcodec^=h264] / (bv*+ba/b)\""
    print(command)
    os.system(command)

def storageVideoDownloaded(video_id, ids_path):
    f = open(ids_path, "a")
    f.write(video_id)
    f.write("\n")
    f.close()

def storageVideosDownloaded(downloaded_videos, ids_path):
    downloaded_videos_ids = getAllIdsFromDic(downloaded_videos)
    f = open(ids_path, "a")
    for id in downloaded_videos_ids:
        f.write(id)
        f.write("\n")
    f.close()

def getAllIdsFromDic(dic):
    ids = list(())
    for item in dic:
        ids.append(item['id'])
    return ids