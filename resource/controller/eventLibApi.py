# -*- coding: utf-8 -*-

from resource import db
import datetime
from flask import Flask, blueprints, jsonify, request, Blueprint, g
from resource.model.analysisProjectModel import AnalysisProject
from resource.model.analysisProjectResultModel import AnalycisEventResult
from petrarch_chinese.main import petrarch_chinese_main
import thread, time
import json

eventLibApi = Blueprint(name='event_lib', import_name=__name__)


def create_analysis_result_table(project_id):
	table_name = 'rs_analysis_event_result_%s' % project_id
	drop_sql = 'DROP TABLE IF EXISTS {}'.format(table_name)
	create_sql = 'create table IF NOT EXISTS {}(' \
				 'id int(20) not null primary key auto_increment,' \
				 'text_id varchar(255) not null,' \
				 'recall_rate decimal(10,2),' \
				 'accuracy_rate decimal(10,2),' \
				 'event_num int(11) not null,' \
				 'event_result text not null' \
				 ')'.format(table_name)
	db.session.execute(drop_sql)
	db.session.execute(create_sql)


@eventLibApi.route('/test')
def test():
	analysis_event("1")
	return 'well done'

# 在子线程中分析文本库的文本，并把提取到的事件载入分析结果库里
def analysis_event(project_id):
	# 创建对应的文本库数据表
	create_analysis_result_table(project_id)

	# TODO 调整petrarch参数
	art_events = petrarch_chinese_main()

	# 打开对应的结果库
	table_name = 'rs_analysis_event_result_%s' % project_id
	AnalycisEventResult.__table__.name = table_name

	# 保存事件
	try:
		for art in art_events:
			events = art_events[art]
			result = []
			event_num = 0
			for event in events:
				result = result + event
				event_num = event_num + len(event)
			text_id = art
			event_result = json.dumps(result)
			new_result = AnalycisEventResult(text_id=text_id, event_num=event_num, event_result=event_result)
			db.session.add(new_result)
			db.session.commit()

		# 修改分析状态
		project = AnalysisProject.query.get(project_id)
		project.status = 1
		db.session.commit()
		print("ok")
	except Exception as e:
		print ('error')
		print (e)


def test_thread():
	time.sleep(5)
	print("haha")


# 开始一个文本库事件提取
@eventLibApi.route('/', methods=['POST'])
def create_analysis_event():
	paras = request.json
	lib_id = paras['lib_id']  # 文本库id
	algorithm = paras['algorithm']  # 分析算法
	type = paras['type']  # 提取分析类型
	name = paras['name']  # 事件提取名称
	dict_id = paras['dic_id']  # 词典id
	uid = g.uid  # 用户id

	analysis_project = AnalysisProject(name=name, textlibrary_id=lib_id, analysis_alorithm=algorithm,
									   analysis_type=type, dictionary_id=dict_id, create_user=uid,
									   create_time=datetime.datetime.now())
	try:
		db.session.add(analysis_project)
		db.session.commit()
		db.session.flush()
		# 输出新插入数据的主键
		id = analysis_project.id

		# 子线程调用petrarch
		thread.start_new_thread(analysis_event, (id,))
		return jsonify(code=20000, flag=False, message="创建事件分析结果成功")
	except:
		return jsonify(code=20001, flag=False, message="创建事件分析结果失败")

# 得到指定位置的分析结果
@eventLibApi.route('/<page>/<size>', methods=['POST'])
def get_analysis_project(page, size):
	try:
		projects = AnalysisProject.query.filter(AnalysisProject.is_delete == 1).all()
		start = (int(page) - 1) * int(size)
		end = min(int(page) * int(size), len(projects))
		result_project = []
		for project in projects[start:end]:
			result_project.append(project.as_dict())
		return jsonify(code=20000, flag=True, message="查询成功", data={"total": len(projects), "rows": result_project})

	except Exception as e:
		print(e)
		return jsonify(code=20001, flag=False, message="查询事件分析结果失败")


# 删除特定的分析工程
@eventLibApi.route('/<id>', methods=['DELETE'])
def delete_analysis_project(id):
	project = AnalysisProject.query.get(id)
	if project is None:
		return jsonify(code=20001, flag=False, message="不存在指定的文本库分析信息")
	db.session.delete(project)
	db.session.commit()
	return jsonify(code=20000, flag=True, message="删除成功")

# 获得分析状态
@eventLibApi.route('/<id>', methods=['GET'])
def get_analysis_status(id):
	project = AnalysisProject.query.get(id)
	if project is None:
		return jsonify(code=20001, flag=False, message="不存在指定的文本库分析信息")
	status = project.status
	if status == 0:
		return jsonify(code=20000, flag=True, message="未完成")
	else:
		return jsonify(code=20000, flag=True, message="完成")
