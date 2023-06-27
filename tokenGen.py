import spotipy
import spotipy.util as util

# Configurações do aplicativo do Spotify
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'  # URL de redirecionamento configurada no painel de desenvolvedor do Spotify

# Escopo de permissões necessárias
scope = 'playlist-modify-private playlist-modify-public'

# Autorização do usuário
username = '31tuzmptxe35k4slem47kafnjm2a'
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

print(token)
# Criação do objeto da API do Spotify
sp = spotipy.Spotify(auth=token)

# Utilize o objeto da API 'sp' para fazer chamadas à API do Spotify
# Aqui você pode implementar o código para manipular suas playlists e interagir com a API
