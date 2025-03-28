from flask_marshmallow import Marshmallow
from api.models import TopcvDataJob, ItviecDataJob
from api.app import ma

class TopcvDataJobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TopcvDataJob
        include_relationships = False
        load_instance = True

class ItviecDataJobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItviecDataJob
        include_relationships = False
        load_instance = True

topcv_job_schema = TopcvDataJobSchema()
itviec_job_schema = ItviecDataJobSchema()