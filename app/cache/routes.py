from flask import make_response
from flask_nova import NovaBlueprint, status
from app.extensions import cache
from flask_jwt_extended import jwt_required

cache_router = NovaBlueprint("cache", __name__)


@cache.cached(timeout=50)
@cache_router.route("/", tags=["Cache"])
@jwt_required()
def Home():
    return make_response("", status.OK)

