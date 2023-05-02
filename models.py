from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMG = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """
    A class representing a cupcake.

    Fields:
        id (int): The unique ID of the cupcake. Primary key.
        flavor (str): The flavor of the cupcake. Required field.
        size (str): The size of the cupcake. Required field.
        rating (float): The rating of the cupcake. Required field.
        image (str): The URL of the image associated with the cupcake. Required field.

    """
    __tablename__ = 'cupcakes'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    
    flavor = db.Column(
        db.String(20),
        nullable=False)
    
    size = db.Column(
        db.String(20),
        nullable=False)
    
    rating = db.Column(
        db.Float,
        nullable=False)
    
    image = db.Column(
        db.String(200),
        nullable=False,
        default=DEFAULT_IMG)