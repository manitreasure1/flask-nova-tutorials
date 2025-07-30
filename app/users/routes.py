from flask_nova import NovaBlueprint, status, HTTPException
from  app.schemas import UpdateProfile
from app.models.users import Users
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import make_response
from app.extensions import db
from app.utils.security import hash_password


users = NovaBlueprint("users", __name__)



@users.route("/profile", methods=["PUT"], tags=["Users"])
@jwt_required()
def update_profile(update_data: UpdateProfile):
    user_id = get_jwt_identity()
    user = Users.query.get(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.NOT_FOUND,
            detail="User not found",
            title="Not Found"
        )
    print(update_data.model_dump())
    user_instance = UpdateProfile(**update_data.model_dump())  
    user_data = user_instance.model_dump(exclude_unset=True) 
    for key, value in user_data.items():
        setattr(user, key, value)
    db.session.commit()
    db.session.refresh(user)

    return make_response("", status.NO_CONTENT) 