# -*- coding: utf-8 -*-

from flask import Flask, blueprints, jsonify, request, Blueprint, g
from resource.model.analysisProjectResultModel import AnalycisEventResult

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
