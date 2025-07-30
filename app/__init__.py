import os
from dotenv import load_dotenv
from flask_nova import FlaskNova, status
from .extensions import db, jwt, migrate, cors, cache, limiter, bcrypt
from app.auth.routes import auth_bp
from app.users.routes import users
from app.cache.routes import cache_router
from config import Config
from flask import make_response, jsonify
from app.models.revoke import RevokedToken
from sqlalchemy import select

load_dotenv()  # Load from .env

def create_app():
    app = FlaskNova(__name__)

    config = Config()
    
    app.config.from_object(config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)
    # cache.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        stmt = select(RevokedToken).where(RevokedToken.jti == jti)
        return db.session.execute(stmt).scalar_one_or_none() is not None

    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return make_response(jsonify({"msg": "Token has been revoked"}), status.UNAUTHORIZED)


    

    # Register NovaBlueprints later
    app.setup_swagger(info={
            "title": "FlaskNova API test",
            "version": "0.1.0",
            "description": "Beautiful API for modern apps.",
            "termsOfService": "https://example.com/terms",
            "contact": {
                "name": "Team FlaskNova",
                "url": "https://github.com/flasknova",
                "email": "support@flasknova.dev"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        })
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(users)
    app.register_blueprint(cache_router)

    return app

