# -*- coding: utf-8 -*-

from flask import request, Blueprint, jsonify, current_app, make_response, send_file
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
import hashlib
from ..model import userModel,dicModel
from resource import app
from resource import db
from werkzeug.utils import secure_filename
import datetime
import os

dictionary_api = Blueprint(name="dictionary_api", import_name=__name__)


@dictionary_api.route('/test', methods=['POST'])
def test():
    return "sssss"


@dictionary_api.route('', methods=['POST'])
def add_dic():
    try:
        upload_file = request.files['dic']
        name = request.form.get('name')
        file_name = secure_filename(upload_file.filename)
        print(file_name)
        if upload_file is None:
            return jsonify(code=20001, flag=False, message="dic_file is null")
        upload_path = os.path.join(os.path.abspath('..'), 'PetrarchChineseServer','dictionary',file_name)
        print(upload_path)
        upload_file.save(upload_path)
        dictionary=dicModel.Dictionary(name=name,file_name=file_name,create_user=2,create_time=datetime.datetime.now())
        db.session.add(dictionary)
        db.session.commit()
        return jsonify(code=20000, flag=True, message="成功添加词典")
    except Exception as e:
        return jsonify(code=20001, flag=False, message="添加词典失败")


@dictionary_api.route('/<id>', methods=['DELETE'])
def del_dic(id):
    dictionary=dicModel.Dictionary.query.get(id)
    if dictionary is None:
        return jsonify(code=20001, flag=False, message="要删除的词典不存在")
    db.session.delete(dictionary)
    db.session.commit()
    return jsonify(code=20000, flag=True, message="删除成功")


@dictionary_api.route('/data/<id>', methods=['GET'])
def get_dic(id):
    dictionary = dicModel.Dictionary.query.filter_by(id=id).first()
    print(dictionary)
    #dictionary=dicModel.Dictionary.query.get(id)
    if dictionary is None:
        return jsonify(code=20001, flag=False, message="要查找的词典不存在")
    file_name=dictionary.file_name
    file_path = os.path.join(os.path.abspath('..'), 'PetrarchChineseServer','dictionary',file_name)
    print file_path
    with open(file_path,'r') as f:
        content = f.readlines()
    content_str = ""
    for line in content:
        content_str+=line
    return jsonify({'code': 20000,'flag':True, 'message':"get_dictionary sucessful",'data':{"content":content_str}})


@dictionary_api.route("<page>/<size>", methods=["get"])
def get__all_dict(page, size):
    try:
        res = dicModel.Dictionary.query.all()
        start = (int(page) - 1) * int(size)
        end = min(int(page) * int(size), len(res))
        data_json = []
        for data in res[start:end]:
            data_json.append(data.as_dict())
        return jsonify(code=20000, flag=True, message="查询成功", data={"total": len(res), "rows": data_json})
    except Exception as e:
        return jsonify(code=20001, flag=False, message="查询失败")

@dictionary_api.route("/download/<id>",methods=["get"])
def download(id):
    dictionary = dicModel.Dictionary.query.filter_by(id=id).first()
    if dictionary is None:
        return jsonify(code=20001, flag=False, message="要下载的词典不存在")
    file_name = dictionary.file_name
    file_path = os.path.join(os.path.abspath('..'), 'PetrarchChineseServer', 'dictionary', file_name)
    # 首先定义一个生成器，每次读取512个字节


    return send_file(file_path)