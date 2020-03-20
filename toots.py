import json
import os

from flask import Flask

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

# load authors into memory
with open(os.path.join(BASE_PATH, 'data', 'authors.json'), 'r') as fp:
    authors = json.load(fp)

# load toots into memory
with open(os.path.join(BASE_PATH, 'data', 'toots.json'), 'r') as fp:
    toots = json.load(fp)


# get author object from author's id or name and if there is no data for the specified id or name, return none
def get_author(author_id=None, author_name=None):
    try:
        author = [author for author in authors if author['id'] == author_id or author['name'] == author_name][0]
        return author
    except IndexError:
        return None


# build a threaded tree structure for the toots data (recursively)
def render_child_toots(parent_toot):
    children = [toot for toot in toots if toot['parent_id'] == parent_toot['id']]
    if children:
        rendered = []
        for child in children:
            author_name = get_author(author_id=child['author_id'])['name']
            rendered.append(
                f'<li>'
                f'<span><a href="/author/{author_name}">{author_name}</a></span>'
                f"<span>:</span> <span>{child['text']}</span>"
                f"{render_child_toots(child)}"
                f'</li>'
            )
        return f"<ul>{''.join(rendered)}</ul>"
    return ''


@app.route('/')
def index():
    toots_tree = [{
        'author_name': get_author(author_id=toot['author_id'])['name'],
        'text': toot['text'],
        'id': toot['id'],
        'children': render_child_toots(toot)
    } for toot in toots if toot['parent_id'] is None]

    top_level_rendered = []
    for top_level in toots_tree:
        author_name = top_level['author_name']
        top_level_rendered.append(
            f'<li>'
            f'<span><a href="/author/{author_name}">{author_name}</a></span>'
            f"<span>:</span> <span>{top_level['text']}</span>"
            f"{top_level['children']}"
            f'</li>'
        )
    return f"<ul>{''.join(top_level_rendered)}</ul>"


def get_toot_root(toot_id):
    toot = [toot for toot in toots if toot['id'] == toot_id][0]
    if toot['parent_id'] is None:
        return {
            'author_name': get_author(author_id=toot['author_id'])['name'],
            'text': toot['text'],
            'children': render_child_toots(toot)
        }
    return get_toot_root(toot['parent_id'])


@app.route('/author/<author_name>')
def toot_threads_by_author(author_name):
    author = get_author(author_name=author_name)
    toots_tree = [{
        'author_name': get_author(author_id=toot['author_id'])['name'],
        'text': toot['text'],
        'id': toot['id'],
        'children': render_child_toots(toot),
        'parent_id': toot['parent_id'],
    } for toot in toots if toot['author_id'] == author['id']]

    toots_to_go = []

    for toot in toots_tree:
        if toot['parent_id']:
            toots_to_go.append(get_toot_root(toot['id']))
        else:
            toots_to_go.append(toot)

    top_level_rendered = []
    for top_level in toots_to_go:
        author_name = top_level['author_name']
        top_level_rendered.append(
            f'<li>'
            f'<span><a href="/author/{author_name}">{author_name}</a></span>'
            f"<span>:</span> <span>{top_level['text']}</span>"
            f"{top_level['children']}"
            f'</li>'
        )

    return f'<span>Specific Toot threads for {author_name}</span><ul>{"".join(top_level_rendered)}</ul>'
