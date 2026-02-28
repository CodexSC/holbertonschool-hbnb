from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place management operations")

place_input_model = api.model(
    "PlaceInput",
    {
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "price_per_night": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "owner_id": fields.String(required=True),
        "max_guests": fields.Integer(required=False),
        "amenity_ids": fields.List(fields.String, required=False),
    },
)

place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(required=False),
        "description": fields.String(required=False),
        "price_per_night": fields.Float(required=False),
        "latitude": fields.Float(required=False),
        "longitude": fields.Float(required=False),
        "max_guests": fields.Integer(required=False),
        "amenity_ids": fields.List(fields.String, required=False),
    },
)


@api.route("/")
class PlaceList(Resource):
    def get(self):
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @api.expect(place_input_model)
    @api.response(201, "Place created")
    @api.response(400, "Bad request")
    def post(self):
        data = api.payload or {}
        try:
            place = facade.create_place(data)
        except ValueError as exc:
            api.abort(400, str(exc))
        return place.to_dict(), 201


@api.route("/<string:place_id>")
@api.param("place_id", "Place identifier")
class PlaceResource(Resource):
    @api.response(404, "Place not found")
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict(), 200

    @api.expect(place_update_model)
    @api.response(200, "Place updated")
    @api.response(404, "Place not found")
    @api.response(400, "Bad request")
    def put(self, place_id):
        data = api.payload or {}
        try:
            place = facade.update_place(place_id, data)
        except ValueError as exc:
            api.abort(400, str(exc))
        if not place:
            api.abort(404, "Place not found")
        return place.to_dict(), 200
