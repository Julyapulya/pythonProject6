from flask import Blueprint, request, jsonify, render_template
from database import CarTax

tax_bp = Blueprint('tax_bp', __name__)


@tax_bp.route('/v1/car/tax/calc', methods=['GET'])
def calculate_tax():
    region_id = request.args.get('city_id')
    production_year = int(request.args.get('production_year'))
    hp_car = int(request.args.get('hp_car'))

    tax_param = CarTax.query.filter(
        CarTax.city_id == region_id,
        CarTax.from_hp_car <= hp_car,
        CarTax.to_hp_car >= hp_car,
        CarTax.from_production_year_car <= production_year,
        CarTax.to_production_year_car >= production_year
    ).first()

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден по заданным критериям "}), 400

    tax = float(tax_param.rate) * hp_car
    return jsonify({"tax": tax}), 200


@tax_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
