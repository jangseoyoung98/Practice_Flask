from flask import Flask, request, redirect
import random

app = Flask(__name__)

nextId = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'},
]

def template(contents, content = "<h2>Welcome</h2>Hello, Web"):
    return f'''<!DOCTYPE html>
    <html>
        <body>
            <h1><a href="/">WEB</h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">CREATE</a></li>
            </ul>
        </body>
    </html>
    '''

def getContents():
    liTags = " "

    for topic in topics:
        liTags += f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'

    return liTags


@app.route('/')
def index():
    return template(getContents())

@app.route('/read/<int:id>/') #id를 string으로 불러오기 때문에, int:로 형 변환 시켜줘야 함
def read(id):

    title = " "
    body = " "
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break # !!

    return template(getContents(), f"<h2>{title}</h2> <p>{body}</p>")

@app.route('/create/', methods=['POST', 'GET'])
def create():
    # method = GET이면, url을 통해 공개적으로 정보 전달 (조회) / POST이면, 은밀한 방식으로 정보 전달 (수정)
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST"> 
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method == 'POST':
        global nextId   # 전역변수를 건드리기 위해서는, 사용하기 전에 global과 함께 선언해 줘야 한다.
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body} # newTopic이라는 새 엘리먼트를 만들고
        topics.append(newTopic) # topics 리스트에 추가한다.
        url = '/read/'+str(nextId) + '/'    # nextID는 int라서, str으로 변경하기!
        nextId = nextId + 1
        return redirect(url)

app.run(port=5001, debug=True)

