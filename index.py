import os
from googleapiclient.discovery import build
import requests

API_KEY = 'Your youtube api key'


def download_thumbnail(url, output_dir, count):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_name = f"{count}.jpg"
        image_path = os.path.join(output_dir, image_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Téléchargement terminé : {image_path}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de la miniature : {e}")

def get_videos_with_views(keyword, num_videos):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    videos = []
    next_page_token = None

    while len(videos) < num_videos:
        search_response = youtube.search().list(q=keyword, part='id', maxResults=min(50, num_videos - len(videos)), type='video', pageToken=next_page_token).execute()
        
        for result in search_response['items']:
            video_id = result['id']['videoId']
            videos.append(video_id)
        
        if 'nextPageToken' in search_response:
            next_page_token = search_response['nextPageToken']
        else:
            break
    
    return videos[:num_videos]

def main():
    output_dir = 'thumbnails'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    keyword = input("Entrez un mot-clé pour la recherche de vidéos : ")
    num_videos = 1000

    videos = get_videos_with_views(keyword, num_videos)

    print(f"Téléchargement des miniatures des {len(videos)} vidéos avec au moins 1 million de vues.")

    for index, video in enumerate(videos, start=1):
        thumbnail_url = f"https://img.youtube.com/vi/{video}/maxresdefault.jpg"
        download_thumbnail(thumbnail_url, output_dir, index)

if __name__ == '__main__':
    main()