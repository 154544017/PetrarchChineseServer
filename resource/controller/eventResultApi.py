# -*- coding: utf-8 -*-

from flask import Flask, blueprints, jsonify, request, Blueprint, g
from resource.model.analysisProjectResultModel import AnalycisEventResult
from resource.model.analysisProjectModel import AnalysisProject
from resource.model.textLibDataModel import TextLibraryData
import json

eventResultApi = Blueprint(name='event_result', import_name=__name__)


@eventResultApi.route('/<id>', methods=['GET'])
def get_event_result(id):
	try:
		table_name = 'rs_analysis_project_' + id
		AnalycisEventResult.__table__.name = table_name
		results = AnalycisEventResult.query.filter(AnalycisEventResult.text_id == id).all()
		result_data = []
		for result in results:
			result_data.append(result.as_dct())
		return jsonify(code=20000, flag=True, message="查询成功", data={"total": len(result_data), "rows": result_data})
	except Exception as e:
		print(e)
		return jsonify(code=20001, flag=False, message="查询分析结果失败")


@eventResultApi.route('/detail/<project_id>/<text_id>', methods=['GET'])
def get_event_detail(project_id, text_id):
	project = AnalysisProject.query.get(project_id)

	# 查询content
	textlib_id = project.textlibrary_id
	textlibrary_data_tablename = 'rs_textlibrary_data_%s' % textlib_id
	TextLibraryData.__table__.name = textlibrary_data_tablename
	text_data = TextLibraryData.query.get(text_id)
	text_dict = text_data.as_dict()
	paragraphs = text_data.content.decode("utf-8").split(u"\u3000")
	# remove the empty str
	paragraphs = filter(None, paragraphs)
	res = []
	for p in paragraphs:
		p = '\t' + p
		res.append(p)
	text_dict.update({"content": res})

	# 查询result
	result_tablename = 'rs_analysis_event_result_%s' % project_id
	AnalycisEventResult.__table__.name = result_tablename
	result = AnalycisEventResult.query.filter(AnalycisEventResult.text_id == text_id).all()
	result = result[0].as_dict()['event_result']
	result = json.loads(result, encoding='utf-8',strict=False)

	results = []

	for i_result in result:
		origin = i_result["origin"]
		# get Source
		source = origin[0]
		if "source" in i_result:
			source += ": " + i_result["source"]
		target = origin[1]
		if "target" in i_result:
			target += ": " + i_result["target"]
		event_code = origin[2]
		if "eventtext" in i_result:
			event_code += ": " + i_result["eventtext"]

		results.append({"source": source, "target": target, "event": event_code, "location": i_result["location"],
						"rs": "-".join(i_result["origin"])})

	return jsonify(code=20000, flag=True, message="查询成功", text=text_dict, events=results)
