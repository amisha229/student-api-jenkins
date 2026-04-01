```python
from flask import Flask
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields
from flask_sqlalchemy import SQLAlchemy

# ----------------------
# App configuration
# ----------------------
app = Flask(__name__)

app.config["API_TITLE"] = "Student API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Database config (SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)

# ----------------------
# Database Model
# ----------------------
class StudentModel(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)

# ----------------------
# Schema
# ----------------------
class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    dept = fields.Str(required=True)

# ----------------------
# Blueprint
# ----------------------
blp = Blueprint("students", __name__, description="Student CRUD operations")

# ----------------------
# Routes
# ----------------------
@blp.route("/students")
class StudentList(MethodView):

    @blp.response(200, StudentSchema(many=True))
    def get(self):
        return StudentModel.query.all()

    @blp.arguments(StudentSchema)
    @blp.response(201, StudentSchema)
    def post(self, student_data):
        student = StudentModel(**student_data)
        db.session.add(student)
        db.session.commit()
        return student


@blp.route("/students/<int:student_id>")
class Student(MethodView):

    @blp.response(200, StudentSchema)
    def get(self, student_id):
        student = StudentModel.query.get(student_id)
        if student:
            return student
        return {"message": "Student not found"}, 404

    @blp.arguments(StudentSchema)
    @blp.response(200, StudentSchema)
    def put(self, student_data, student_id):
        student = StudentModel.query.get(student_id)
        if student:
            student.name = student_data["name"]
            student.dept = student_data["dept"]
            db.session.commit()
            return student
        return {"message": "Student not found"}, 404

    def delete(self, student_id):
        student = StudentModel.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return {"message": "Deleted successfully"}, 200
        return {"message": "Student not found"}, 404


# ----------------------
# Register Blueprint
# ----------------------
api.register_blueprint(blp)

# ----------------------
# Create Tables
# ----------------------
with app.app_context():
    db.create_all()

# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    app.run()
```
