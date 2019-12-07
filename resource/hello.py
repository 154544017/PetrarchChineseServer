from flask import Blueprint, jsonify
from . import mysqldb

hellobp = Blueprint('hello', __name__, url_prefix='/hello')


@hellobp.route('/')
def hello():
	result = {'code': 200, 'message': 'hello'}
	return jsonify(result)

@hellobp.route('/test')
def test():
	mydb = mysqldb.get_db()
	cursor = mydb.cursor()
	sql = "SELECT * FROM test"
	cursor.execute(sql)
	result = cursor.fetchone()
	print(result)

	return jsonify({'code': 200, 'message': result})
