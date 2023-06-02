from flask import Blueprint, render_template, request

map_bp = Blueprint('map', __name__)

@map_bp.route('/map', methods=['GET'])
def show_map():
    # Retrieve the coordinates from the request or session
    coordinates = request.args.get('coordinates')  # Alternatively, you can store the coordinates in the session

    # Process the coordinates if necessary
    # ...

    return render_template('map.html', coordinates=coordinates)
