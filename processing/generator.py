# -*- coding: utf-8 -*-
"""
@author: 柯西君_BingWong
#"""
from pyecharts import Style,Map
from pyecharts import  Line, Scatter, EffectScatter, Pie, Gauge, Bar,WordCloud
from pyecharts import Grid, Page
import pandas as pd
from cpca import *
import numpy as np
import glob
import os
import re


#path = 'data/'

WIDTH = 1100
def geo_formatter(params):
    return params.name + ' : ' + params.value + ' 家'

def create_charts(path):
    #read the latest file
    latest_file = sorted(glob.iglob(path + '/*'), key=os.path.getmtime)[-1]

    df_data = pd.DataFrame()
    #get date based on file name
    date = latest_file[len(path):-4]
    status_file = pd.ExcelFile(latest_file, sort = True)
    stat_file = pd.read_csv('processing/data/IPOstatus/stat.csv')
    
    #status data
    for sheet in status_file.sheet_names[1:]:
        data = status_file.parse(sheet,header=[2],index_col=0,skipfooter=1)
        new_columns = [data.columns[i-1] + "二" if data.columns[i].find("Unnamed") >= 0 else data.columns[i] for i in range(len(data.columns))]
        data.columns = new_columns
        data['date'] = date
        data['板块'] = sheet
        df_data = df_data.append(data, ignore_index=True)
    province = transform(df_data['注册地'].tolist())['省']
    df_data['省'] = [x[:-1]  if len(x)==3 else x for x in province.values]
    df_data.replace('', np.nan, inplace=True)
    df_data['省'].fillna(df_data['注册地'], inplace=True)
    # print(df_data['省'].value_counts().tolist())
    # print(df_data['省'].value_counts().index.tolist())
    
    #stat data
    #stat_file.drop(columns='waiting',inplace=True)
    #stat_file.rename(columns={"date": "日期", "total": "受理企业总数","passed":"已过会","queue":"待审企业","failed":"中止审查企业"},inplace = True)
    latest_stat = stat_file.iloc[-1]
    date_stat = stat_file['date']
    total_stat = stat_file['total']
    diff_stat = stat_file['total'] - stat_file['total'].shift(1)
    passed_stat = list(stat_file['passed'])
    queue_stat = list(stat_file['queue'])
    failed_stat = list(stat_file['failed'])

##################################################################################
    page = Page()

    style = Style(
        width=1100, height=600
    )
    value = df_data['省'].value_counts().tolist()
    attr = df_data['省'].value_counts().index.tolist()
    data = [(name,val) for (name,val) in zip(attr,value)]
    chart = Map("IPO申报企业分布图","cnVaR.cn",title_pos='center', **style.init_style)
    chart.add("", attr, value, maptype='china',
              is_visualmap=True,
              is_label_show=True,
              visual_text_color='#000',
              tooltip_formatter=geo_formatter,  # 重点在这里，将函数直接传递为参数。
              label_emphasis_textsize=15,
              label_emphasis_pos='right',
              )
    page.add(chart)

    #
    bar_diff = Bar("")
    bar_diff.add("受理企业总数", date_stat, total_stat)
    bar_diff.add("增长(减少)企业数", date_stat, diff_stat, legend_pos="15%")

    bar_stat = Bar("申报企业情况")
    bar_stat.add("已过会", date_stat, passed_stat, is_stack=True)
    bar_stat.add("待审企业", date_stat, queue_stat, is_stack=True)
    bar_stat.add("中止审查企业", date_stat, failed_stat, is_stack=True,legend_pos="60%")
    
    chart = Grid(width=WIDTH)
    chart.add(bar_stat, grid_left="60%")
    chart.add(bar_diff, grid_right="60%")
    page.add(chart)


    #
    v1 = df_data['所属行业'].value_counts().tolist()
    attr = df_data['所属行业'].value_counts().index.tolist()
    pie = Pie("所属行业分布","cnVaR.cn", title_pos="center", **style.init_style)
    pie.add("", attr, v1, radius=[45, 55], center=[50, 50],
            legend_pos="85%", legend_orient='vertical')
    page.add(pie)

    #
    chart = Pie('申报企业所占板块的比例', "数据来自中国证券监督管理委员会 ",
                title_pos='center', **style.init_style)
    total_counts = df_data['板块'].count()
    for exchange,counts,position in zip(df_data['板块'].unique(),df_data['板块'].value_counts(),range(1,4)):
        chart.add("", [exchange, "总数"], [counts, total_counts], center=[25*position, 30], radius=[28, 34],
                  label_pos='center', is_label_show=True, label_text_color=None, legend_top="center" )
    page.add(chart)
    
    #
    attr1 = [attr.replace("（特殊普通合伙）","").replace('(特殊普通合伙)','').replace('（特殊普通合伙)','')for attr in df_data['会计师事务所'].unique().tolist()]
    attr2 = df_data['保荐机构'].unique().tolist()
    v1 = df_data['会计师事务所'].value_counts().tolist()
    v2 = df_data['保荐机构'].value_counts().tolist()
    #chart_accountants
    chart_accountants = Bar("会计师事务所 - 统计图","cnVaR.cn",title_pos="center", **style.init_style)
    chart_accountants.add("会计师事务所", attr1, v1,legend_pos="75%",
              mark_point=["max", "min"], is_datazoom_show=True, datazoom_range=[0, 40], datazoom_type='both',
              xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30)
    chart = Grid(width=WIDTH)
    chart.add(chart_accountants, grid_bottom="30%")
    page.add(chart)
    #chart_sponsor
    chart_sponsor = Bar("保荐机构 - 统计图","cnVaR.cn",title_pos="center", **style.init_style)
    chart_sponsor.add("保荐机构", attr2, v2,legend_pos="75%",
              mark_point=["max", "min"], is_datazoom_show=True, datazoom_range=[0, 40], datazoom_type='both',
              xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30,yaxis_margin=50)
    chart = Grid(width=WIDTH)
    chart.add(chart_sponsor, grid_bottom="30%")
    page.add(chart)

    return page

#create_charts().render('./graph.html')

