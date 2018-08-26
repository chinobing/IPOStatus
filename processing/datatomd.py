# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 00:07:51 2018

@author: 柯西君_BingWong
#"""
import pandas as pd
from tabulate import tabulate
import glob
import os

def df_to_markdown(df, y_index=False):
    blob = tabulate(df, headers='keys', tablefmt='pipe')
    if not y_index:
        # Remove the index with some creative splicing and iteration
        return '\n'.join(['| {}'.format(row.split('|', 2)[-1]) for row in blob.split('\n')])
    return blob

def save_file(content, filename):
    f = open(filename, 'w',encoding="utf-8")
    f.write(content)
    f.close()

def data2md(data_path,termination_path,md_path):
    data_file = sorted(glob.iglob(data_path + '/*'), key=os.path.getmtime)[-1]
    termination_file = sorted(glob.iglob(termination_path + '/*'), key=os.path.getmtime)[-1]
    md_file = sorted(glob.iglob(md_path + '/*'), key=os.path.getmtime)[-1]
    #status data

    f = open(md_file, 'r',encoding='utf8')
    markdown = f.read()


    markdown += '\n# 正常审核状态申请企业情况 \n\n'
    status_file = pd.ExcelFile(data_file, sort = True)
    for sheet in status_file.sheet_names[1:4]:
        markdown += '\n\n## ' + sheet + '\n\n'
        data = status_file.parse(sheet,header=[2],index_col=0,skipfooter=1)
        new_columns = [data.columns[i-1] + "二" if data.columns[i].find("Unnamed") >= 0 else data.columns[i] for i in range(len(data.columns))]
        data.columns = new_columns

        table = df_to_markdown(data)
        markdown += table

    #terminated data
    markdown += '\n\n# 中止审查和终止审查企业情况 \n\n'
    terminated_file = pd.ExcelFile(termination_file, sort = True)
    for sheet in terminated_file.sheet_names[1:4]:
        markdown += '\n\n## ' + sheet + '\n\n'
        data = terminated_file.parse(sheet,header=[2],index_col=0)
        new_columns = [data.columns[i-1] + "二" if data.columns[i].find("Unnamed") >= 0 else data.columns[i] for i in range(len(data.columns))]
        data.columns = new_columns

        table = df_to_markdown(data)
        markdown += table
    #获取5th table，因为格式不一样，所以要分开获取
    sheet = terminated_file.sheet_names[4]
    data = terminated_file.parse(sheet, header=[2], index_col=0)
    table = df_to_markdown(data)
    markdown += '\n\n## ' + sheet + '\n\n'
    markdown += table

    save_file(markdown,'processing/data/index.md')

# data_path = 'data/IPOstatus/data/'
# termination_path = 'data/IPOstatus/termination/'
# md_path = 'data/IPOstatus/md/'
# data2md(data_path,termination_path,md_path)