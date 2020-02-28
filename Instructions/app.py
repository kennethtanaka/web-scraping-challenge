# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

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
def scrape():
    mars_data = mongo.db.mars_data

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


# create route that renders index.html template
#@app.route("/")
#def echo():
    #return render_template("index.html", text="Ken Flask server", subtitle="")

# Bonus add a new route
#@app.route("/bonus")
#def bonus():

    #return render_template("bonus.html", text="ken second page")

