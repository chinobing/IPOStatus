# -*- coding: utf-8 -*-
"""
@author: 柯西君_BingWong
#"""

import urllib
from bs4 import BeautifulSoup
import re
import os
import csv


#DIRTH_DATA = './data/'
#DIRTH_MD = './md/'
#    
#url = "http://www.csrc.gov.cn/pub/zjhpublic/G00306202/201803/t20180324_335702.htm"

def save_file(content, filename):
    f = open(filename, 'w',encoding="utf-8")
    f.write(content)
    f.close()
    
def parse(url,DIRTH_DATA,DIRTH_TERMINATION,DIRTH_MD):
    try:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        
        title = soup.title.string[8:]
                
        #description & statistics
        text = ""
        stat = []
        for p in soup.find_all(name='p')[-1]:
            text += str(p).replace("<span>","").replace("</span>","")
        description = (text[4:])    
        stat = re.findall('\d+', description ) # get all the stat number such as total firms, passed and failed ones
        stat = stat[3:]
        #file links
        links = ""
        for link in soup.find_all(re.compile("^a"))[:3]:
            links += "[{}]({}{})\n".format(link.string,url[:-21],link['href'][1:])
        
        #date    
        date = soup.select("#headContainer span")[2].string
        date = date.replace('年','').replace('月','').replace('日','')
        
        #generate markdown as output file
        markdown = """---\ntitle: 首次公开发行股票申请企业情况\ncomment: false\ndate: \n---\n"""
        markdown += """\n{}\n{}\n<iframe src = "graph.html" width="1200px"  height="3000px" frameborder=0 marginheight=0  marginwidth=0 scrolling="no"></iframe> \n
        """.format( description,  links)

        if not os.path.exists(DIRTH_DATA + date +".xls"): 
            #save md
            file_name = DIRTH_MD + date + '.md'
            save_file(markdown,file_name)
            save_file(markdown,'processing/data/index.md')
                
            #download xls file
            status_name = DIRTH_DATA + date + '.xls'title
            status_file = soup.find_all(re.compile("^a"))[1]
            status_file = url[:-21] + status_file['href'][1:]
            urllib.request.urlretrieve(status_file, status_name)

            termination_name = DIRTH_TERMINATION + date + '.xls'
            termination_file = soup.find_all(re.compile("^a"))[2]
            termination_file = url[:-21] + termination_file['href'][1:]
            urllib.request.urlretrieve(termination_file, termination_name)

            #apend stat to csv file
            stat.insert(0,date)
            with open('processing/data/IPOstatus/stat.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(stat) 
        
        else:
            print('数据已于'+ date +'更新，无需再次操作！')
        
    except urllib.error.URLError as e:
        print(e)

#parse(url,DIRTH_DATA,DIRTH_MD)

