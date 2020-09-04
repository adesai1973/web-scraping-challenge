from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import json
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    news_data = mongo.db.news_collection.find_one()
    image_data = mongo.db.image_collection.find_one()
    #facts_data = mongo.db.facts_collection.find_all()
    facts_data = mongo.db.facts_collection.find()
    print(facts_data[0]['key'], facts_data[0]['value'])
    print(facts_data.count())
    mars_hems_data = mongo.db.mars_hems_data.find_one()
    print(mars_hems_data['title1'])
    print(mars_hems_data['img_url1'])
    # Return template and data
    return render_template("index.html", mars_news=news_data, mars_image=image_data, mars_facts=facts_data, mars_hems=mars_hems_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_mars_news()
    print(mars_data)
    # Update the Mongo database using update and upsert=True
    mongo.db.news_collection.update({}, mars_data, upsert=True)

    # Run the scrape function
    featured_image_url = scrape_mars.scrape_mars_image()
    print(featured_image_url)
    # Update the Mongo database using update and upsert=True
    mongo.db.image_collection.update({}, featured_image_url, upsert=True)

    # Run the scrape function
    mars_facts_data = scrape_mars.scrape_mars_facts()
    print(mars_facts_data)
    records = json.loads(mars_facts_data.T.to_json()).values()
    mongo.db.facts_collection.drop()
    mongo.db.facts_collection.insert(records)

    # Run the scrape function
    mars_hems_data = scrape_mars.scrape_mars_hemispheres()
    print(mars_hems_data)
    mongo.db.mars_hems_data.update({}, mars_hems_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
