# pip install flask
# pip install pandas
# pip install excel2json-3
# pip install openpyxl

from crypt import methods
import json
import pandas as pd
from flask import Flask,jsonify,request
import openpyxl

app = Flask(__name__)

# df = pd.read_excel('/home/omar/Desktop/novels_api/novels.xlsx')

page_url = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"
# file_excel = '/home/omar/Desktop/novels_api/novels.xlsx'

def get_data():
    excel_file = 'novels.xlsx'
    df = pd.read_excel(excel_file, sheet_name='novels', engine='openpyxl')
    data_list = df.values.tolist()
    data_dicts = []
    for item in data_list:
        item_dict = {}
        item_dict["order"] = item[0]
        item_dict["novel"] = item[1]
        item_dict["writer"] = item[2]
        item_dict["country"] = item[3]
        data_dicts.append(item_dict)
    return data_dicts

@app.route('/novels/', methods=['GET'])
def get_novels():
    if request.method == "GET":
        data_dicts = get_data()
        data_json = json.dumps(data_dicts, ensure_ascii = False)
    return data_json

@app.route("/novels/<id>", methods=["GET"])
def read_novel(id):
    if request.method == "GET":
        data_dicts = get_data()
        returned_item = {}
        print(id)
        for item in data_dicts:
            if item["order"] == int(id):
                returned_item = item
                returned_item =json.dumps(returned_item, ensure_ascii = False)
        print(returned_item)
        if returned_item:
            return returned_item
        else:
            return "Not Found Please Enter Valid Number"

@app.route("/novels/", methods=["POST"])
def add_novel():
    if request.method == "POST":
        print('#################')
        novel = request.get_json().get("novel")
        writer = request.get_json().get("writer")
        country = request.get_json().get("country")
        print('ddd', novel)
        if novel and writer and country:
            print(request.get_json())
            print('@@@@@@@@@@@@@@@@')
            data_dicts = get_data()
            last_order = data_dicts[-1]["order"]
            data_dicts.append(request.get_json())
            added_novel_order = last_order + 1
            new_data = {"order":added_novel_order}
            new_data.update(data_dicts[-1])
            request_line = {"order":added_novel_order,"novel":novel,"writer":writer,"country":country}
            added_line = new_data.update()
            print('EEEEEE',added_line,type(added_line))
            data_dicts[-1] = new_data
            return '', 204
        return '', 400


app.run()