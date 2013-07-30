import json
import logging
import re
import unidecode

import requests
from pelican import signals


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
GIST_API_ENDPOINT = 'https://api.github.com/gists'

def _slugify(title):
    """Turns the specified title into a format compatible with Gist's file fields."""
    title = unidecode.unidecode(title).lower()
    title = re.sub(r'\W+', '-', title)
    return title


def _load_gist_ids(filename='gist_comment_ids.json'):
    """
    Load Gist ID information stored in the specified filename into a
    dictionary and return it.
    """
    try:
        f = open(filename, 'r')
        content = f.read()
        f.close()
        if content:
            return json.loads(content)
    except IOError:
        pass
    return {}


def _save_gist_ids(gist_dict, filename='gist_comment_ids.json'):
    """
    Save the dictionary specified in gist_dict to the specified filename.
    """
    f = open(filename, 'w+')
    f.write(json.dumps(gist_dict))
    f.close()


def _create_gist(title, page_url, auth_token):
    """Create a Gist using GitHub's API and return the Gist's ID."""
    logger.info('Creating a Gist for "%s"' % title)
    headers = {
        'Authorization': 'token %s' % auth_token,
        'content-type': 'application/json'
    }
    payload = {
        "description": "Comments for %s" % title,
        "public": True,
        "files": {
            "comments-for-%s.md" % _slugify(title): {
                "content": "Please use this page to discuss [%s](%s)." % (title, page_url)
            }
        }
    }

    r = requests.post(GIST_API_ENDPOINT, data=json.dumps(payload), headers=headers)
    if r.status_code != 201:
        logger.error('gist_comments:  An error occurred during Gist creation. The response from the API follows.')
        logger.error(r.content)
        exit(-1)
    return r.json()['id']


def gist_comments(generator, metadata):
    if not 'GITHUB_USERNAME' in generator.settings.keys():
        logger.error('gist_comments: Please add GITHUB_USERNAME to your settings file.')
        exit(-1)

    if not 'GITHUB_AUTH_TOKEN' in generator.settings.keys():
        logger.error('gist_comments: Please add GITHUB_AUTH_TOKEN to your settings file.')
        logger.error('See README.md for instructions on creating a GitHub auth token.')
        exit(-1)

    slug = metadata['slug']
    page_url = '%s/%s' % (generator.settings['SITEURL'], slug)
    gist_ids = _load_gist_ids()

    if not slug in gist_ids:
        gist_ids[slug] = _create_gist(metadata['title'], page_url, generator.settings['GITHUB_AUTH_TOKEN'])

    metadata['gist_id'] = gist_ids[slug]
    _save_gist_ids(gist_ids)


def register():
    signals.article_generate_context.connect(gist_comments)
