#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import glob
import os
import re

def load_data(path):
    """
    Loads csv files into a panda dataframe
    Args: 
        path: path of the csv dir
    Returns:
        a panda dataframe
    """
    frame = pd.DataFrame()
    in_files = glob.glob(os.path.join(path, "*.csv"))
    pd_list = []
    for in_file in in_files:
        print(os.path.basename(in_file))
        #pd_temp = pd.read_csv(in_file, sep='\t', parse_dates=['date'], infer_datetime_format=True).assign(New=os.path.basename(in_file))
        pd_temp = pd.read_csv(in_file, sep='\t').assign(file=os.path.basename(in_file))
        pd_list.append(pd_temp)
    frame = pd.concat(pd_list, ignore_index=True)
    return frame

def regex_filter(df, pat, col="content"):
    """
    filter a dataframe by a given regex pattern on 
    'content' column (contains)
    if col is set to 'all' the pattern is searched on
    all columns, which can be looooong
    
    Args:
        df: pandas dataframe
        pat: str, the regex pattern
        col: column id, default to 'content'
    Returns:
        dataframe object
    """
    if col == "all":
        mask = df.apply(lambda x: x.str.contains(pat, regex=True)).any(axis=1)
        res = df[mask]
    else:
        res = df[df[col].str.contains(pat, regex=True, na=False)]
    return res

def date_sort(df):
    """
    sort a dataframe by 'date' and 'time' columns
    
    Args:
        df: pandas dataframe
        
    Returns:
        dataframe
    """
    res = df.iloc[pd.to_datetime((df.date+":"+df.time), format="%Y-%m-%d:%H:%M:%S").values.argsort()]
    return res

if __name__ == '__main__':
    fd = load_data('./csv')
    fd.to_pickle('pickle_pandas_fi.bz', 'bz2')
