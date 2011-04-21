# -*- coding: utf-8 -*-
__author__ = 'sevas'

from collections import namedtuple
from datetime import datetime, date, time
try:
    import json
except ImportError:
    import simplejson as json


TaggedURL = namedtuple('TaggedURL', 'URL title tags')


def tag_URL((url, title), tags):
    return TaggedURL(URL=url, title=title, tags=tags)



def count_words(some_text):
    words = some_text.split(' ')
    return len(words)


def make_dict_keys_str(a_dict):
    items = [(str(k), v) for (k, v) in a_dict.items()]
    return dict(items)


class ArticleData(object):
    """
    A glorified dict to keep the extracted metadata and content of one article.
    Has utility methods for json (de)serialization.
    """

    def __init__(self, url, title,
                 pub_date, pub_time, fetched_datetime,
                 external_links, internal_links,
                 category, author,
                 intro, content):
        """
        Boring init func.
        """
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.pub_time = pub_time
        self.fetched_datetime = fetched_datetime

        self.external_links = external_links
        self.internal_links = internal_links

        self.category = category
        self.author = author

        self.intro = intro
        self.content = content


    def print_summary(self):
        print 'title:', self.title
        print 'url:', self.url
        print 'publication date:', self.pub_date
        print 'publication time:', self.pub_time
        print 'fetched on:', self.fetched_datetime
        print '# external links:', len(self.external_links)
        print '# internal links:', len(self.internal_links)
        print 'category:', '/'.join(self.category)
        print 'author:', self.author
        print '# words:', count_words(''.join(self.content))
        print 'intro:', self.intro


    def to_json(self):
        """
        Converts all attributes in self.__dict__ into a json string.
        Takes care of non natively serializable objects (such as datetime).
        """
        d = dict(self.__dict__)
        # datetime, date and time objects are not json-serializable

        fetched_datetime = d['fetched_datetime']
        d['fetched_datetime'] = fetched_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        pub_date, pub_time = d['pub_date'], d['pub_time']

        d['pub_date'] = pub_date.strftime('%Y-%m-%d')
        if pub_time:
            d['pub_time'] = pub_time.strftime('%H:%S')
        else:
            d['pub_time'] = None
            
        return json.dumps(d)



    @classmethod
    def from_json(kls, json_string):
        """
        Class method to rebuild an ArticleData object from a json string.
        Takes care of non natively deserializable objects (such as datetime).
        """
        d = json.loads(json_string)

        date_string = d['fetched_datetime']
        d['fetched_datetime'] = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')

        pub_date, pub_time = d['pub_date'],  d['pub_time']
        year, month, day = [int(i) for i in pub_date.split('-')]
        d['pub_date'] = date(year, month, day)

        if pub_time:
            h, m = [int(i) for i in pub_time.split(':')]
            d['pub_time'] = time(h, m)
        else:
            d['pub_time'] = None

        d = make_dict_keys_str(d)
        return kls(**d)