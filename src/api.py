
import requests

# Chess API endpoints
CHESS_API_BASE_URI = 'https://api.chess.com'
CHESS_API_PUB = f'{CHESS_API_BASE_URI}/pub'


def get_leaderboard_data(game_type=None):
    '''
    Requests the leaderboard data from chess.com api
    '''
    data = (requests.get(f'{CHESS_API_PUB}/leaderboards')).json()
    if game_type:
        return data[game_type]
    return data


def get_player_by_username(username):
    '''
    Returns the player profile details from chess.com api
    '''
    return (requests.get(f'{CHESS_API_PUB}/player/{username}')).json()


def get_streamers():
    '''
    Returns a list of streamers
    {
         "username": "string",
         "avatar": "URL",
         "twitch_url": "Twitch.tv URL",
         "url":"member url's"
      }
    '''
    response = requests.get(f'{CHESS_API_PUB}/streamers')
    response_dict = response.json()
    streamers = response_dict['streamers']
    return streamers
