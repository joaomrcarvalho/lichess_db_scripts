import re
from tqdm import tqdm
import subprocess
import os


def get_number_of_lines(file_path: str) -> int:
    print(f"Checking number of lines of file {file_path}")
    command = ["wc", "-l", file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    line_count = int(output.split()[0])
    print(f"The file '{file_path}' has {line_count} lines.")
    return line_count

def process_game(game_text):
    global filtered_games
    event_pattern = re.compile(r'\[Event "(.*)"\]')
    event_match = event_pattern.search(game_text)
    if event_match:
        try:
            event = event_match.group(1)
            elo_pattern = re.compile(r'\[(White|Black)Elo "(.*)"\]')
            white_elo_match = elo_pattern.search(game_text, 0)
            black_elo_match = elo_pattern.search(game_text, white_elo_match.end())
            # if (event == "Rated Classical game" or event == "Rated Rapid game") and \
            # if (event == "Rated Rapid game") and \
            # if (event == "Rated Classical game") and \
            if (event == "Rated Classical game" or event == "Rated Rapid game" or event == 'Rated Blitz game') and \
            white_elo_match and black_elo_match and \
            MIN_ELO <= int(white_elo_match.group(2)) < MAX_ELO and MIN_ELO <= int(black_elo_match.group(2)) < MAX_ELO:
                filtered_games.append(game_text)
                # return game_text

        except:
            global SKIPPING_GLOBAL
            SKIPPING_GLOBAL += 1


def main():
    num_lines = get_number_of_lines(pgn_file)
    chunk_size = int(102400000 / 3)
    total_games = 0  
    global filtered_games
    filtered_games = []

    with open(pgn_file) as f:
        print("Opening file to process")
        game_lines = []
        output_lines_number = 0
        for chunk_start in tqdm(range(0, num_lines, chunk_size)):
            # print(f"Have found {len(filtered_games)} that match the criteria, so far")
            chunk_end = min(chunk_start + chunk_size, num_lines)
            f.seek(chunk_start)

            for _ in range(chunk_end - chunk_start):
                line = f.readline()
                if line.startswith("[Event "):
                    # process the previous game
                    if game_lines:
                        game_text = "".join(game_lines)
                        process_game(game_text)
                        output_lines_number += 1
                    game_lines = [line]
                else:
                    game_lines.append(line)

            # Write the filtered games to a new PGN file
            print("Writing chunk to output file")
            with open(OUTPUT_FILE, "a") as f_out:
                f_out.write("\n\n".join(filtered_games))
            total_games += len(filtered_games)
            filtered_games = []
            
        # process the last game
        if game_lines:
            game_text = "".join(game_lines)
            process_game(game_text)
            output_lines_number += 1
            
    # Write the last game to the PGN filtered file
    print("Writing last game to output file")
    with open(OUTPUT_FILE, "a") as f_out:
        f_out.write("\n\n".join(filtered_games))
    total_games += len(filtered_games)

    print(f"Output file has {total_games} games that matched the criteria.")
    print(f"Skipped {SKIPPING_GLOBAL}")



if __name__ =='__main__':
    MIN_ELO = 1
    MAX_ELO = 10000
    BASE_FOLDER = '/mnt/e/Lichess DB/pgns_uncompressed'
    OUTPUT_FOLDER = '/mnt/e/Lichess DB/pgns_filtered'
    for pgn_file_name in tqdm(os.listdir(BASE_FOLDER)):
        print(pgn_file_name)
        OUTPUT_FILE = f'{OUTPUT_FOLDER}/filtered_{pgn_file_name}'
        SKIPPING_GLOBAL = 0
        pgn_file = f'{BASE_FOLDER}/{pgn_file_name}'
        main()
    
   