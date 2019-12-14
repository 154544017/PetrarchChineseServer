# -*- coding: utf-8 -*-

from flask import request, Blueprint,jsonify,current_app,g
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


@dictionary_api.route('/add_dic', methods=['POST'])
def add_dic():
    upload_file = request.files['dic']
    name = request.form.get('name')
    file_name = secure_filename(upload_file.filename)
    print(file_name)
    if upload_file is None:
        return jsonify(code=20001, flag=False, message="dic_file is null")
    upload_path = os.path.join(os.path.abspath('..'), 'PetrarchChineseServer','dictionary',file_name)
    print(upload_path)
    upload_file.save(upload_path)
    dictionary=dicModel.Dictionary(id=1,name=name,file_name=file_name,create_user=2,create_time=datetime.datetime.now())
    db.session.add(dictionary)
    db.session.commit()
    return jsonify(code=20000, flag=True, message="成功添加词典")


@dictionary_api.route('/del_dic', methods=['DELETE'])
def del_dic():
    params = request.json
    id = params["id"]
    dictionary=dicModel.Dictionary.query.get(id)
    if dictionary is None:
        return jsonify(code=20001, flag=False, message="要删除的词典不存在")
    db.session.delete(dictionary)
    db.session.commit()
    return jsonify(code=20000, flag=True, message="删除成功")

@dictionary_api.route('/get_dic', methods=['GET'])
def get_dic():
    print("ssssss")
    params = request.json
    id = params["id"]
    dictionary = dicModel.Dictionary.query.filter_by(id=id).first()
    print(dictionary)
    #dictionary=dicModel.Dictionary.query.get(id)
    if dictionary is None:
        return jsonify(code=20001, flag=False, message="要查找的词典不存在")
    name=dictionary.name
    file_name=dictionary.file_name
    maker=dictionary.create_user
    time=dictionary.create_time
    return jsonify({'code': 20000,'flag':True, 'message':"get_dictionary sucessful",'data':{'name':name,'file_name':file_name,'author':maker,'create_time':time}})

