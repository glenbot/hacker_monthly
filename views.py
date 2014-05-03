from flask import render_template, jsonify, request

from utils import app, query_index


@app.context_processor
def context():
    return {
        'APP_NAME': app.config['APP_NAME'],
        'APP_TAGLINE': app.config['APP_TAGLINE']
    }


@app.route('/')
def index():
    ctx = {}
    return render_template('index.html', **ctx)


@app.route('/query')
def query():
    _query = request.args.get('query')
    results = query_index(app.config['ES_INDEX_NAME'], _query)
    return jsonify(**{'results': results})
