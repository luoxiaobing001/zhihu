__author__="luoxiaobing"

import requests
import re
import json
import collections
from multiprocessing import Pool
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<li>.*?pic">.*?class.*?>(\d+)</em>.*?src="(.*?)".*?hd">.*?href="(.*?)".*?title">'
                             +'(.*?)</span>.*?quote">.*?inq">(.*?)</span>.*?</li>',re.S)

    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'player':item[2],
            'title':item[3],
            'mark':item[4],
        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
def main(offset):
    url='https://movie.douban.com/top250?start=' + str(offset)
    html = get_one_page(url)
    # print(parse_one_page(html))
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])