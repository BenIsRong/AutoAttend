import os
import json
import glob
import time
import flask
import pymongo
import hashlib
import requests
import subprocess

from datetime import datetime
from bson.objectid import ObjectId

app = flask.Flask(__name__)
app.secret_key = "secret_key"
mongodb = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

db = mongodb["AutoAttendDB"]
admin = db["admin"]
record = db["records"]
student = db["students"]
person_group_id = "autoattend"
key = "32cd204c1b7f4bbe98a67cd7dae08cc7"
endpoint = "https://autoattend.cognitiveservices.azure.com/"

@app.route('/', methods=["GET", "POST"])
def home():
    message = ""
    if flask.request.method == "POST":
        res = admin.find_one({"adminNum": flask.request.form["adminNum"]})
        if res:
            if hashlib.sha256(str(flask.request.form["password"]).encode()).hexdigest() == res["password"]:
                flask.session["adminNum"] = flask.request.form["adminNum"]
                return flask.redirect(flask.url_for("dashboard"))
            else:
                message = "wrong password"
        else:
            message = "admin not found"
    return flask.render_template("index.html", message=message)

@app.route('/api/v1/students', methods=["GET", "DELETE"])
def students():
    if not "adminNum" in flask.session:
        return json.dumps({"students": []})
    else:
        if flask.request.method == "GET":
            return json.dumps({"students": sorted([{"id": str(std["_id"]), "reg": std["reg"], "name": std["name"], "class": std["class"], "personId": std["personId"]} for std in student.find({}, {"_id": 1, "reg": 1, "name": 1, "class": 1, "personId": 1})], key=lambda x:x["reg"])})
        else:
            args = [args.split("=")[-1] for args in flask.request.get_data().decode().split("&")]
            # student.find_one_and_delete({"_id": ObjectId(args[0])})
            # response = requests.delete(f"{endpoint}face/v1.0/persongroups/{person_group_id}/persons/{args[1]}", headers={"Ocp-Apim-Subscription-Key": key})
            return json.dumps({"students": []})

@app.route('/api/v1/records', methods=["GET", "DELETE"])
def records():
    if not "adminNum" in flask.session:
        return json.dumps({"records": []})
    else:
        if flask.request.method == "GET":
            recs = [{"id": str(rec["_id"]), "reg": rec["reg"], "date": rec["date"], "time": rec["time"]} for rec in record.find({}, {"_id": 1, "reg": 1, "date": 1, "time": 1})]
            res_records = []

            for rec in recs:
                rec["name"] = student.find_one({"reg": int(rec["reg"])})["name"]
                res_records.append(rec)

            return json.dumps({"records": res_records})
        else:
            record.find_one_and_delete({"_id": ObjectId(flask.request.get_data().decode().split('=')[-1])})
            return json.dumps({"students": []})

@app.route('/dashboard', methods=["GET"])
def dashboard():
    if not "adminNum" in flask.session:
        return flask.redirect(flask.url_for("home"))
    else:
        return flask.render_template("dashboard.html")

@app.route('/api/v1/mark', methods=["POST"])
def mark():
    if not "adminNum" in flask.session:
        return flask.redirect(flask.url_for("home"))
    else:
        try:
            now = datetime.now()
            date = now.strftime("%d/%m/%y")
            time = now.strftime("%H:%M")
            res_path = os.path.join("\\".join(os.path.realpath(__file__).split('\\')[:-3]), "temp", "result")
            images_path = os.path.join("\\".join(os.path.realpath(__file__).split('\\')[:-3]), "temp", "images")
            flask.request.files["attendance"].save(images_path + "\\attendance.jpg")
            subprocess.run(["peekingduck", "run"])
            result = json.load(open(res_path + "\\result.json"))

            for file in glob.glob(f"{res_path}\\*"):
                os.remove(file)

            for file in glob.glob(f"{images_path}\\*"):
                os.remove(file)
            
            for reg in result["regs"]:
                record.insert_one({"reg": str(reg), "date": date, "time": time})

            return flask.redirect(flask.url_for("dashboard"))

        except Exception:
            return flask.redirect(flask.url_for("dashboard"))

@app.route('/editStudent', methods=['GET', 'POST'])
def edit_student():
    if not "adminNum" in flask.session:
        return flask.redirect(flask.url_for("home"))
    else:
        if flask.request.method == "GET":
            student_info = student.find_one({"_id": ObjectId(flask.request.args["id"])})
            return flask.render_template('editStudent.html', student_info = student_info)
        else:
            print(flask.request.form)
            student.find_one_and_update({"_id": ObjectId(flask.request.args["id"])}, {"$set": {"reg": int(flask.request.form["reg"]), "name": flask.request.form["name"], "class": flask.request.form["class"]}})
    return flask.redirect(flask.url_for("dashboard"))

@app.route('/editAttendance', methods=['GET', 'POST'])
def edit_attendance():
    if not "adminNum" in flask.session:
        return flask.redirect(flask.url_for("home"))
    else:
        if flask.request.method == "GET":
            record_info = record.find_one({"_id": ObjectId(flask.request.args["id"])})
            record_info["name"] = student.find_one({"reg": int(record_info["reg"])})["name"]
            return flask.render_template('editAttendance.html', record_info = {"name": record_info["name"], "reg": record_info["reg"], "_id": record_info["_id"], "time": record_info["time"], "date": record_info["date"]})
        else:
            print(flask.request.form)
            record.find_one_and_update({"_id": ObjectId(flask.request.form["_id"])}, {"$set": {"time": flask.request.form["time"], "date": flask.request.form["date"]}})
    return flask.redirect(flask.url_for("dashboard"))


app.run()