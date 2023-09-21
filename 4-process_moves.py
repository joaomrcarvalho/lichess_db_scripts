import pandas as pd
import chess.pgn
import io
import swifter

INPUT_FILE_PATH = "/home/joao/workspace/lichess/datasets_csv/clean_classical_above_800_2023-01.csv"
OUTPUT_FILE = "/home/joao/workspace/lichess/datasets_csv/clean_classical_above_800_2023-01_2.csv"

print(f"Reading file {INPUT_FILE_PATH}")
df = pd.read_csv(INPUT_FILE_PATH, index_col=0, header=0)

print("Filtering records based on ELO criteria")
df = df[(df['WhiteElo'] <= 1000) & (df['BlackElo'] <= 1000)]

# mask = df.index.duplicated(keep=False)
# duplicates = df.index[mask].tolist()
# print(len(duplicates))
# print(len(mask))
# exit(0)

# define custom function to transform each row into one row per move available from the PGN
def process_row(row: pd.Series):
    moves = row['Moves']
    dict_result = {'Id': [], 'MoveNumber': [], 'WhiteElo': [], 'BlackElo': [], 'Result': [], 'Board':[]}

    pgn = chess.pgn.read_game(io.StringIO(moves))
    board = pgn.board()

    move_number = 0
    for move in pgn.mainline_moves():
        dict_result['Id'].append(f"{row['Id']}-{move_number}")
        dict_result['MoveNumber'].append(move_number)
        move_number += 1
        dict_result['WhiteElo'].append(row['WhiteElo'])
        dict_result['BlackElo'].append(row['BlackElo'])
        dict_result['Result'].append(row['Result'])
        dict_result['Board'].append(board.fen())
        board.push(move)
        # print(board.fen(), move)
    return pd.DataFrame(dict_result)


print('Processing each game and transforming into "expanded" dataset')
# apply custom function to each row in dataframe and concatenate results
print(df.head())
df.reset_index(drop=False, inplace=True)
print(df.head())
result = pd.concat(df.swifter.apply(process_row, axis=1).tolist(), ignore_index=True).set_index('Id')
print(result.head())
print(f"Saving file {OUTPUT_FILE}")
result.to_csv(OUTPUT_FILE)