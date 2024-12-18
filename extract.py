import requests
import os
import json
import pandas as pd




## read in reference table to get selected symbols to fetch
raw_data_dir = './data/raw'
os.makedirs(raw_data_dir,exist_ok=True)

src_dir = './data'
ref_file_name = 'top_50_symbols.csv'
ref_file = os.path.join(src_dir,ref_file_name)
symbols_df = pd.read_csv(ref_file)

## light transformation
symbols_df.columns = symbols_df.columns.str.lower().str.replace(' ','_').str.replace('(','').str.replace(')','')

print(symbols_df)

symbols = symbols_df['stock_symbol'].tolist()

tgt_dir = './data/raw'

i = 0
for symbol in symbols: 
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=MLPZXNUP09LXFSRF'
    r = requests.get(url)
    data = r.json()

    output_file_name = f'{symbol}.json'
    output_file = os.path.join(tgt_dir,output_file_name)

    with open(output_file,'w') as f:
        json.dump(data,f)
    
    i += 1
    if i >= 10:
        break

print('json data write complete.')