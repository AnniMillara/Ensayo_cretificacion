from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.libro import Libros
from flask_app.models.favorito import Favoritos
from flask_app.models.usuario import Usuarios

@app.route("/agregar_favorito/<int:id>")
def agregar_favorito(id):
    if "usuario_id" not in session:
        return redirect("/")

    usuario_id = session["usuario_id"]
    
    libro = Libros.buscar_id(id)
    if not libro:
        return redirect("/")
    
    data = {
        "libro_id" : libro,
        "usuario_id" : usuario_id
    }

    flash("Libro agregado correctamente!! ❤︎", "success")
    Favoritos.guardar(data)
    return redirect(url_for("mostrar_libros"))

@app.route("/eliminar_favorito/<int:id>")
def eliminar_favorito(id):
    if "usuario_id" not in session:
        return redirect("/")

    usuario_id = session["usuario_id"]
    
    libro = Libros.buscar_id(id)
    if not libro:
        return redirect("/")
    
    
    data = {
        "libro_id" : libro,
        "usuario_id" : usuario_id
    }

    Favoritos.eliminar(data)
    flash("Libro agregado correctamente!! ❤︎", "success")
    return redirect(url_for("mostrar_libros"))