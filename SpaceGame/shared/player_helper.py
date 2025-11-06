import os

def load_player_names(settings):
    player_dir = settings['PLAYER_DIRECTORY']

    player_names = []
    for filename in os.listdir(player_dir):
        player_name = os.path.splitext(filename)[0]
        player_names.append(player_name)
    return player_names

def add_players_to_settings(player_names : list[str], settings):
    for player in player_names:
        settings.add_player(player, None)