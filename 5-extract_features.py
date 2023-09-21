import pandas as pd
import chess.pgn
import io
from tqdm import tqdm
tqdm.pandas()
import swifter
import numpy as np

def count_pieces(fen: str) -> dict:
    piece_count = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0, 'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0}

    fen_parts = fen.split()
    board_state = fen_parts[0]
    rows = board_state.split('/')
    
    # Define a lookup table to convert a piece character to its corresponding count key
    piece_lookup = {
        'K': 'K',
        'Q': 'Q',
        'R': 'R',
        'B': 'B',
        'N': 'N',
        'P': 'P',
        'k': 'k',
        'q': 'q',
        'r': 'r',
        'b': 'b',
        'n': 'n',
        'p': 'p'
    }
    
    for i, row in enumerate(rows):
        rank = 8 - i
        file = 0
        for chr in row:
            if chr.isnumeric():
                file += int(chr)
            else:
                piece_count[piece_lookup[chr]] += 1
                file += 1
    return piece_count

def extract_features_from_board(row: pd.Series) -> pd.Series:
    board = row['Board']
    
    # print(f"\n\n{row}\n\n")
    pieces_dict = count_pieces(board)
    # print(pieces_dict)
    for key, val in pieces_dict.items():
        row[key] = val
    return row


if __name__ == '__main__':
    INPUT_FILE_PATH = "/home/joao/workspace/lichess/datasets_csv/clean_classical_above_800_2023-01_2.csv"
    OUTPUT_FILE = "/home/joao/workspace/lichess/datasets_csv/ml_ready.csv"
    
    print(f"Reading file {INPUT_FILE_PATH}")
    df = pd.read_csv(INPUT_FILE_PATH, index_col=0, header=0)

    print(df.head())
    df.reset_index(drop=False, inplace=True)
    print(df.head())

    for col in ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']:
        df[col] = np.nan

    # result = df.progress_apply(extract_features_from_board, axis=1)
    # result = df.swifter.set_dask_scheduler('processes').set_npartitions(16).apply(extract_features_from_board, axis=1)
    # df = df.swifter.set_dask_scheduler('processes').set_npartitions(16).allow_dask_on_strings().apply(extract_features_from_board, axis=1)
    # df = df.swifter.allow_dask_on_strings().apply(extract_features_from_board, axis=1)
    print("Applying 'extract_features_from_board'")
    df = df.swifter.allow_dask_on_strings().apply(extract_features_from_board, axis=1)
    df.set_index('Id', inplace=True)
    print(df.head)
    
    print(f"Saving file {OUTPUT_FILE}")
    df.to_csv(OUTPUT_FILE)

    # fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    # print(count_pieces(fen))
