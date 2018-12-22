#!-*-coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from meijuTT_m import store_links


def get_info(searchword):
    url = "https://www.meijutt.com/search/index.asp"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.102 Safari/537.36'
    }
    data = {'searchword': searchword.encode("gbk")}
    html = requests.post(url, headers=headers, data=data)
    html.encoding = "gbk"
    bs = BeautifulSoup(html.text, "html.parser").select("li a.B")
    res = []
    for rs in bs:
        meiju_url = "https://www.meijutt.com" + rs['href']
        meiju_html = requests.get(meiju_url)
        meiju_html.encoding = "gbk"
        meiju_bs = BeautifulSoup(meiju_html.text, "html.parser").select("strong.down_part_name a")
        for i in meiju_bs:
            item = {}
            item['title'] = i.text
            item['link'] = i['href']
            res.append(item)
    print("Get %d records!" % len(res))
    store_links(searchword, res)

