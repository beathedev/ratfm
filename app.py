from flask import Flask, render_template
import requests
import json
from google_images_search import GoogleImagesSearch

#google
api_key_google = ""
cx=""

#lastfm
api_key = ''
user = ''


app = Flask(__name__)

@app.route('/')
def index():

    url = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&format=json&limit=5'
    url2 = f'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={user}&api_key={api_key}&limit=1&period=1month&format=json'

    response = requests.get(url)
    if response.ok:
        data = response.json()
        tracks = data['recenttracks']['track']

        response2 = requests.get(url2)
        data2 = response2.json()
        track_info = data2['toptracks']['track'][0]
        artist_name = track_info['artist']['name']
        track_name = track_info['name']
        artist_image = track_info['image'][-1]['#text']
        
        query = artist_name + " " + track_name + "album cover"
        num_images = 1


        # Pesquisa a imagem no google        
        url3 = f'https://customsearch.googleapis.com/customsearch/v1?cx={cx}&q={query}&searchType=image&num=1&start=1&safe=off&key={api_key_google}'
        response3 = requests.get(url3)

        if response3.status_code == 200:
            # A resposta é bem sucedida. Parseie a resposta JSON.
            json_response3 = response3.json()
            if 'items' in json_response3:
                # Há pelo menos um item de resultado. Acesse a URL da imagem.
                image_url = json_response3['items'][0]['link']
                print(image_url)
            else:
                # Não há resultados de pesquisa disponíveis.
                print('Nenhum resultado encontrado.')
                image_url = "Não tem"
        else:
        # A resposta não é bem sucedida.
            print(f'Erro na solicitação: {response3.status_code}')

        return render_template('index.html', tracks=tracks, artist_name=artist_name, artist_image=artist_image, track_name=track_name, image_url=image_url, user=user)

if __name__ == '__main__':
    app.run(host='192.168.0.8')


    
