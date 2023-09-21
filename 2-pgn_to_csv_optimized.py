import pandas as pd
from tqdm import tqdm
import chess.pgn
import mmap
import csv
import os


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


def convert_pgn_to_csv(input_pgn_file_path: str, output_csv_file_path: str):
    rows = []

    # header = ['Event', 'Id', 'WhiteElo', 'BlackElo', 'Result', 'Termination', 'Moves']
    # rows.append(header)
    csv_header = None
    
    num_rows = 1
    print(f"Processing games from file {input_pgn_file_path}")

    # opens the file to read
    with open(input_pgn_file_path) as f:
        
        # opens the output file
        with open(output_csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            for _ in tqdm(range(get_number_of_games_in_pgn(input_pgn_file_path))):

                # Read a game from the PGN file
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                
                if csv_header is None:
                    csv_header = [x for x in game.headers]
                    csv_header.append('Moves')
                    rows.append(csv_header)
                    csv_header.remove('Moves')
                
                new_row = [
                    game.headers[x] for x in csv_header
                ]
                new_row.append(game.mainline_moves())

                rows.append(new_row)
                
                num_rows += 1

                # every time X rows are accumulated
                if num_rows == 100000:
                    print(f"Dumping 100000 rows into {output_csv_file_path}")
                    # dump rows to file
                    csv_writer.writerows(rows)

                    # resets rows to dump
                    num_rows = 0
                    rows = []

            # Write rows to CSV file
            print(f"Dumping {len(rows)} rows into {output_csv_file_path}")
            csv_writer.writerows(rows)
        
    print(f"Saved results to {output_csv_file_path}")

def main():
    BASE_FOLDER = '/mnt/e/Lichess DB/pgns_filtered'
    OUTPUT_FOLDER = '/mnt/e/Lichess DB/csvs_filtered'
    
    for pgn_file_name in tqdm(os.listdir(BASE_FOLDER)):
        print(pgn_file_name)
        INPUT_FILE = f'{BASE_FOLDER}/{pgn_file_name}'
        
        csv_file_name = pgn_file_name.replace('pgn', 'csv')
        OUTPUT_FILE = f'{OUTPUT_FOLDER}/{csv_file_name}'
        convert_pgn_to_csv(INPUT_FILE,OUTPUT_FILE)

        
# def main():
#     # num_processes = multiprocessing.cpu_count()
#     num_processes = 6
#     pool = multiprocessing.Pool(processes=num_processes)
    
#     BASE_FOLDER = '/mnt/e/Lichess DB/pgns_filtered'
#     OUTPUT_FOLDER = '/mnt/e/Lichess DB/csvs_filtered'
    
#     processes_to_run = []
#     for pgn_file_name in tqdm(os.listdir(BASE_FOLDER)):
#         print(pgn_file_name)
#         INPUT_FILE = f'{BASE_FOLDER}/{pgn_file_name}'
        
#         csv_file_name = pgn_file_name.replace('pgn', 'csv')
#         OUTPUT_FILE = f'{OUTPUT_FOLDER}/{csv_file_name}'
#         processes_to_run.append(multiprocessing.Process(target=convert_pgn_to_csv, args=(INPUT_FILE,OUTPUT_FILE)))

#     for process in processes_to_run:
#         process.start()

if __name__ == "__main__":
    main()
