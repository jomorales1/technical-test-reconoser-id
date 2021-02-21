from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import time
import re

ua = UserAgent()


class BeautifulSoupComponent:
    def __init__(self, url):
        self.url = url
        self.initial_time = time.time()
        html_file = requests.get(self.url, headers={'User-Agent': ua.random}).text
        self.soup = BeautifulSoup(html_file, 'html.parser')
        self.soup.prettify()

    def get_first_level_urls(self):
        tags = self.soup.find_all('a')
        urls = set()
        for tag in tags:
            tag_url = tag['href']
            elements = tag_url.split('/')
            if self.url in tag_url and len(elements) and self.url != tag_url:
                urls.add(tag_url)
        return urls

    def __count_url_labels(self, labels, initial_time):
        counter = {}
        for label in labels:
            counter[label] = len(self.soup.find_all(name=label))
        processing_time = round(time.time() - initial_time, 2)
        counter['processing_time'] = processing_time
        return counter

    def count_labels(self, labels):
        result = {}
        urls = self.get_first_level_urls()

        result[self.url] = self.__count_url_labels(labels=labels, initial_time=self.initial_time)

        for url in urls:
            start_time = time.time()
            html_file = requests.get(url, headers={'User-Agent': ua.random}).text
            self.soup = BeautifulSoup(html_file, 'html.parser')
            result[url] = self.__count_url_labels(labels=labels, initial_time=start_time)
        return result

    def __count_url_words(self, words, initial_time):
        page = {}
        words_dict = {}
        for tag in self.soup.find_all(True):
            if tag.name and tag.name not in words_dict.keys():
                words_dict[tag.name] = 0
        for word in words:
            counter = words_dict.copy()
            tags = self.soup.find_all(text=re.compile(word))
            for tag in tags:
                text = str(tag).strip().split()
                occurrences = 0
                for w in text:
                    if w == word:
                        occurrences = occurrences + 1
                counter[tag.parent.name] = counter.get(tag.parent.name) + occurrences
            page[word] = counter
        processing_time = round(time.time() - initial_time, 2)
        page['processing_time'] = processing_time
        return page

    def count_words(self, words):
        result = {}
        urls = self.get_first_level_urls()

        result[self.url] = self.__count_url_words(words=words, initial_time=self.initial_time)

        for url in urls:
            start_time = time.time()
            try:
                html_file = requests.get(url, headers={'User-Agent': ua.random}).text
            except requests.ConnectionError as exception:
                print(exception)
                continue
            self.soup = BeautifulSoup(html_file, 'html.parser')
            result[url] = self.__count_url_words(words=words, initial_time=start_time)
        return result
