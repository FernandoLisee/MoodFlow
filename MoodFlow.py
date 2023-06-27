import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Configurações da API do Spotify
SCOPE = "playlist-modify-public"
USERNAME = "2232xa42crdx3lqbjb5rsefqq"  # Substitua pelo seu nome de usuário do Spotify
CLIENT_ID = "69676a7e57da46c7a2dfc61c60e8b48f"  # Substitua pelo seu client ID do Spotify
CLIENT_SECRET = "s22ce0186bbf746bab7bb9c7127e2d761"  # Substitua pelo seu client secret do Spotify
REDIRECT_URI = "http://localhost:8888/callback"  # URL de redirecionamento

## Autenticar na API do Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Função para analisar o sentimento
def analisar_sentimento(texto):
    blob = TextBlob(texto, analyzer=NaiveBayesAnalyzer())

    if blob.sentiment.classification == 'pos':
        return 'positivo'
    elif blob.sentiment.classification == 'neg':
        return 'negativo'
    else:
        return 'neutro'

# Função para buscar e retornar uma playlist do Spotify por gênero
def buscar_playlist_por_genero(genero):
    results = sp.search(q=f"genre:'{genero}'", type='playlist', limit=1)
    playlists = results['playlists']['items']

    if playlists:
        playlist = playlists[0]
        return playlist['id']
    else:
        return None

# Função para criar uma playlist personalizada com base no sentimento
def criar_playlist_personalizada(sentimento):
    if sentimento == 'positivo':
        genero = 'pop'
    elif sentimento == 'negativo':
        genero = 'rock'
    else:
        genero = 'edm'

    playlist_id = buscar_playlist_por_genero(genero)

    if playlist_id:
        playlist_nome = f"Playlist {sentimento.capitalize()}"
        sp.user_playlist_create(user='seu_username', name=playlist_nome, public=True)
        sp.user_playlist_add_tracks(user='seu_username', playlist_id=playlist_id, tracks=['spotify:track:track_id'])
        print(f"A playlist '{playlist_nome}' foi criada com sucesso!")
    else:
        print("Não foi possível encontrar uma playlist correspondente ao gênero desejado.")

# Função principal
def main():
    # Entrada do usuário
    frase = input("Digite a frase para analisar o sentimento: ")

    # Analisar o sentimento
    sentimento = analisar_sentimento(frase)

    # Resposta baseada no sentimento
    if sentimento == 'positivo':
        resposta = "Que ótimo! Tenha um dia maravilhoso!"
    elif sentimento == 'negativo':
        resposta = "Sinto muito em ouvir isso. Espero que seu dia melhore em breve."
    else:
        resposta = "Fico feliz em saber que você está se sentindo neutro hoje."

    # Exibir a resposta
    print(resposta)

    # Criar playlist personalizada com base no sentimento
    criar_playlist_personalizada(sentimento)

if __name__ == '__main__':
    main()