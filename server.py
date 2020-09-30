from flask import Flask, Response, request  # for server request and response
import pymongo  # to communicate with mongodb
import json  # to view the response in json

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.intelli
except:
    print("Error.....")


# to get the actual news within the given date range and source
@app.route("/news", methods=["POST"])
def news():
    try:
        res = db.news.find({"source": request.form["source"], "current_date": {
            "$gte": request.form["startDate"],
            "$lte": request.form["endDate"]
        }
        }, {"_id": 0})
        news = []
        for doc in res:
            news.append(doc)
        return Response(
            response=json.dumps(news),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)


# to get the count of news articles within the given date range and source
@app.route("/count", methods=["POST"])
def count():
    try:
        res = db.news.count_documents({"source": request.form["source"], "current_date": {
            "$gte": request.form["startDate"],
            "$lte": request.form["endDate"]
        }
        })
        return Response(
            response=json.dumps({"No. of articles": f"{res}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(port=80, debug=True)
