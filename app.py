from flask import Flask
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields

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

api = Api(app)

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
blp = Blueprint(
    "students",
    __name__,
    description="Student CRUD operations"
)

# In-memory data (for learning)
students = []

# ----------------------
# Routes (CRUD)
# ----------------------
@blp.route("/students")
class StudentList(MethodView):

    @blp.response(200, StudentSchema(many=True))
    def get(self):
        """Get all students"""
        return students

    @blp.arguments(StudentSchema)
    @blp.response(201, StudentSchema)
    def post(self, student_data):
        """Create a new student"""
        student_data["id"] = len(students) + 1
        students.append(student_data)
        return student_data


@blp.route("/students/<int:student_id>")
class Student(MethodView):

    @blp.response(200, StudentSchema)
    def get(self, student_id):
        """Get one student"""
        for s in students:
            if s["id"] == student_id:
                return s
        return {"message": "Student not found"}, 404

    @blp.arguments(StudentSchema)
    @blp.response(200, StudentSchema)
    def put(self, student_data, student_id):
        """Update student"""
        for s in students:
            if s["id"] == student_id:
                s.update(student_data)
                return s
        return {"message": "Student not found"}, 404

    def delete(self, student_id):
        """Delete student"""
        global students
        students = [s for s in students if s["id"] != student_id]
        return {"message": "Deleted successfully"}, 200


# ----------------------
# Register Blueprint
# ----------------------
api.register_blueprint(blp)

# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)