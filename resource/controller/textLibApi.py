from flask import Flask, blueprints, jsonify, request, Blueprint

textLib_api = Blueprint(name="textLib_api", import_name=__name__)


@textLib_api.route("/",methods=["post"])
def create_text_lib():
    return