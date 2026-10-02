from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.libro import Libros
from flask_app.models.favorito import Favoritos

@app.route("/favoritos")
def mis_favoritos():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    libros_favs = Favoritos.libros_favoritos(session["id_usuario"])
    return render_template(
        'favoritos.html',
        libros_favs=libros_favs
    )

@app.route("/agregar_favorito/<int:id>")
def agregar_favorito(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for("inicio_libros"))
    
    ya_existe = Favoritos.buscar_libro_usuario(id, session["id_usuario"])
    if ya_existe:
        flash("Ya tienes este libro en favoritos.", "danger")
        return redirect(url_for("detalle_libro", id=id))
    
    data = {
        "libro_id": libro.id_libro,
        "usuario_id": session["id_usuario"]
    }
    Favoritos.guardar(data)
    flash("Libro agregado a favoritos.", "success")
    return redirect(url_for("detalle_libro", id=id))

@app.route("/eliminar_favorito/<int:libro_id>")
def eliminar_favorito(libro_id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    favorito = Favoritos.buscar_libro_usuario(libro_id, session["id_usuario"])
    if not favorito:
        flash("Ese libro no está en tus favoritos.", "danger")
        return redirect(url_for("mis_favoritos"))
    
    Favoritos.eliminar(favorito.id)
    flash("Libro eliminado de favoritos.", "success")
    return redirect(url_for("mis_favoritos"))