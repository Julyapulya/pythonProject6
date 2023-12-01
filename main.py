from config import app, db
from routes.region_routes import region_bp
from routes.tax_param_route import tax_param_route_bp
from routes.tax_route import tax_bp

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.register_blueprint(region_bp)
    app.register_blueprint(tax_bp)
    app.register_blueprint(tax_param_route_bp)
    app.run()


