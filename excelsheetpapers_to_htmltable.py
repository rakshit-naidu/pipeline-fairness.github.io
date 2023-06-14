import pandas as pd
import argparse, os





if __name__ == "__main__":

    
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default="Pipeline Fairness Lit Review - updated_table.csv", type=str)
    args = parser.parse_args()
    file_name = args.filename

    df = pd.read_csv(file_name)

    # new_rows = updated_df[~updated_df.isin(old_df)].dropna()

    


