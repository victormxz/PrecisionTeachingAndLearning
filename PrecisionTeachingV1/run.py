#coding=utf-8
import json
import requests
from flask import Flask,request, render_template,g
import sqlite3
import datetime
import get_submit_time

app = Flask(__name__)

USERNAME = 'leiyunhe'
PASSWORD = 'he18801730209'
CREATOR = 'leiyunhe'
TIME = '2017-01-01T00:00:00Z'
REPO_OWNER = 'AIMinder'
REPO_NAME = 'Py103'
payload = {
			'since':TIME} # 每个函数传递的payload不同，因此需要修改，重新写成几个不同的payload,存在字典中，以备调用。
DATABASE = './databasetest.db'
PAGE = 'test.html'

AREA = {'长三角大区','珠三角大区','北京大区','其他地区'}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def query_from_db(name):
	'''通过用户github名称，从数据库查询用户每个单元作业的提交时间'''
	r = query_db('select * from submit_issue where github_user_name = ?',
	                [name], one=True)
	if r is None:
	    print('No such user')
	else:
	    print(r)
	return r

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def fetch_db():
	
	for row in get_db().execute('SELECT * FROM submit_issue ORDER by github_user_name'):
		print(row)


@app.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == 'POST':
		r = request.form['UserName']

		if r and request.form['query'] == '查询':
			s = query_from_db(r)
			# print(s,type(s))
			List_history.append(s)		
			return render_template(PAGE, result = s)
		else:
			s = ['请AIMinder Py103学员输入GitHub用户名，进行查询']
			return render_template(PAGE, result = s)		

	else:
		if request.args.get('button') == 'help':
			s = ['AIMinder Py103学员输入GitHub用户名，查询个人提交作业的情况']
			return render_template(PAGE, help = s)
		elif request.args.get('button') == 'history':
			s = List_history
			return render_template(PAGE, history = s)
		elif request.args.get('button') == 'Py103':
			# s = []
			# for item in fetch_db():
			# 	s.append(item)
			# s[0] = fetch_db()
			# # s = fetch_db()
			s = ['alldata']
			return render_template(PAGE, py103 = s)
		else:
			return render_template(PAGE)

if __name__ == '__main__':
	List_history = []
	
	with app.app_context():
		# insert_into_db()
		app.run(debug=True)