import requests

print('Get Data')

response = requests.get('https://accounts.spotify.com/authorize', [('client_id', '9b45ca0d11584648ae1a46fd50c1fd61'),
                        ('redirect_uri', 'localhost:8000')])
response.headers()