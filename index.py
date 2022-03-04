from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return '''
    <a href="/home">Home</a>
    '''


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/rss')
def contact():
    return 'RSS Page Route'


@app.route('/api')
def api():
    with open('data.json', mode='r') as my_file:
        text = my_file.read()
        return text
