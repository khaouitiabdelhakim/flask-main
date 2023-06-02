from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import sqlite3
import json
from TSP_MASTER import TSP_Solver


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        first_stop = request.form.get('first-stop')
        final_stop = request.form.get('final-stop')
        intermediate_stops = request.form.getlist('stop-2')

        # Process the selected stops and redirect to the map route
        return redirect(url_for('views.map_view', first_stop=first_stop, final_stop=final_stop, intermediate_stops=intermediate_stops))

    # Connect to the database
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Retrieve the list of pharmacies from the database
    cursor.execute("SELECT nom FROM pharmacies")
    results = cursor.fetchall()
    pharmacies = [result[0] for result in results]

    # Close the database connection
    connection.close()

    return render_template('home.html', pharmacies=pharmacies, user=current_user)



@views.route('/api/pharmacies', methods=['GET'])
def get_pharmacies():
    # Retrieve the list of pharmacies from the database
    pharmacies = retrieve_pharmacies()

    # Return the list of pharmacies as JSON
    return jsonify(pharmacies)

@views.route('/api/coordinates', methods=['GET'])
def get_coordinates():
    # Retrieve the selected stops from the query parameters
    first_stop = request.args.get('first_stop')
    final_stop = request.args.get('final_stop')
    intermediate_stops = request.args.getlist('intermediate_stops')

    # Retrieve the coordinates from the database based on the selected stops
    coordinates = retrieve_coordinates(first_stop, final_stop, intermediate_stops)

    # Return the coordinates as JSON
    return jsonify(coordinates)

@views.route('/map', methods=['GET', 'POST'])
def map_view():
    """ 
    first_stop = request.args.get('first_stop')
    final_stop = request.args.get('final_stop')
    intermediate_stops = request.args.getlist('intermediate_stops') """

    first_stop = request.form["first-stop"]
    final_stop = request.form["final-stop"]
    intermediate_stops = []
    if request.form.get("stop-2"):
        intermediate_stops.append(request.form["stop-2"])
    if request.form.get("stop-3"):
        intermediate_stops.append(request.form["stop-3"])
    if request.form.get("stop-4"):
        intermediate_stops.append(request.form["stop-4"])
    if request.form.get("stop-5"):
        intermediate_stops.append(request.form["stop-5"])
    if request.form.get("stop-6"):
        intermediate_stops.append(request.form["stop-6"])
    if request.form.get("stop-7"):
        intermediate_stops.append(request.form["stop-7"])
    if request.form.get("stop-8"):
        intermediate_stops.append(request.form["stop-8"])
    if request.form.get("stop-9"):
        intermediate_stops.append(request.form["stop-9"])
    if request.form.get("stop-10"):
        intermediate_stops.append(request.form["stop-10"])


    # Retrieve the coordinates based on the selected stops
    coordinates = retrieve_coordinates(first_stop, final_stop, intermediate_stops)

    # Convert coordinates to JSON
    coordinates_json = json.dumps(coordinates)

    f = open("output.txt","w",encoding="UTF-8")
    f.write(coordinates_json)
    f.write("\n")
    #what to change

    pharmacies_tuples = []
    for key in coordinates:
        pharmacies_tuples.append(coordinates[key])

    omptimal = TSP_Solver(pharmacies_tuples,0)[1]
    

    coordinates = order_dictionary(coordinates,omptimal)

    l = []
    for key in coordinates:
        l.append(key)

    coordinates[l[0]+"2"] = coordinates[l[0]]

    coordinates_json = json.dumps(coordinates)
    
    f = open("last_output.txt","w",encoding="UTF-8")
    f.write(coordinates_json)
    f.close
    return render_template('map.html', coordinates=coordinates_json)


def order_dictionary(dictionary, order):
    ordered_dict = {}
    for index in order:
        key = list(dictionary.keys())[index]
        value = dictionary[key]
        ordered_dict[key] = value
    return ordered_dict






def retrieve_coordinates(first_stop, final_stop, intermediate_stops):
    # Connect to the database
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Retrieve the coordinates from the database based on the selected pharmacies
    query = "SELECT nom, latitude, longitude FROM pharmacies WHERE nom IN (?, ?{})".format(", ?" * len(intermediate_stops))
    params = [first_stop, final_stop] + intermediate_stops
    cursor.execute(query, params)
    results = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Create a dictionary to store the coordinates
    coordinates = {}
    for result in results:
        pharmacy_name, latitude, longitude = result
        coordinates[pharmacy_name] = [latitude, longitude]
    return coordinates

def retrieve_pharmacies():
    # Connect to the database
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Retrieve the list of pharmacies from the database
    query = "SELECT nom FROM pharmacies"
    cursor.execute(query)
    results = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Extract the pharmacy names from the results
    pharmacies = [result[0] for result in results]

    # Return the list of pharmacies
    return pharmacies






@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Perform desired actions with the form data (e.g., send email, store in database)

        return 'Thank you for your submission!'
    
    return render_template('contact.html', user=current_user)



@views.route('/page')
def custom_page():
    return render_template('page.html', user=current_user)

