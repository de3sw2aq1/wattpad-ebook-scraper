#!/usr/bin/env python

import requests
import json
import dateutil.parser
import ez_epub
import sys
from genshi.input import HTML

# Setup session to not hit Android download app page
# TODO: Cookies probably aren't needed if only API requests are made
session = requests.session()
session.cookies['android-noprompt'] = '1'
session.cookies['skip-download-page'] = '1'

# Used by Android app normally
# Example parameters are what Android provides
API_STORYINFO = 'http://www.wattpad.com/api/v3/stories/' #9876543?drafts=0&include_deleted=1

# Used by website and Android app normally
API_STORYTEXT = 'http://www.wattpad.com/apiv2/storytext' # ?id=23456789
# Webpage uses a page parameter: ?id=23456789&page=1
# Android uses these parameters: ?id=23456789&increment_read_count=1&include_paragraph_id=1&output=text_zip

# Documented api
API_GETCATEGORIES = 'http://www.wattpad.com/apiv2/getcategories'

# Fixup the categories data, this could probably be cached too
categories = json.loads(session.get(API_GETCATEGORIES).content)
categories = {int(k): v for k, v in categories.iteritems()}

def download_story(story_url):
    # TODO verify input URL better
    story_id = story_url.split('/')[-1].split('-')[0]

    # TODO: probably use {'drafts': 0, 'include_deleted': 0}
    storyinfo_req = session.get(API_STORYINFO + story_id, params={'drafts': 1, 'include_deleted': 1})
    storyinfo_json = json.loads(storyinfo_req.content)

    story_title = storyinfo_json['title']
    story_description = storyinfo_json['description']
    story_createDate = dateutil.parser.parse(storyinfo_json['createDate'])
    story_modifyDate = dateutil.parser.parse(storyinfo_json['modifyDate'])
    story_author = storyinfo_json['user']['name']
    story_categories = [categories[c] for c in storyinfo_json['categories'] if c in categories] # category can be 0
    story_rating = storyinfo_json['rating'] # TODO: I think 4 is adult?

    print 'Story "{story_title}": {story_id}'.format(story_title=story_title, story_id=story_id)

    # Setup epub
    book = ez_epub.Book()
    book.title = story_title
    book.authors = [story_author]
    book.sections = []
    book.impl.description = HTML(story_description, encoding='utf-8') # TODO: not sure if this is HTML or text
    book.impl.add_meta('publisher', 'Wattpad - scraped')
    book.impl.add_meta('source', story_url)

    for part in storyinfo_json['parts']:
        chapter_title = part['title']

        if part['draft']:
            print 'Skipping "{chapter_title}": {chapter_id}, part is draft'.format(chapter_title=chapter_title, chapter_id=chapter_id)
            continue

        if 'deleted' in part and part['deleted']:
            print 'Skipping "{chapter_title}": {chapter_id}, part is deleted'.format(chapter_title=chapter_title, chapter_id=chapter_id)
            continue

        chapter_id = part['id']

        # TODO: could intelligently only redownload modified parts
        chapter_modifyDate = dateutil.parser.parse(part['modifyDate'])

        print 'Downloading "{chapter_title}": {chapter_id}'.format(chapter_title=chapter_title, chapter_id=chapter_id)

        chapter_req = session.get(API_STORYTEXT, params={'id': chapter_id})
        chapter_html = json.loads(chapter_req.content)['text']

        section = ez_epub.Section()
        section.html = HTML(chapter_html, encoding='utf-8')
        section.title = chapter_title
        book.sections.append(section)

    print 'Saving epub'
    book.make(book.title + '.epub')

# story_url = 'http://www.wattpad.com/story/9876543-example-story'

if sys.argv[1:]:
    story_urls = sys.argv[1:]
else:
    story_urls = sys.stdin

for story_url in story_urls:
    download_story(story_url)
