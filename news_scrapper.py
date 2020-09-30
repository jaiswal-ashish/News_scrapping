import json
import newspaper
import pymongo
from datetime import datetime

# connecting to db
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.intelli
    # creating unique index
    db.news.create_index(
        [("title", 1), ("source", 1), ("story_date", 1)], unique=True)
except:
    print("Error.....")

# loading input file date
with open("sites.json") as data:
    sites = json.load(data)

today = datetime.now().strftime("%B %d, %Y")  # get today's date
news = []
maxx = 5

# traverse over each website and scrape news articles
for site, address in sites.items():
    paper = newspaper.build(address['link'])
    count = 0
    for art in paper.articles:
        if count >= maxx:
            break
        try:
            art.download()
            art.parse()
        except Exception as e:
            print("Continue download..")
            continue
        if art.publish_date is None:
            continue
        count = count + 1
        article = {}
        article['title'] = art.title
        article['source'] = site
        article['link'] = art.url
        article['current_date'] = today
        article['author'] = art.authors
        article['story_date'] = art.publish_date.strftime("%B %d, %Y")
        art.nlp()
        article['body'] = art.summary
        article['topics'] = art.keywords
        # print(json.dumps(article, indent=4))
        news.append(article)

# to create file using today's date and save the data
filename = today + '.json'
try:
    with open(filename, 'w') as output:
        json.dump(news, output, indent=4)
except Exception as e:
    print(e)

# to insert each scraped article in database
for i in news:
    try:
        db.news.insert_one(i)
    except Exception as ex:
        print("Database Insert error....")
