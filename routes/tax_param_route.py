from flask import Blueprint, request, jsonify, render_template
from sqlalchemy.exc import IntegrityError
from database import CarTax, Region, db

tax_param_route_bp = Blueprint('tax_param_route_bp', __name__)


@tax_param_route_bp.route('/v1/tax-param/add', methods=['POST'])
def add_car_tax_param():
    region_id = request.form.get('city_id')
    from_hp_car = request.form.get('from_hp_car')
    to_hp_car = request.form.get('to_hp_car')
    from_production_year_car = request.form.get('from_production_year_car')
    to_production_year_car = request.form.get('to_production_year_car')
    rate = request.form.get('rate')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден"}), 400

    existing_tax_param = CarTax.query.filter_by(
        city_id=region_id,
        from_hp_car=from_hp_car,
        to_hp_car=to_hp_car,
        from_production_year_car=from_production_year_car,
        to_production_year_car=to_production_year_car,
    ).first()

    if existing_tax_param:
        return jsonify({"error": "Налоговый параметр уже существует"}), 400

    new_tax_param = CarTax(
        city_id=region_id,
        from_hp_car=from_hp_car,
        to_hp_car=to_hp_car,
        from_production_year_car=from_production_year_car,
        to_production_year_car=to_production_year_car,
        rate=rate,
    )

    try:
        db.session.add(new_tax_param)
        db.session.commit()
        return jsonify({"message": "Налоговый параметр успешно добавлен"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Ошибка целостности"}), 400


@tax_param_route_bp.route('/v1/tax-param/update', methods=['POST'])
def update_car_tax_param():
    tax_param_id = request.form.get('id')
    region_id = request.form.get('city_id')
    from_hp_car = request.form.get('from_hp_car')
    to_hp_car = request.form.get('to_hp_car')
    from_production_year_car = request.form.get('from_production_year_car')
    to_production_year_car = request.form.get('to_production_year_car')
    rate = request.form.get('rate')

    region = Region.query.get(region_id)

    if not region:
        return jsonify({"error": "Регион не найден"}), 400

    existing_tax_param = CarTax.query.filter_by(
        city_id=region_id,
        from_hp_car=from_hp_car,
        to_hp_car=to_hp_car,
        from_production_year_car=from_production_year_car,
        to_production_year_car=to_production_year_car,
    ).first()

    if existing_tax_param and existing_tax_param.id != tax_param_id:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    tax_param = CarTax.query.get(tax_param_id)

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    tax_param.city_id = region_id
    tax_param.from_hp_car = from_hp_car
    tax_param.to_hp_car = to_hp_car
    tax_param.from_production_year_car = from_production_year_car
    tax_param.to_production_year_car = to_production_year_car
    tax_param.rate = rate

    db.session.commit()
    return jsonify({"message": "Налоговый параметр успешно обновлен"}), 200


@tax_param_route_bp.route('/v1/tax-param/delete', methods=['POST'])
def delete_car_tax_param():
    tax_param_id = request.form.get('id')

    tax_param = CarTax.query.get(tax_param_id)

    if not tax_param:
        return jsonify({"error": "Налоговый параметр не найден"}), 400

    db.session.delete(tax_param)
    db.session.commit()
    return jsonify({"message": "Налоговый параметр успешно удален"}), 200


@tax_param_route_bp.route('/v1/tax-param/get/all', methods=['GET'])
def get_all_car_tax_params():
    tax_params = CarTax.query.all()

    result = []
    for tax_param in tax_params:
        result.append({
            "city_id": tax_param.city_id,
            "from_hp_car": tax_param.from_hp_car,
            "to_hp_car": tax_param.to_hp_car,
            "from_production_year_car": tax_param.from_production_year_car,
            "to_production_year_car": tax_param.to_production_year_car,
            "rate": float(tax_param.rate),
        })

    return jsonify(result), 200


@tax_param_route_bp.route('/web/tax-param', methods=['GET'])
def list_car_tax_params():
    car_tax_params = CarTax.query.all()
    return render_template('tax-param-list.html', tax_params=car_tax_params)


@tax_param_route_bp.route('/web/tax-param/add', methods=['GET'])
def add_car_tax_param_form():
    return render_template('tax-param-add.html')


@tax_param_route_bp.route('/web/tax-param/update', methods=['GET'])
def update_car_tax_param_form():
    return render_template('tax-param-update.html')


@tax_param_route_bp.route('/web/tax-param/delete', methods=['GET'])
def delete_car_tax_param_form():
    return render_template('tax-param-delete.html')

