"""
    Apply below tranformations:
    1. calculate simple moving average of 5 days
    2. combine all stocks data into one csv file
"""

import pandas as pd
import os
import glob

src_dir = './data/raw'
file_pattern = '*.csv'
tgt_dir = './data/processed'

os.makedirs(tgt_dir,exist_ok=True)

files = glob.glob(os.path.join(src_dir,file_pattern))

df_list = [] 
for file in files:
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower().str.replace(' ','_')

    df['date'] =  pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    ## calculate 5 day simple moving average 
    df['sma_5'] = df['close'].rolling(window=5).mean()

    symbol = file.split('/')[-1].split('.')[0]
    df['symbol'] = symbol
    df_list.append(df)

combined_df = pd.concat(df_list,ignore_index=True)
output_file_name = 'processed_stocks.csv'
output_file = os.path.join(tgt_dir,output_file_name)
combined_df.to_csv(output_file,index=False)

print('transforming complete.')


    
    

    


