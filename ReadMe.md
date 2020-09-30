## **Steps to run the application**

### 1) Start the mongodb server
### 2) Command to fetch news articles and store in a file -- python news_scrapper.py
### 3) Command to run flask server for request and respose -- python server.py

**Routes Functions**
-> Both POST routes take 3 inputs as form data - source(like CNN, Reuters, HT), startDate(September 22, 2020), endDate(September 29, 2020)

/count -- to get number of news articles scraped from the given source and date range

/news -- to get actual news articles in json format from the given source and date range

![](/Images/SS1.png)
![](/Images/SS2.png)
