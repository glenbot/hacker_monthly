import io
import sys
import logging

from flask.ext.script import Manager

from utils import app
from utils import create_index as _create_index
from utils import delete_index as _delete_index
from utils import index_data as _index_data
from utils import query_index as _query_index

manager = Manager(app)

logging.basicConfig(level='ERROR')


@manager.command
def create_index(name=app.config['ES_INDEX_NAME']):
    """Create an elastic search index"""
    _create_index(name)


@manager.command
def delete_index(name=app.config['ES_INDEX_NAME']):
    """Create an elastic search index"""
    _delete_index(name)


@manager.command
def index_data(name=app.config['ES_INDEX_NAME'], path=app.config['HM_EPUB_FILES']):
    """Index magazine data"""
    _index_data(name, path)


@manager.command
def reindex_data(name=app.config['ES_INDEX_NAME'], path=app.config['HM_EPUB_FILES']):
    """Query index for data"""
    _delete_index(name)
    _create_index(name)
    _index_data(name, path)


@manager.command
def query_index(query, name=app.config['ES_INDEX_NAME']):
    """Query index for data"""
    results = _query_index(name, query)
    for hit in results:
        source = hit['_source']
        print '[{}] "{}" in {} by {}'.format(
            hit['_score'],
            source['title'],
            source['name'],
            source['author']
        )

@manager.command
def runserver():
    """Runs the Flask development server i.e. app.run()"""
    from main import run
    run()


if __name__ == "__main__":
    manager.run()
