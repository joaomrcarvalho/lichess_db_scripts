import pandas as pd
from tqdm import tqdm
import chess.pgn
import mmap
import csv


def get_number_of_games_in_pgn(pgn_file: str) -> int:
    num_games = 0

    with open(pgn_file, "r") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            while True:
                event_pos = mm.find(b"[Event ")
                result_pos = mm.find(b"[Result ")
                if event_pos == -1 and result_pos == -1:
                    break
                elif event_pos != -1 and (event_pos < result_pos or result_pos == -1):
                    num_games += 1
                    mm.seek(event_pos + 1)
                else:
                    mm.seek(result_pos + 1)

    return num_games

def main():
    INPUT_PGN = "/home/joao/workspace/lichess/datasets_pgn_filtered/classical_above_800_2023-01.pgn"
    OUTPUT_CSV = "/home/joao/workspace/lichess/datasets_csv/classical_above_800_2023-01.csv"
    csv_file = open(OUTPUT_CSV, 'w', newline='')
    csv_writer = csv.writer(csv_file)

    header = ['Event', 'Id', 'WhiteElo', 'BlackElo', 'Result', 'Termination', 'Moves']
    csv_writer.writerow(header)

    print(f"Processing games from file {INPUT_PGN}")
    with open(INPUT_PGN) as f:
        for _ in tqdm(range(get_number_of_games_in_pgn(INPUT_PGN))):
        # Read a game from the PGN file
            game = chess.pgn.read_game(f)
            if game is None:
                break
            
            csv_writer.writerow([
                game.headers['Event'],
                game.headers['Site'],
                game.headers['WhiteElo'],
                game.headers['BlackElo'],
                game.headers['Result'],
                game.headers['Termination'],
                game.mainline()
            ])

    csv_file.close()
    
if __name__ == "__main__":
    main()