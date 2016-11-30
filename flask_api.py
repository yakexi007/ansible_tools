#!/usr/bin/env  python
#coding:utf-8

from flask import Flask,request,jsonify,make_response,g,url_for
from flask_restful import abort
from flask_httpauth import HTTPBasicAuth
from flask_exe_mysql import db, app, User
import ansible.runner

auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/users/', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 204, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/user/<id>')
def get_user(id):
    return '<h1>Hello,%s</h1>' % user.name

@app.route('/api/token/')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/api/tasks/', methods=['POST','GET'])
@auth.login_required
def task():
    data = request.json
    result = ansible.runner.Runner(
          remote_user = data['username'],
          remote_pass = data['password'],
          module_name = data['moudle'],
	  module_args = data['args'],
          pattern = data['host']
	  #environment = {'LANG':'zh_CN.UTF-6','LC_CTYPE':'zh_CN.UTF-8'}
          ).run()
    return jsonify(result['contacted'])

@app.route('/api/data/')
@auth.login_required
def demo():
    return jsonify({'data':'ok'})


if __name__ == '__main__':
    app.run(debug=True)
