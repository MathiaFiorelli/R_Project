import numpy as np
import pandas as pd
from itertools import product

game_coord = {'p1': np.array([1, 0, 0, 1]).reshape((2, 2)),
              'p2': np.array([1, 0, 0, 1]).reshape((2, 2))}
game_prison = {"p1": np.array([5, 1, 10, 2]).reshape((2, 2)),
               "p2": np.array([5, 10, 1, 2]).reshape((2, 2))}
game_anticoord = {'p1': np.array([0, 1, 1, 0]).reshape((2, 2)),
                  'p2': np.array([0, 1, 1, 0]).reshape((2, 2))}
game_stag = {'p1': np.array([3, 2, 0, 2]).reshape((2, 2)),
             'p2': np.array([3, 0, 2, 2]).reshape((2, 2))}
coord4 = {'p1': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape((2, 2, 2, 2)),
          'p2': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape((2, 2, 2, 2)),
          'p3': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape((2, 2, 2, 2)),
          'p4': np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]).reshape((2, 2, 2, 2))}

games = {'Coordination 2p': game_coord,
         'Prison': game_prison,
         'Anticoordination 2p': game_anticoord,
         'Stag-Hare': game_stag,
         'Coordination 4p': coord4}


def nash(game):
    game_flat = {f'{key} value': value.flatten() for key, value in game.items()}
    change_columns = [f'{p} change' for p in game.keys()]

    strategies = {}
    for i, p in enumerate(game.keys()):
        strategies[p] = np.arange(game[p].shape[i])

    str_combo = pd.DataFrame(product(*strategies.values()), columns=game.keys())

    df = pd.DataFrame(game_flat)
    str_combo = pd.concat([str_combo, df], axis=1)
    str_combo[change_columns] = 0

    for index, row in str_combo.iterrows():
        for player in game.keys():
            # Other players
            other_players = list(game.keys())
            other_players.remove(player)
            # Other values with the same other players' strategies
            other_players_str = row[other_players].tolist()
            condition = (str_combo[other_players] == other_players_str).all(axis=1)
            player_values = str_combo.loc[condition, f'{player} value'].tolist()
            player_values_bool = [x > row[f'{player} value'] for x in player_values]
            #print(player,player_values,row[f'{player} value'],player_values_bool)
            # Check if other players might want to change their strategies to accomodate his will
            str_combo.loc[index, f'{player} change'] = any(player_values_bool)

    str_combo['Nash'] = ~str_combo[change_columns].any(axis=1)
    return str_combo.loc[str_combo['Nash']]


for name, game in games.items():
    print(name)
    print(nash(game))
