# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
#import scrape_mars
#from scrape_mars2 import scrape
import scrape_mars2

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

# create route that renders index.html template
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()

    # return template and data
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars_data

    # Run the scrape function
    mars_data = scrape_mars2.scrape()

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
