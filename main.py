from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random2 import choice
from flask import jsonify
from sqlalchemy import text

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def get_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random():
    # get the random  the cafe from database
    all_cafes = Cafe.query.all()
    random_cafe = choice(all_cafes)
    return jsonify(cafe=random_cafe.get_dict())


# all cafes
@app.route("/all", methods=["GET"])
def get_all_cafe():
    all_cafes = Cafe.query.all()
    cafes_list_dict = []
    for cafe in all_cafes:
        cafes_list_dict.append(cafe.get_dict())
    return jsonify(cafe=cafes_list_dict)


@app.route("/search", methods=["GET"])
def search():
    loc = request.args.get('loc')
    all_cafes = Cafe.query.filter_by(location=loc.title()).all()
    if all_cafes != []:
        cafes_location = []
        for cafe in all_cafes:
            cafes_location.append(cafe.get_dict())
        return jsonify(cafe=cafes_location)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location"})


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        seats=request.form.get("seats"),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        has_sockets=bool(request.form.get("has_sockets")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        coffee_price=request.form.get("coffee_price")
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe"})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["GET", "PATCH"])
def update_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe_info = Cafe.query.filter_by(id=cafe_id).first()
    if cafe_info:
        cafe_info.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the coffee price."}), 200
    else:
        return jsonify(response={"error": "cafe not found"}), 400


## HTTP DELETE - Delete Record
@app.route("/cafe_closed/<cafe_id>", methods=["DELETE"])
def remove_cafe(cafe_id):
    secret_key = request.args.get("api_key")
    cafe_info = Cafe.query.filter_by(id=cafe_id).first()
    if cafe_info:
        if secret_key == "delete":
            db.session.delete(cafe_info)
            db.session.commit()
            return jsonify(response={"success": "Successfully remove the cafe"}), 200
        else:
            return jsonify(response={"Not Found": "Enter the valid API key"}), 404
    else:
        return jsonify(response={"Forbidden": "Cafe  not found"}), 403


if __name__ == '__main__':
    app.run(debug=True)
