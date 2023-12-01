from flask import Blueprint, request, render_template

from database import Region
from database import db

region_bp = Blueprint('region_bp', __name__)


@region_bp.route('/v1/region/add', methods=['POST'])
def add_region():
    region_id = request.form.get('id')
    name = request.form.get('name')

    existing_region = Region.query.filter_by(id=region_id).first()
    if existing_region:
        return {'message': 'Регион уже существует'}, 400

    region = Region(id=region_id, name=name)
    db.session.add(region)
    db.session.commit()

    return {'message': 'Регион успешно добавлен'}, 200


@region_bp.route('/v1/region/update', methods=['POST'])
def update_region():
    region_id = request.json.get('id')
    name = request.json.get('name')

    region = Region.query.filter_by(id=region_id).first()
    if not region:
        return {'message': 'Регион не найден'}, 400

    region.name = name
    db.session.commit()

    return {'message': 'Регион успешно обновлен'}, 200


@region_bp.route('/v1/region/delete', methods=['POST'])
def delete_region():
    region_id = request.json.get('id')

    region = Region.query.filter_by(id=region_id).first()
    if not region:
        return {'message': 'Регион не найден'}, 400

    db.session.delete(region)
    db.session.commit()

    return {'message': 'Регион успешно удален'}, 200


@region_bp.route('/web/region', methods=['GET'])
def list_regions():
    regions = Region.query.all()
    return render_template('region-list.html', regions=regions)


@region_bp.route('/web/region/add', methods=['GET'])
def add_region_form():
    return render_template('region-add.html')


@region_bp.route('/web/region/update', methods=['GET'])
def update_region_form():
    return render_template('region-update.html')


@region_bp.route('/web/region/delete', methods=['GET'])
def delete_region_form():
    return render_template('region-delete.html')

