from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data_db")
mongo.db.data_mars.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.data_mars.find_one()

    # Return template and data
    return render_template("index.html", scraped=mars_data)


@app.route("/scrape")
def scrape():    
    #m_collection = db.data_mars
    mongo.db.data_mars.drop()

    mars_scrape = scrape_mars.scrape()
   
    #m_collection.update({},mars_scrape,upsert=True)
    mongo.db.data_mars.insert_one(mars_scrape)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)