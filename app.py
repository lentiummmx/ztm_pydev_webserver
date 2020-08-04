import os
from markupsafe import escape
from flask import Flask, render_template, url_for, send_from_directory, request, redirect

from utils.utils import write_to_file, write_to_csv

app = Flask(__name__)


# with app.test_request_context():
#     app.add_url_rule('/favicon.ico',
#                      endpoint=url_for('static', filename='images/favicon.ico'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/')
def hello_world():
    return 'Hello World!!!!'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


@app.route('/<string:page_name>')
def page_name(page_name=None):
    return render_template(('index.html', page_name)[page_name != None])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    # error = None
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            write_to_file(data)
            write_to_csv(data)
            msg = 'I\'ll get in touch with you shortly'
        except Exception as err:
            msg = 'Error saving to database'
    else:
        msg = 'something goes wrong'
    return render_template('thank_you.html', message=msg)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
