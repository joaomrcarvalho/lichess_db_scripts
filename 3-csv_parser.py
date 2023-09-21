import pandas as pd
from tqdm import tqdm
import numpy as np

def clean_pgn_mainline(pgn_mainline: str) -> str:
    if(type(pgn_mainline) != str):
        print(f"{pgn_mainline} of type {type(pgn_mainline)}")
        return ""
    else:
        return pgn_mainline


def replace_question_mark_with_na(value: str) -> str:
    if '?' in value:
        return 0
    else:
        return int(value)

def replace_winner_by_int(value: str) -> int:
    if value == '1-0':
        return 0
    if value == '0-1':
        return 1
    # value == '1/2-1/2'
    else:
        return 2       

def main():
    INPUT_CSV = "/home/joao/workspace/lichess/datasets_csv/classical_above_800_2023-01.csv"
    OUTPUT_CSV = "/home/joao/workspace/lichess/datasets_csv/clean_classical_above_800_2023-01.csv"

    print(f"Reading file {INPUT_CSV}")
    
    df = pd.read_csv(INPUT_CSV, index_col=1, header=0)
    print(df.info())
    
    # not interested in 'Time forfeit' games
    df = df[df['Termination'] == 'Normal']

    # if all games are from the same type of event, no need to keep it
    df.drop(columns=['Termination', 'Event'], inplace=True)

    # df['WhiteElo'] = df['WhiteElo'].apply(replace_question_mark_with_na)
    # df['WhiteElo'] = df['WhiteElo'].astype('int16')
    # df['BlackElo'] = df['BlackElo'].apply(replace_question_mark_with_na)
    # df['BlackElo'] = df['BlackElo'].astype('int16')
    # df = df[df['BlackElo'] != 0]
    # df = df[df['WhiteElo'] != 0]
    # print(sorted(list(df['WhiteElo'].unique())))
    # print(sorted(list(df['BlackElo'].unique())))

    # df['Result'] = df['Result'].apply(replace_winner_by_int)
    # df['Result'] = df['Result'].astype('int16')


    # identify rows with float values in the column, by mistake
    moves_mask = df['Moves'].apply(lambda x: isinstance(x, float))
    # drop rows with float values in the column
    df = df[~moves_mask]
    
    df['Moves'] = df['Moves'].apply(clean_pgn_mainline)

    print(df.info())
    # print(sum(df['Moves'].str.len() == np.nan))
    # print(sorted(list(set(df['Moves'].str.len()))))

    print(f"Writing file {OUTPUT_CSV}")
    df.to_csv(OUTPUT_CSV)

    
if __name__ == "__main__":
    main()

