from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.services.dashboard_servies import get_dashboard_payload
from app.utils.helpers import success_response


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("", methods=["GET"])
@jwt_required()
def get_dashboard():

    return success_response(
        get_dashboard_payload()
    )