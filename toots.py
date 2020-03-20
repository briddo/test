from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    # TODO: render threads!
    return render_toot(None)


@app.route('/author/<author_name>')
def toot_threads_by_author(author_name):
    # TODO: Implement me!
    return '<span>Specific Toot threads for {author_name}</span>'.format(author_name=author_name)


def render_toot(toot):
    author_name = 'Someone' # FIXME
    text = 'Not a real Toot' # FIXME

    return """
    <li>
        <span><a href="/author/{author_name}">{author_name}</a></span>
        <span>:</span>
        <span>{text}</span>
    </li>
    """.format(
        author_name=author_name,
        text=text,
    )
