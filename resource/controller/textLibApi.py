from flask import Flask, blueprints, jsonify, request, Blueprint,g
from ..model.textLibModel import TextLibrary
from ..model.textLibDataModel import TextLibraryData
from resource import db
import datetime
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
textLib_api = Blueprint(name="textLib_api", import_name=__name__)


def create_data_table(tb_id):
    tb_name = "rs_textlibrary_data_" + str(tb_id)
    create_sql = 'CREATE TABLE IF NOT EXISTS {}(' \
                 'id int(11) not null primary key auto_increment,' \
                 'title varchar(255),' \
                 'summary text,' \
                 'keywords varchar(255),' \
                 'publish_time datetime,' \
                 'author varchar(255),' \
                 'source varchar(255),' \
                 'page varchar(20),' \
                 'content text,' \
                 'url varchar(512),' \
                 'publish_source varchar(255),' \
                 'create_time datetime,' \
                 'is_delete int(11)' \
                 ') ENGINE=InnoDB DEFAULT CHARSET=utf8;'.format(tb_name)
    db.session.execute(create_sql)


@textLib_api.route("/test")
def test():
    create_data_table(2)
    return "well done"


@textLib_api.route("/",methods=["post"])
def create_text_lib():
    params = request.json
    name = params["name"]
    desc = params["desc"]
    uid = g.uid
    text_lib = TextLibrary(textlibrary_name=name, description= desc, create_user=uid, create_time=datetime.datetime.now())
    try:
        db.session.add(text_lib)
        db.session.commit()
        db.session.flush()
        # 输出新插入数据的主键
        text_lib_id = text_lib.id
        # 创建对应的文本库数据表
        create_data_table(text_lib_id)
        return jsonify(code=20000, flag=True, message="创建文本库成功")
    except:
        return jsonify(code=20001, flag=False, message="创建文本库失败")


@textLib_api.route("/<id>",methods=["put"])
def modify_text_lib(id):
    params = request.json
    text_lib = TextLibrary.query.get(id)
    if text_lib:
        try:
            text_lib.textlibrary_name = params["name"]
            text_lib.description = params["desc"]
            db.session.commit()
            return jsonify(code=20000, flag=True, message="文本库信息修改成功")
        except:
            return jsonify(code=20002, flag=False, message="修改文本库信息失败")
    else:
        return jsonify(code=20001, flag=False, message="未找到该文本库")


@textLib_api.route("/<page>/<size>",methods=["GET"])
def get_text_libs(page=1,size=10):
    try:
        libs = TextLibrary.query.all()
        start = (int(page) - 1) * int(size)
        end = min(int(page) * int(size), len(libs))
        libs_json=[]
        for lib in libs[start:end]:
            libs_json.append(lib.as_dict())
        return jsonify(code=20000, flag=True, message="查询成功", data={"total":len(libs),"rows":libs_json})
    except Exception as e:
        print(e)
        return jsonify(code=20001, flag=False, message="未找到文本库信息")


@textLib_api.route("/<lib>/<page>/<size>")
def get_text_lib_data(lib, page, size):
    text_lib_data_table = "rs_textlibrary_data_"
    AutoBase = automap_base()
    AutoBase.prepare(db.engine, reflect=True)
    tablename1 = text_lib_data_table+"1"
    TextLibDataModel = getattr(AutoBase.classes, tablename1)
    db.session = Session(db.engine)
    rs1 = db.session.query(TextLibDataModel).all()
    AutoBase.prepare(db.engine, reflect=True)
    tablename2 = text_lib_data_table + "2"
    TextLibDataModel2 = getattr(AutoBase.classes, tablename2)
    db.session = Session(db.engine)
    rs2 = db.session.query(TextLibDataModel2).all()
    return "well"
