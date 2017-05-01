from flask import Flask,render_template,request,redirect,url_for,make_response,abort
from flask.ext.script import Manager
from werkzeug.routing import BaseConverter
from os import path
from werkzeug.utils import secure_filename

class RegexConvertor(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConvertor,self).__init__(url_map)
        self.regex=items[0]

app = Flask(__name__)
app.url_map.converters['regex']=RegexConvertor
manager = Manager(app)


@app.route('/')
def hello_world():
    #return render_template('index.html',title='<h1>Hello World!-title</h1>')
    response = make_response(render_template(
        'index.html',
        title='<h1>Hello World!-title</h1>',
        body="## Header2"
    ))
    response.set_cookie('username','hahaha')
    return response

@app.route('/services')
def services():
    return 'service'

@app.route('/about')
def about():
    return 'about'

@app.route('/user/<username>')
def user(username):
    return 'Username %s' % username

@app.route('/user/<int:user_id>')
def userid(user_id):
    return  'User_id %d' % user_id

@app.route('/user/<regex("[a-z]{3}[A-Z]{3}"):user_regex>')
def userregex(user_regex):
    return 'Userregex %s' % user_regex

@app.route('/projects/')
@app.route('/our-works/')
def projects():
    return 'The project page'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username=request.form['username']
        password = request.form['password']
        print 'POST:',username, password
    else:
        username = request.args['username']
        print 'else:', username
    return render_template('login.html', method=request.method)

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path=path.join(basepath,'static\uploads')
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

@app.template_filter('md')
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)

@app.context_processor
def inject_methods():
    return dict(read_md=read_md)

def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x,y:x+y,md_file.readlines())
    return content.decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
