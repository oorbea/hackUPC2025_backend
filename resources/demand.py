from flask import abort, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from marshmallow import ValidationError
from psycopg2 import IntegrityError

from db import db
from models.Demand import Demand
from models.User import User
from schemas import DemandPayloadSchema, DemandResponseSchema

blp = Blueprint('demand', __name__, description='Demand related CRUD operations.')

@blp.route('/')
class DemandCRUD(MethodView):
    """
    Demand CRUD operations.
    """
    @jwt_required()
    @blp.doc(security=[{"jwt": []}])
    @blp.arguments(DemandPayloadSchema)
    @blp.response(201, DemandResponseSchema)
    @blp.response(400, description="Bad request.")
    @blp.response(404, description="User not found.")
    @blp.response(409, description="Conflict.")
    @blp.response(500, description="Internal server error.")
    def post(self, data:dict):
        """
        Create a new demand.
        """
        try:
            user_id = int(get_jwt_identity())
            user:User = User.query.get(user_id)
            if user is None:
                abort(404, message="User not found.")

            data['mountain'] = False
            data['beach'] = False
            data['big_city'] = False
            data['village'] = False

            places:list[str] = data.pop('places')
            for place in places:
                data[place] = True

            demand = Demand(user_id=user_id, **data)

            db.session.add(demand)
            db.session.commit()

            demand_dict = demand.to_dict()
            demand_dict['places'] = places

            demand_dict.pop('mountain')
            demand_dict.pop('beach')
            demand_dict.pop('big_city')
            demand_dict.pop('village')

            return jsonify(demand_dict), 201
        except ValidationError as e:
            abort(400, message=str(e))
        except IntegrityError as e:
            db.session.rollback()
            abort(409, message=str(e.orig))
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal server error.")