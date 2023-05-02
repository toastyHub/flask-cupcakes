from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'toasty-secret'

connect_db(app)

@app.route('/')
def index():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


# *****************************
# RESTFUL JSON API
# *****************************
def serialize_cupcake(cupcake):
    """
    Serializes a Cupcake object into a dictionary.

    Args:
        cupcake (Cupcake): The Cupcake object to be serialized.

    Returns:
        dict: A dictionary representation of the Cupcake object, with keys 'id',
        'flavor', 'size', 'rating', and 'image'. The values are the corresponding
        field values of the Cupcake object.

    """
    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    """
    Returns a JSON representation of all cupcakes in the database.

    Returns:
        flask.Response: A Flask response object that contains a JSON representation
        of all cupcakes in the database. The response has a 'cupcakes' key that maps
        to a list of dictionaries, where each dictionary is a serialized Cupcake object.
        The keys of the dictionary are 'id', 'flavor', 'size', 'rating', and 'image'.

    """
     # Retrieve all cupcakes from the database
    cupcakes = Cupcake.query.all()
    # Serialize the cupcakes into a list of dictionaries
    serialized = [serialize_cupcake(c) for c in cupcakes]
    # Return the serialized cupcakes as a JSON response
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
    """
    Returns a JSON representation of a single cupcake.

    Args:
        id (int): The ID of the cupcake to retrieve.

    Returns:
        flask.Response: A Flask response object that contains a JSON representation
        of the specified cupcake. The response has a 'cupcake' key that maps to a
        dictionary, which is a serialized Cupcake object. The keys of the dictionary
        are 'id', 'flavor', 'size', 'rating', and 'image'.

    """
    # Get the Cupcake object with the specified ID from the database, or return a 404
    # 404 error if no matching object is found
    cupcake = Cupcake.query.get_or_404(id)
    # Serialize the Cupcake object into a dictionary
    serialized = serialize_cupcake(cupcake)
    # Return a JSON response containing the serialized Cupcake dictionary
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """
    Creates a new cupcake in the database.

    Returns:
        flask.Response: A Flask response object that contains a JSON representation
        of the newly created cupcake. The response has a 'cupcake' key that maps to a
        dictionary, which is a serialized Cupcake object. The keys of the dictionary
        are 'id', 'flavor', 'size', 'rating', and 'image'.
        
    """
    data = request.json
    try:
        # Get the fields for the new cupcake from the request body
        flavor = data['flavor']
        size = data['size']
        rating = data['rating']
        image = data['image']
        

        # Create a new Cupcake object with the specified fields
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image or None)
        # Add the new cupcake to the database
        db.session.add(new_cupcake)
        db.session.commit()
        # Serialize the new cupcake into a dictionary
        serialized = serialize_cupcake(new_cupcake)
        return (jsonify(cupcake=serialized), 201)
    except KeyError:
        # If the request is missing required fields, return an error
        message = {'error': 'Missing required fields'}
        return (jsonify(message), 400)
    
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """
    Updates an existing cupcake in the database with the specified ID.

    Args:
        id (int): The ID of the cupcake to update.

    Returns:
        flask.Response: A Flask response object that contains a JSON representation
        of the updated cupcake. The response has a 'cupcake' key that maps to a dictionary,
        which is a serialized Cupcake object. The keys of the dictionary are 'id', 'flavor',
        'size', 'rating', and 'image'.

    """
    # Retrieve the cupcake with the specified ID, or raise a 404 error if not found
    cupcake = Cupcake.query.get_or_404(id)
    
    # Update the cupcake's properties based on the request JSON data
    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    
    # Serialize the updated cupcake into a dictionary and commit changes to the database
    serialized = serialize_cupcake(cupcake)
    db.session.commit()
    
    # Return a JSON response containing the serialized Cupcake dictionary
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete a specific cupcake by its ID.

    Args:
        id (int): The ID of the cupcake to be deleted.

    Returns:
        dict: A JSON object with a message indicating that the cupcake was deleted.

    Raises:
        404 Error: If no cupcake with the specified ID is found.
    """
    
    # Get the cupcake with the specified ID, or return a 404 error if it doesn't exist
    cupcake = Cupcake.query.get_or_404(id)
    
    # Delete the cupcake from the database
    db.session.delete(cupcake)
    db.session.commit()
    
    # Return a JSON object with a message indicating that the cupcake was deleted
    message = {'message': 'Cupcake deleted'}
    return jsonify(message)


