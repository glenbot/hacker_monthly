#!/usr/bin/env python
import re
import os
import io
import sys
import glob
from zipfile import BadZipfile

import epub
import simplejson
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, RequestError
from bs4 import BeautifulSoup

from app import app


__all__ = [
    'parse_epub',
    'list_epub_files',
    'create_index',
    'delete_index',
    'index_data',
    'create_index',
]


def create_index(name):
    """Create an elastic search index"""
    es_client = Elasticsearch()
    schema = None

    with io.FileIO(app.config['ES_INDEX_SCHEMA'], 'r') as stream:
        schema = simplejson.loads(stream.read())

    try:
        es_client.indices.create(index=name, body=schema)
        print 'Successfully created index: {}'.format(app.config['ES_INDEX_NAME'])
    except ConnectionError ,e:
        sys.exit(e.error)
    except RequestError, e:
        sys.exit(e.error)


def delete_index(name):
    """Create an elastic search index"""
    es_client = Elasticsearch()

    try:
        es_client.indices.delete(index=name)
        print 'Successfully deleted index: {}'.format(app.config['ES_INDEX_NAME'])
    except ConnectionError ,e:
        sys.exit(e.error)
    except RequestError, e:
        sys.exit(e.error)


def index_data(index_name, epub_path):
    """Index magazine data"""
    es_client = Elasticsearch()
    files = list_epub_files(epub_path)

    for _file in files:
        data = parse_epub(_file)
        magazine_title = data['title']
        articles = data['articles']
        print 'Indexing {} articles in {}'.format(len(articles), magazine_title)

        for article in articles:
            document = {
                'name': magazine_title,
                'title': article['title'],
                'author': article['author'],
                'content': article['content']
            }

            try:
                es_client.index(index=index_name, doc_type='articles', body=document)
            except ConnectionError ,e:
                sys.exit(e.error)
            except RequestError, e:
                sys.exit(e.error)


def query_index(name, query):
    """Query index for data"""
    es_client = Elasticsearch()
    base_query = {
        "size": 20,
        "sort": ["_score"],
        "query": {
            "multi_match" : {
                "query": "", 
                "fields": [
                    "name",
                    "title",
                    "title.partial.front",
                    "title.partial.middle",
                    "author",
                    "author.partial.front",
                    "content",
                    "content.partial.front",
                    "content.partial.middle",
                    "content.partial.back"
                ] 
            }
        }
    }
    base_query['query']['multi_match']['query'] = query

    try:
        results = es_client.search(index=name, body=base_query)
        if 'hits' in results['hits']:
            if len(results['hits']['hits']) > 0:
                return results['hits']['hits']
            return []
    except ConnectionError ,e:
        sys.exit(e.error)
    except RequestError, e:
        sys.exit(e.error)


def clean_data(data):
    """Clean up unwanted markup in data"""
    data = data.strip()
    data = data.replace('\n', ' ')
    return data


def find_article_title(soup):
    """Find the title of an article using BeautifulSoup"""
    title = soup.find('h1')
    if title:
        return clean_data(title.text)
    return None


def find_article_author(soup):
    """Find the author of an article using BeautifulSoup"""
    author = soup.find_all(text=re.compile(r"By\s*.*"))
    if author:
        return clean_data(author[0].replace('By ', ''))
    return None


def find_article_content(soup):
    """Find the content of an article using BeautifulSoup"""
    content = []
    for tag in soup.find_all(['p', 'pre']):
        content.append(clean_data(tag.text))
    return ''.join(content)


def parse_epub(_file):
    """Parse the epub file and return a dictionary containing
    information about the magazine and articles"""
    data = {
        'title': '',
        'articles': []
    }
    try:
        magazine = epub.open_epub(_file)
    except BadZipfile:
        return data

    # get the title of the magazine
    data['title'] = magazine.toc.title 

    for item_id, _ in magazine.opf.spine.itemrefs:
        item = magazine.get_item(item_id)
        contents = magazine.read_item(item)
        soup = BeautifulSoup(contents)
        article = {}

        title = find_article_title(soup)
        author = find_article_author(soup)
        content = find_article_content(soup)

        if all([title, author, content]):
            article['title'] = title
            article['author'] = author
            article['content'] = content

            data['articles'].append(article)

    return data


def list_epub_files(path):
    """Get a list of epub files with absolute path"""
    files = []
    if os.path.isdir(path):
        magazines = glob.glob(os.path.join(path, '*.epub'))
        for magazine in magazines:
            _file = os.path.join(path, magazine)
            files.append(_file)
    return files


if __name__ == '__main__':
    run()
