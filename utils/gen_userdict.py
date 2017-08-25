#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2


def get_html(url):
    request = urllib2.Request(url)
    request.add_header(
        'User-Agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    )
    html = urllib2.urlopen(request)
    return html.read()


def get_soup(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    return soup


def fetch_lagou():
    words = []
    url = 'https://www.lagou.com/'
    soup = get_soup(url)
    category_list = soup.find_all('div', attrs={'class': 'menu_sub dn'})
    for category in category_list:
        dls = category.find_all('dl')
        for dl in dls:
            names = dl.dd.find_all('a')
            for name in names:
                words.append(name.text)
    return words


def fetch_zhipin():
    words = []
    url = 'http://www.zhipin.com/'
    soup = get_soup(url)
    job_menu = soup.find('div', attrs={'class': 'job-menu'})
    dls = job_menu.find_all('dl')
    for dl in dls:
        divs = dl.find_all('div', attrs={'class': 'text'})
        for div in divs:
            names = div.find_all('a')
            for name in names:
                words.append(name.text)
    return words


def fetch_stackoverflow():
    words = []
    for pageNo in range(1, 20):
        url = 'https://stackoverflow.com/tags?page=%d&tab=popular' % (pageNo)
        soup = get_soup(url)
        tags_list = soup.find('div', attrs={'id': 'tags_list'})
        trs = tags_list.table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            for td in tds:
                words.append(td.a.text)
    return words


if __name__ == '__main__':
    words = []
    words += fetch_zhipin()
    words += fetch_lagou()
    words += fetch_stackoverflow()
    word_set = set(words)
    with open('userdict.txt', 'w') as fd:
        for word in word_set:
            fd.write(word.encode('utf8'))
            fd.write(' nz')
            fd.write('\n')