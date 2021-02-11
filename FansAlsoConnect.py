import tekore as tk
import networkx as nx

client_id = 'dff21b856c2f4618a94b22a44c8c0a6f'
client_secret = '9995bff098c64c85bb99477c89a8a468'

token = tk.request_client_token(client_id, client_secret)

# Too Door Cinema Club: 536BYVgOnRky0xjsPT96zl

spotify = tk.Spotify(token)
album = spotify.album('3RBULTZJ97bvVzZLpxcB0j')
for track in album.tracks.items:
    print(track.track_number, track.name)

