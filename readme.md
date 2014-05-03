# Hacker Monthly Finder

![Hacker Monthly Finder Screen Shot](http://i.imgur.com/t4uUEWw.png)

This was a Saturday side project and the goal was to index all of the articles in the current issues of hacker monthly and make the data searchable. I wanted this because there were multiple times when I was at work and remembered some cool utility or hack I read about and couldn't find which Hacker Monthly contained the wisdom I needed.

To use this project you will need the following requirements:

* Python 2.7+ (virtual environments optional)
* Elastic search version 1.1.1 - https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.tar.gz

Follow the steps below to get your own index running:

## Step 1: Install and run elastic search

    $ wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.tar.gz
    $ tar zxvf elasticsearch-1.1.1.tar.gz
    $ cd elasticsearch-1.1.1/bin
    $ ./elasticsearch

Woah. Super easy. Elastic search is awesome.

## Step 2: Clone the repo

    $ git clone git@github.com:glenbot/hacker_monthly.git

## Step 3: Prep Data

You need to copy all of your Hacker Monthly epub files into the `data` directory of this project. You can get all of the epub files from the subscriber area of hacker monthly https://subscriber.hackermonthly.com/

    $ cd hacker_monthly
    $ cp <path_to_your_epubs>/*.epub data

This instruction may vary. The end result is that you need epub files in the `data` directory.

## Step 4: Install python requirements and index data

Make sure you have elastic search running in a terminal somewhere.

With virtual environment (recommended). This assumes you have installed virtualenv and virtualenvwrapper:

    $ git clone git@github.com:glenbot/hacker_monthly.git
    $ mkvirtualenv hm
    $ pip install -r hacker_monthly/requirements.txt
    $ cd hacker_monthly
    $ python manage.py create_index
    $ python manage.py index_data
    $ python manage.py runserver

Without virtual environment (you may need sudo):

    $ git clone git@github.com:glenbot/hacker_monthly.git
    $ pip install -r hacker_monthly/requirements.txt
    $ cd hacker_monthly
    $ python manage.py create_index
    $ python manage.py index_data
    $ python manage.py runserver

## Step 5: Find articles

Visit `http://127.0.0.1:5000` in your browser and search away.

## Reindexing data

If you add or remove hacker montly files from the `data` directory you can always run

    $ python manage.py reindex_data

## Searching VIA command line

    $ python manage.py query_index "Some search string"

## Caveats

Some of the older hacker monthly from 2010 are not parsing correctly. The TOC in the epub files don't contain the articles in the epub which makes it harder to parse. It does a decent job of it though.

## Issues

Please use the github issue tracker.

## Contributions

Pull requests always welcome :)
