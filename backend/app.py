# defining the import statements
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

# creating an instance of the flask class
app = Flask(__name__)

# configuring of the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# migrating the database
migrate = Migrate(app, db)

# initializing the flask app
db.init_app(app)

# creating the different routes 
@app.route('/')
def default_tab():
    return "<h1>Welcome to my Restaurants Full Stack Site</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    # accessing, formatting, convert to json
    restaurants = Restaurant.query.all()
    restaurants_data = [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        for restaurant in restaurants
    ]
    return jsonify(restaurants_data)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    # Query the database to find the restaurant by its ID
    restaurant = Restaurant.query.get(id)

    # Check if the restaurant exists
    if not restaurant:
        # If the restaurant does not exist, return an error response with status code 404 (Not Found)
        return jsonify({"error": "Restaurant not found"}), 404

    # If the restaurant exists, build the response JSON
    restaurant_data = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "pizzas": [
            {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients,
            }
            for pizza in restaurant.pizzas  
        ]
    }

    # Return the JSON response with status code 200 (OK)
    return jsonify(restaurant_data), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    # Query the database to find the restaurant by its ID
    restaurant = Restaurant.query.get(id)

    # Check if the restaurant exists
    if not restaurant:
        # If the restaurant does not exist, return an error response with status code 404 (Not Found)
        return jsonify({"error": "Restaurant not found"}), 404

    # Delete associated RestaurantPizza records
    associated_pizzas = RestaurantPizza.query.filter_by(restaurant_id=id).all()
    for pizza in associated_pizzas:
        db.session.delete(pizza)

    # Delete the restaurant itself
    db.session.delete(restaurant)
    db.session.commit()

    # Return an empty response with status code 204 (No Content) to indicate successful deletion
    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Query the database to fetch all pizza data
    pizzas = Pizza.query.all()

    # Convert the pizza data into the desired JSON format
    pizza_data = [
        {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients,
        }
        for pizza in pizzas
    ]

    # Return the JSON response
    return jsonify(pizza_data)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    # Parse the request JSON data
    data = request.json

    # Extract the properties from the request data
    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    # Validate the request data
    if not (price and pizza_id and restaurant_id):
        return jsonify({"errors": ["Missing required data"]}), 400

    # Check if the specified Pizza and Restaurant exist
    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not (pizza and restaurant):
        return jsonify({"errors": ["Pizza or Restaurant not found"]}), 404

    # Create a new RestaurantPizza instance
    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)

    # Save the new RestaurantPizza to the database
    db.session.add(restaurant_pizza)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["Validation errors"]}), 400

    # Return the data related to the Pizza
    pizza_data = {
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients,
    }
    
    return jsonify(pizza_data), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)