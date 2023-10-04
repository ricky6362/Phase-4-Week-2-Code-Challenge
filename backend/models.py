from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(250), nullable=False)
    restaurant_address = db.Column(db.String(250), nullable=False)

    # relationship to restaurant_pizza class
    pizza = db.relationship('RestaurantPizza', back_populates='restaurant')

class Pizza(db.Model):
    __tablename__ = 'pizza'

    pizza_id = db.Column(db.Integer, primary_key=True)
    pizza_name = db.Column(db.String(100), nullable=False)
    pizza_ingredients = db.Column(db.String(250), nullable=False)

    # realtionship to the restaurant_pizza class
    restaurant = db.relationship('RestaurantPizza', back_populates='pizza')

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    restaurant_pizza_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.pizza_id'), nullable=False)

    # validation for the price
    @validates('price')
    def price_validator(self, key, value):
        if not (1 <= value <= 30):
            raise ValueError('Price should be a value ranging from 1 to 30.')
        return value
    
    price = db.Column(db.Float, nullable=False)

    # relationship to the pizza and resataurant classes
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizza')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizza')
   
