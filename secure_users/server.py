from flask_app import app
from flask_app.controllers import autores, favoritos, generos, libros, usuarios

if __name__ == "__main__":
    app.run(debug=True)