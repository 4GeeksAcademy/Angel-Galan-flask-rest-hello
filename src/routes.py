from flask import Blueprint, jsonify, request
from models import db, User, People, Planet, Favorite


api = Blueprint('api', __name__)



@api.route('/user', methods=['GET'])
def get_all_users():
    
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route('/people', methods=['GET'])
def get_all_people():
    
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200

@api.route('/planet', methods=['GET'])
def get_all_planets():
   
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200



@api.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
   
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Persona no encontrada"}), 404
    return jsonify(person.serialize()), 200

@api.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200



@api.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([f.serialize() for f in favorites]), 200



@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

    user_id = request.json.get("user_id", 1)
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if not user or not planet:
        return jsonify({"error": "Usuario o planeta no encontrado"}), 404
    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito de planeta añadido"}), 201

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
   
    user_id = request.json.get("user_id", 1)
    user = User.query.get(user_id)
    person = People.query.get(people_id)
    if not user or not person:
        return jsonify({"error": "Usuario o personaje no encontrado"}), 404
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito de personaje añadido"}), 201



@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    
    favorite = Favorite.query.filter_by(planet_id=planet_id, user_id=1).first()
    if not favorite:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito de planeta eliminado"}), 200

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
   
    favorite = Favorite.query.filter_by(people_id=people_id, user_id=1).first()
    if not favorite:
        return jsonify({"error": "Favorito no encontrado"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito de personaje eliminado"}), 200



@api.route('/create_test_user', methods=['POST'])
def create_test_user():
    
    user = User(email="test@example.com", is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201








