import spotipy
import spotipy.util as util
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    scope = 'user-library-read'
    token = util.prompt_for_user_token('Nixer', scope)
    sp = spotipy.Spotify(auth=token)

    '''Get full json data of specific playlist'''
    def get_playlist_tracks(username, playlist_id):
        results = sp.user_playlist_tracks(username, playlist_id)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        return tracks

    '''Process json data and return simple dictionaries'''
    def get_tracks_dic(tracks):
        result_dic = {}     # !dictionary: {album_name: {track_name: artist_name}}
        tracks_dic = {}     # dictionary: {track_name: album_name}
        artist_dic = {}     # !dictionary: {artist_name: album_name}
        images = {}         # !dictionary: {album_name: image_url}
        urls = {}           # !dictionary: {album_name: spotify_url}
        tracks_artist_dic = {}  # dictionary: {track_name: artist_name}
        tracks_temp = {}

        for i in range(len(tracks)):
            artist_dic[tracks[i]['track']['artists'][0]['name']] = tracks[i]['track']['album']['name']
            tracks_dic[tracks[i]['track']['name']] = tracks[i]['track']['album']['name']
            tracks_artist_dic[tracks[i]['track']['name']] = tracks[i]['track']['artists'][0]['name']
            images[tracks[i]['track']['album']['name']] = tracks[i]['track']['album']['images'][2]['url']
            urls[tracks[i]['track']['album']['name']] = tracks[i]['track']['album']['external_urls']['spotify']

        for key, value in artist_dic.items():
            for k, v in tracks_dic.items():
                if value == v:
                    tracks_temp[k] = tracks_artist_dic[k]
                    result_dic[value] = tracks_temp
            tracks_temp = {}

        result_dic = dict((key, value) for (key, value) in result_dic.items() if len(value) > 1)

        for key, value in artist_dic.items():
            if value in result_dic.keys():
                artist_dic[key] = value
            else:
                pass

        for key, value in images.items():
            if key in result_dic.keys():
                images[key] = value
            else:
                pass

        for key, value in urls.items():
            if key in result_dic.keys():
                urls[key] = value
            else:
                pass

        artist_dic = dict((key, value) for (key, value) in artist_dic.items() if len(value) > 1)

        switched_artist_dic = {artist_dic[k]: k for k in artist_dic}  # dictionary: {album_name: artist_name}
        artist_list_nospace = {k:v.replace(" ", "").replace("'", "").replace("&", "") for k, v in switched_artist_dic.items()}
        return switched_artist_dic, result_dic, images, urls, artist_list_nospace

    tracks_2016 = get_playlist_tracks('12135627614', '4TTuo9NoDRKXSRPJvQQEaE')
    tracks_2017 = get_playlist_tracks('12135627614', '6eyCzm6cWR733Hdv0p5tCW')
    switched_artist_dic_16, result_dic_16, images_16, urls_16, no_space_16 = get_tracks_dic(tracks_2016)
    switched_artist_dic_17, result_dic_17, images_17, urls_17, no_space_17 = get_tracks_dic(tracks_2017)
    return render_template('index.html', rdic16=result_dic_16, imurl16=images_16,
                           artist_dic_sw16=switched_artist_dic_16, urls16=urls_16, nsp16=no_space_16,
                           rdic17=result_dic_17, imurl17=images_17, artist_dic_sw17=switched_artist_dic_17,
                           urls17=urls_17, nsp17=no_space_17)


if __name__ == '__main__':
    app.run()
