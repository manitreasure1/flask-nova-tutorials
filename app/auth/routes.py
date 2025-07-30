
from app.schemas import UserCreate, UserOut, LoginOut, LoginInput
from app.utils.security import hash_password, verify_password
from flask_nova import NovaBlueprint, status, HTTPException
from app.models.revoke import RevokedToken
from flask import jsonify, make_response
from app.models.users import Users
from app.extensions import db
from flask_jwt_extended import( create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt_identity,
                                get_jwt)


auth_bp = NovaBlueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/", summary="Register a new user",methods=["POST"], response_model=UserOut, tags=["Auth"])
def register_user(data: UserCreate):
    existing = Users.query.filter(
        (Users.email == data.email) | (Users.username == data.username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.CONFLICT,
            detail="User with this email or username already exists",
            title="Conflict"
        )

    user = Users(
        firstname=data.firstname, # type: ignore
        lastname=data.lastname, # type: ignore
        email=data.email, # type: ignore
        username=data.username, # type: ignore
        password_hash=hash_password(data.password) # type: ignore
    )

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    return make_response(jsonify({
            "message": "User created successfully",
            "username": user.username,
            "email": user.email
        }), status.CREATED)


@auth_bp.route("/login", methods=["POST"], summary="Login user", response_model=LoginOut, tags=["Auth"])
def login(data: LoginInput):
    user = Users.query.filter_by(username=data.username).first()

    if not user or not verify_password(user.password_hash, data.password):
        raise HTTPException(
            status_code=status.UNAUTHORIZED,
            detail="Invalid username or password",
            title="Unauthorized"
        )

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return make_response(jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), status.OK)


@auth_bp.route("/refresh", methods=["POST"], summary="Refresh access token", tags=["Auth"])
@jwt_required(refresh=True)
def refresh_access_token():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    
    return make_response(jsonify({
        "access_token": new_access_token
    }), status.OK)


@auth_bp.route("/me", methods=["GET"], summary="Get current user", response_model=UserOut, tags=["Auth"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = Users.query.get(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.NOT_FOUND,
            detail="User not found",
            title="Not Found"
        )

    return make_response(jsonify({
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "username": user.username,
            "approved": user.approved,
        }), status.OK)


@auth_bp.route("/logout", methods=["POST"], summary="Logout user", tags=["Auth"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked = RevokedToken(jti=jti) # type: ignore
    db.session.add(revoked)
    db.session.commit()
    return make_response(jsonify({"msg": "Successfully logged out"}), status.OK)
