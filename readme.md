# Restaurant Pizza Full Stack Application

This is a full-stack web application for managing restaurants, pizzas, and restaurant-pizza associations. The application consists of a Flask-based backend for the server and a React-based frontend for the user interface.

## Project Structure

## Backend

The backend of the application is built using Flask, a Python web framework, and SQLAlchemy for database management. The `backend` folder contains the following important files:

- `app.py`: Defines the Flask application, API routes, and database configuration.
- `models.py`: Defines the database models (Restaurant, Pizza, RestaurantPizza) using SQLAlchemy.

## Frontend

The frontend of the application is built using React, a JavaScript library for building user interfaces. The `frontend` folder contains the React components for the user interface:

- `RestaurantList.js`: Displays a list of restaurants.
- `RestaurantDetail.js`: Displays details of a specific restaurant.
- `PizzaList.js`: Displays a list of pizzas.
- `RestaurantPizzaForm.js`: Allows users to create a new restaurant-pizza association.
- `App.js`: Main component defining the application's routes.

## Database

The application uses an SQLite database located in the `db` folder named `app.db` to store restaurant, pizza, and restaurant-pizza association data.

## Usage

1. Start the backend server by running `python backend/app.py` from the root directory.

2. Install frontend dependencies using `npm install` in the `frontend` directory.

3. Start the frontend application using `npm start` in the `frontend` directory.

4. Access the application in your web browser at `http://localhost:3000`.

## Dependencies

- Flask
- Flask-SQLAlchemy
- React
- React Router