import spotipy
import spotipy.util as util
import json

scope = 'user-library-read'
token = util.prompt_for_user_token('Nixer', scope)
sp = spotipy.Spotify(auth=token)


def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def get_tracks_dic(tracks):
    file_tracks = open("pl.txt", "w")
    file_tracks_temp = open("pl_temp.txt", "w")

    result_dic = {}
    tracks_dic = {}
    artist_dic = {}
    images = {}
    urls = {}
    tracks_artist_dic = {}
    tracks_temp = {}

    for i in range(len(tracks)):
        artist_dic[tracks[i]['track']['artists'][0]['name']] = tracks[i]['track']['album']['name']
        tracks_dic[tracks[i]['track']['name']] = tracks[i]['track']['album']['name']
        tracks_artist_dic[tracks[i]['track']['name']] = tracks[i]['track']['artists'][0]['name']
        images[tracks[i]['track']['album']['name']] = tracks[i]['track']['album']['images'][2]['url']
        urls[tracks[i]['track']['album']['name']] = tracks[i]['track']['album']['external_urls']['spotify']

    file_tracks_temp.write(json.dumps(urls, indent=4))

    for key, value in artist_dic.items():
        for k, v in tracks_dic.items():
            if value == v:
                tracks_temp[k] = tracks_artist_dic[k]
                result_dic[value] = tracks_temp
        tracks_temp = {}

    file_tracks.write(json.dumps(result_dic, indent=4))
    file_tracks.close()


tracks_2016 = get_playlist_tracks('12135627614', '4TTuo9NoDRKXSRPJvQQEaE')
get_tracks_dic(tracks_2016)

# for i in range(0, len(tracks)):
#     # file_temp.write(json.dumps(tracks[i]['track'], indent=4))
#     # if tracks[i]['track']['album']['name'] != album_temp_name:
#     #     file_tracks.write(tracks[i]['track']['artists'][0]['name'] + " - " + tracks[i]['track']['album']['name'] + "\n")
#     # else:
#     #     pass
#     # album_temp_name = tracks[i]['track'  ]['album']['name']
#     # file_tracks.write("\t" + tracks[i]['track']['name'] + "\n")\
#     if tracks[i]['track']['album']['name'] != album_temp_name:
#         tracks_dic = {}
#         tracks_list = []
#     else:
#         tracks_list.append(tracks[i]['track']['name'])
#         # if tracks[i]['track']['artists'][0]['name'] == artist_temp_name or (artist_temp_name in tracks[i]['track']['artists'][0]['name']):
#         tracks_dic[tracks[i]['track']['artists'][0]['name']] = tracks_list
#         # else:
#         #     pass
#     # artist_temp_name = tracks[i]['track']['artists'][0]['name']
#     album_temp_name = tracks[i]['track']['album']['name']
#     result_dic[tracks[i]['track']['album']['name']] = tracks_dic
# print(result_dic)
# file_tracks.write(json.dumps(result_dic, indent=4))
