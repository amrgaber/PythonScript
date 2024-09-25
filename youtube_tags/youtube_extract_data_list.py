import json
import os
import pandas as pd
from pytube import Playlist, YouTube
from YoutubeTags import videotags
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')


def adjust_excel_formatting(writer, sheet_name):
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Set the column width and format
    worksheet.set_column('A:E', 20)

    # Set the row height
    for row in range(100):  # Adjust the range as needed
        worksheet.set_row(row, 15)


def build_youtube_service():
    return build('youtube', 'v3', developerKey=API_KEY)


def get_video_description(youtube, video_id):
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']['description']


def get_playlist_info(youtube, playlist_id, playlist_url):
    request = youtube.playlists().list(part="snippet", id=playlist_id)
    response = request.execute()
    snippet = response['items'][0]['snippet']
    channel_url = f"https://www.youtube.com/channel/{snippet['channelId']}"
    return {
        'Channel Title': snippet['channelTitle'],
        'Channel URL': channel_url,
        'Series Title': snippet['title'],
        'Series Desc': snippet['description'],
        'Series publishedAt': snippet['publishedAt'],
        'Series thumbnails': snippet['thumbnails'],
        'Series Tags': snippet.get('tags'),  # Some playlists may not have tags
        'Series URL': playlist_url
    }


def get_playlists(youtube, username):
    request = youtube.search().list(
        part="snippet", type="channel", q=username, maxResults=1)
    response = request.execute()
    if not response['items']:
        return []
    channel_id = response['items'][0]['id']['channelId']
    request = youtube.playlists().list(
        part="snippet", channelId=channel_id, maxResults=50)
    response = request.execute()
    playlist_urls = [
        f"https://www.youtube.com/playlist?list={item['id']}" for item in response['items']]
    return playlist_urls


def main():
    logging.info('Starting script...')
    youtube = build_youtube_service()
    # channel_lst = [''eman.S.khalifa', 'ajscriptmedia']
    # channel_lst = ['']
    channel_lst = ['Odoo Mates']
    # channel_lst_done = ['MuhammadNasserOfficial', 'Odoo Discussions','AJScript Media']
    all_data = []  # List to store data from all channels
    series_info = {}
    max_tags = 0
    # Initialize an empty dictionary to store the series tags
    series_tags = {}
    # Initialize an empty set to store the channel tags
    channel_tags = set()
    for channel in channel_lst:
        logging.info(f'Processing channel: {channel}')
        playlist_urls = get_playlists(youtube, channel)
        for i, playlist_url in enumerate(playlist_urls, 1):
            logging.info(f'Processing playlist: {playlist_url}')
            playlist = Playlist(playlist_url)
            video_urls = playlist.video_urls
            playlist_id = playlist_url.split('=')[-1]
            series_info = get_playlist_info(youtube, playlist_id, playlist_url)
            series_name = series_info['Series Title']  # Get the series name
            for url in video_urls:
                video = YouTube(url)
                title = video.title
                tags = videotags(url)
                desc = get_video_description(youtube, video.video_id)
                if isinstance(tags, str):
                    tags = tags.split(', ')

                all_data.append(list(series_info.values()) + [title, url, desc] + tags + [''] * (
                    max_tags - len(tags)))  # Append data to all_data list
                max_tags = max(max_tags, len(tags))  # Update max_tags

                # Add the tags to the set of unique tags for this series
                if series_name not in series_tags:
                    series_tags[series_name] = set()
                series_tags[series_name].update(tags)

                # Add the tags to the set of unique tags for this channel
                channel_tags.update(tags)

    # Convert the dictionary into a DataFrame
    series_tags_df = pd.DataFrame.from_dict(series_tags, orient='index')

    # Transpose the DataFrame so that the series names are columns
    series_tags_df = series_tags_df.transpose()

    # Convert the set of channel tags into a DataFrame
    channel_tags_df = pd.DataFrame(
        list(channel_tags), columns=['Channel Tags'])

    column_names = list(series_info.keys()) + ['Video Title', 'Video Url', 'Video Desc'] + [f'Tag_{i}' for i in
                                                                                            range(max_tags)]

    df = pd.DataFrame(all_data, columns=column_names)

    # Write the DataFrame to an Excel file with a single sheet
    with pd.ExcelWriter('AllChannels.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='All Channels', index=False)
        series_tags_df.to_excel(writer, sheet_name='Series Tags', index=False)
        channel_tags_df.to_excel(
            writer, sheet_name='Channel Tags All', index=False)

    logging.info('Script finished.')


if __name__ == "__main__":
    main()
