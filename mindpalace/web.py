import pathlib
from flask import Flask

app = Flask(__name__)

site_dir = pathlib.Path('')

_INDEX_HTML = '''
<html>
    <head></head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_PAGE_HTML = '''
<html>
    <head>
    <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {user_thoughts}
        </table>
    </body>
</html>
'''

_USER_THOUGHT_HTML = '''
<tr>
    <td>{thought_time}</td>
    <td>{thought}</td>
</tr>
'''


@app.route('/')
def updateIndex():
    users_html = []
    for user_dir in site_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(sorted(users_html)))
    return index_html, 200


@app.route('/users/<user_id>')
def updateUser(user_id):
    thoughts_dir = site_dir / user_id
    thought_files = [x for x in thoughts_dir.iterdir() if x.is_file()]
    user_thoughts = []
    for t in thought_files:
        timestamp = (t.stem[::-1].replace('-', ':', 2).replace('_', ' ', 1))[::-1]
        thought = t.read_text()
        user_thoughts.append(_USER_THOUGHT_HTML.format(thought_time=timestamp, thought=thought))
    user_page_html = _USER_PAGE_HTML.format(user_thoughts='\n'.join(user_thoughts), user_id=user_id)
    return user_page_html, 200


def run_webserver(address, data_dir):
    global site_dir
    ip, port = address.split(":")
    site_dir = pathlib.Path(data_dir)
    app.run(host=ip, port=int(port))
