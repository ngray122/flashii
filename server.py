from flask_app import app
from flask_material import Material
# import controllers
from flask_app.controllers import users
from flask_app.controllers import cards


Material(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)