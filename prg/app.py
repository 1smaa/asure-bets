import os
from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, request
from flask_cors import CORS
from packages.sql_builder import *
from packages.decorators import *
from packages.socketconn import *
import mysql.connector
import functools
import string
import random
import socket
ARB_URL = "http://127.0.0.1:5001/fetch"
TOKEN = ""
PUBLIC_RSA = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCNRVrmakiSSZnMev3wFP8VgA5eyIjk3Dv2QyH9jLfiSAYAoMDSb0NbUpA72N01LLHMOGcgHzTWmrOlDUXnSs8mZPdhg4yK8/Fc6+3kz+nABn00DvfIESSBH91kFssxS0sUJ+07qNd8g17jeapJ+79Yho327dGVbHkbJCRQPMsi6QIDAQAB"
CWD = os.getcwd()
WEB_CWD = os.path.join(CWD, "static_web_folder")
D = {
    0: "date",
    1: "sport",
    2: "m",
    3: "ROI",
    4: "calc",
    5: "bookmaker1",
    6: "bet1",
    7: "odds1",
    8: "bookmaker2",
    9: "bet2",
    10: "odds2",
    11: "bookmaker3",
    12: "bet3",
    13: "odds3",
    14: "time"
}
UNAUTHORIZED_REQUEST = None, 401
FAILED_REQUEST = None, 500
HOST = "127.0.0.1"
PORT = 1024

app = Flask(__name__)
api = Api(app)
CORS(app)

## WEB PAGES ##


@app.route("/")
def home() -> str:
    return render_template(os.path.join(WEB_CWD, "home.html"))


@app.route("/news")
def news() -> str:
    return render_template(os.path.join(WEB_CWD, "news.html"))


@app.route("/advices")
def advices() -> str:
    return render_template(os.path.join(WEB_CWD, "advices.html"))


@app.route("/aff")
def affiliation() -> str:
    return render_template(os.path.join(WEB_CWD, "affiliation.html"))


@app.route("/login")
def login() -> str:
    return render_template(os.path.join(WEB_CWD, "login.html"))


@app.route("/register")
def register() -> str:
    return render_template(os.path.join(WEB_CWD, "register.html"))

## RESTFUL API ##


def default(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            return {"result": False}, 200
        else:
            return {"result": True}, 200
    return wrapper


def get_key() -> str:
    return ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))


def get_mysql() -> tuple:
    mydb = mysql.connector.connect(
        host="localhost",
        user="test",
        password="6JNNFJ3WX29mUvHT",
        database="arbmaster"
    )
    cursor = mydb.cursor()
    return mydb, cursor


def close(cursor, db) -> None:
    cursor.close()
    db.close()


def decode(h: int, t: int) -> int:
    return int(h)-int(float(t))


def auth(biri: int, session: str) -> bool:
    q = SelectQuery()
    q.set(attr=["id", "biri1", "biri2", "biri3", "active"], table="users", conditions={
        "sessionKey": session
    })
    db, cursor = get_mysql()
    cursor.execute(q.get())
    result = cursor.fetchall()
    if len(result) != 1:
        return False
    id, biri1, biri2, biri3, active = result[0]
    if not (biri1 == biri or biri2 == biri or biri3 == biri) or not active:
        if biri2 is None:
            set_biri(cursor, db, id, 2, biri)
            close(db, cursor)
            return True
        if biri3 is None:
            set_biri(cursor, db, id, 3, biri)
            close(db, cursor)
            return True
        return False
    close(db, cursor)
    return True


def set_biri(cursor, db, email: str, n: int, biri: str) -> None:
    cursor.execute("UPDATE users SET biri{n}={biri} WHERE email='{email}'".format(
        n=n, biri=biri, email=email))
    db.commit()


class Auth(Resource):
    def post(self) -> tuple:
        args = request.get_json(force=True)
        email, password, biri = args["email"], args["password"], args["biri"]
        db, cursor = get_mysql()
        q = SelectQuery()
        result = []
        q.set(attr=["biri1", "biri2", "biri3", "active"], table="users", conditions={
            "email": email,
            "pwd": int(password)
        })
        cursor.execute(q.get())
        result = cursor.fetchall()
        if len(result) != 1:
            return UNAUTHORIZED_REQUEST
        biri1, biri2, biri3, status = result[0]
        if not (biri1 == biri or biri2 == biri or biri3 == biri):
            if biri2 is None:
                set_biri(cursor, db, email, 2, biri)
            elif biri3 is None:
                set_biri(cursor, db, email, 3, biri)
            else:
                close(cursor, db)
                print(biri)
                return UNAUTHORIZED_REQUEST
        if not status:
            close(cursor, db)
            return UNAUTHORIZED_REQUEST
        key = get_key()
        q = UpdateQuery()
        q.set(table="users",
              attr={
                  "sessionKey": key
              },
              conditions={
                  "email": email
              })
        try:
            cursor.execute(q.get())
            db.commit()
        except:
            close(cursor, db)
            return UNAUTHORIZED_REQUEST
        else:
            close(cursor, db)
            return {"session": key}, 200


def already_registered(cursor, email: str) -> bool:
    q = SelectQuery()
    q.set(attr=["active"], table="users", conditions={
        "email": email
    })
    cursor.execute(q.get())
    result = cursor.fetchall()
    return len(result) != 0


class Affiliation:
    @staticmethod
    def check_affiliation(cursor, affiliation: str) -> bool:
        q = SelectQuery()
        q.set(attr={
            "active"
        },
            table="users",
            conditions={
            "aff": affiliation
        })
        cursor.execute(q.get())
        result = cursor.fetchall()
        if len(result) != 1 or not result[0][0]:
            return False
        else:
            return True

    @staticmethod
    def generate_affiliation() -> str:
        return ''.join([random.choice(string.ascii_uppercase+string.digits) for _ in range(10)])

    @staticmethod
    def increment(db, cursor, affiliation: str) -> int:
        q = SelectQuery()
        q.set(attr=["first_lv", "aff_pass"],
              table="users",
              conditions={
            "aff": affiliation
        })
        cursor.execute(q.get())
        result = cursor.fetchall()
        if len(result) != 1:
            raise Exception("Affiliatione non valida.")
        first, aff = result[0][0], result[0][1]
        qu = UpdateQuery()
        qu.set(attr={
            "first_lv": first+1
        },
            table="users",
            conditions={
                "aff": affiliation
        }
        )
        cursor.execute(qu.get())
        db.commit()
        q.set(attr=["second_lv"],
              table="users",
              conditions={
            "aff": aff
        })
        cursor.execute(q.get())
        result = cursor.fetchall()
        if len(result) != 1:
            raise Exception("Affiliazione non valida.")
        second = result[0][0]
        qu.set(attr={
            "second_lv": second+1
        },
            table="users",
            conditions={
            "aff": aff
        })
        cursor.execute(qu.get())
        db.commit()
        return 1


class Register(Resource):
    @return_catch
    def post(self) -> tuple:
        args = request.get_json(force=True)
        name, last, email, password, biri, aff = args["name"], args[
            "lastName"], args["email"], args["password"], args["biri"], args["affiliation"]
        db, cursor = get_mysql()
        if already_registered(cursor, email):
            return {"status": 0,
                    "message": "Esiste già un account con questo indirizzo email.",
                    "session": ""}, 200
        if not Affiliation.check_affiliation(cursor, aff):
            return {"status": 0,
                    "message": "Il codice amico inserito non esiste.",
                    "session": ""}, 200
        q = InsertQuery()
        key = get_key()
        q.set(table="users", fields={
            "name": name,
            "last": last,
            "email": email,
            "pwd": password,
            "biri1": biri,
            "sessionKey": key,
            "aff": Affiliation.generate_affiliation(),
            "aff_pass": aff
        })
        cursor.execute(q.get())
        db.commit()
        close(cursor, db)
        return {"status": 1,
                "message": "Account registrato correttamente.",
                "session": key}, 200


class GetNews(Resource):
    @return_catch
    def get(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("biri", required=True, type=int, location="args")
        parser.add_argument("page", required=True, type=int, location="args")
        args = parser.parse_args()
        session = request.headers.get("Authorization").replace("Bearer ", "")
        biri, page = args["biri"], args["page"]
        if not auth(biri, session):
            return UNAUTHORIZED_REQUEST
        q = SelectQuery()
        db, cursor = get_mysql()
        q.set(attr=["*"], table="news", conditions={
            "page": page
        })
        cursor.execute(q.get())
        result = cursor.fetchall()
        close(cursor, db)
        return {"result": result}, 200


class GetSource(Resource):
    @return_catch
    def get(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("link", required=True, type=str, location="args")
        args = parser.parse_args()
        link = args["link"]
        path = os.path.join(CWD, link)
        if os.path.exists(path):
            name, extension = os.path.splitext(path)
            if extension != ".html":
                return UNAUTHORIZED_REQUEST
            with open(path, mode="r", encoding="utf-8") as f:
                html = f.read()
            return {"html": html}, 200
        else:
            return {"html": ""}, 200


class Fetch(Resource):
    @return_catch
    def get(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("biri", required=True, type=int, location="args")
        parser.add_argument("sport", required=True, type=str, location="args")
        parser.add_argument("bookmaker", required=True,
                            type=str, location="args")
        args = parser.parse_args()
        session = request.headers.get("Authorization").replace("Bearer ", "")
        if not auth(args["biri"], session):
            return UNAUTHORIZED_REQUEST
        keys = ["sport", "bookmaker"]
        p = []
        for key in keys:
            p.append(args[key])
        string = ' '.join(p)
        data = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(encode(bytes(string, encoding="utf-8")))
            buffer = s.recv(1024)
            data = [buffer]
            while buffer:
                buffer = s.recv(1024)
                data.append(buffer)
        strBuffers = ""
        for buffer in data:
            strBuffers += buffer.decode("utf-8")
        l = [row.split("_") for row in strBuffers.split(";")]
        return list(filter(lambda x: len(x) > 1, l)), 200


class GetAffiliation(Resource):
    @catch
    def get(self) -> tuple:
        parser = reqparse.RequestParser()
        parser.add_argument("biri", required=True, type=int, location="args")
        args = parser.parse_args()
        biri = args["biri"]
        session = request.headers.get("Authorization").replace("Bearer ", "")
        if not auth(biri, session):
            return UNAUTHORIZED_REQUEST
        db, cursor = get_mysql()
        q = SelectQuery()
        q.set(attr=["aff", "first_lv", "second_lv"],
              table="users",
              conditions={
            "sessionKey": session
        })
        cursor.execute(q.get())
        result = cursor.fetchall()
        if len(result) != 1:
            return UNAUTHORIZED_REQUEST
        row = result[0]
        response = {
            "aff": row[0],
            "firstLv": row[1],
            "secondLv": row[2]
        }
        cursor.close()
        db.close()
        return {"response": response}, 200


api.add_resource(Fetch, "/fetch")
api.add_resource(Auth, "/auth")
api.add_resource(Register, "/rgstr")
api.add_resource(GetNews, "/gtnws")
api.add_resource(GetSource, "/gtsrc")
api.add_resource(GetAffiliation, "/getaff")
