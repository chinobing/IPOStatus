# -*- coding: utf-8 -*-
"""
@author: 柯西君_BingWong
#"""

from processing.datatomd import data2md
from processing.data_crawler import parse
from processing.generator import create_charts
from processing.files_extractor import copy2website,sidebar_generator


def main():

   parse(url,DIRTH_DATA,DIRTH_TERMINATION,DIRTH_MD)
   create_charts(DIRTH_DATA).render('processing/data/graph.html')
   data2md(DIRTH_DATA, DIRTH_TERMINATION, DIRTH_MD)



if __name__ == '__main__':
    DIRTH_DATA = 'processing/data/IPOstatus/data/'
    DIRTH_TERMINATION = 'processing/data/IPOstatus/termination/'
    DIRTH_MD = 'processing/data/IPOstatus/md/'
    url = "http://www.csrc.gov.cn/pub/zjhpublic/G00306202/201803/t20180324_335702.htm"

    main()

