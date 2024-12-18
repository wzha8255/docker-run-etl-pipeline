import yfinance as yf
import os
import pandas as pd

## load in reference data to get selected tickers
## read in reference table to get selected symbols to fetch
src_dir = './data'
ref_file_name = 'top_50_symbols.csv'
ref_file = os.path.join(src_dir,ref_file_name)
symbols_df = pd.read_csv(ref_file)

## light transformation
symbols_df.columns = symbols_df.columns.str.lower().str.replace(' ','_').str.replace('(','').str.replace(')','')

symbols = symbols_df['stock_symbol'].tolist()

## write to raw folder 
tgt_dir = './data/raw'

for symbol in symbols:
    data = yf.Ticker(symbol)
    df = pd.DataFrame(data.history(period="1mo"))
    df = df.reset_index()

    output_file_name = f'{symbol}.csv'
    output_file = os.path.join(tgt_dir,output_file_name)
    df.to_csv(output_file,index=False)

print('data extract complete.')