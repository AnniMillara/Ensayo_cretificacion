from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.libro import Libros
from flask_app.models.favorito import Favoritos
from flask_app.models.usuario import Usuarios

@app.route("/agregar_favorito/<int:id>")
def agregar_favorito(id):
    if "id_usuario" not in session: # CORRECCIÓN: Se estandarizó la clave de sesión a "id_usuario" para que coincida con el resto de la app.
        return redirect("/")

    usuario_id = session["id_usuario"]
    
    libro = Libros.buscar_id(id)
    if not libro:
        return redirect("/")
    
    data = {
        "libro_id" : libro.id_libro, # CORRECCIÓN: Se cambió el objeto entero por solo el número de ID (`libro.id_libro`).
        "usuario_id" : usuario_id
    }

    flash("Libro agregado correctamente!! ❤︎", "success")
    Favoritos.guardar(data)
    return redirect(url_for("inicio_libros")) # CORRECCIÓN: Se apuntó a una ruta real existente (`inicio_libros`).

@app.route("/eliminar_favorito/<int:id>")
def eliminar_favorito(id):
    if "id_usuario" not in session: # CORRECCIÓN: Se unificó la clave de sesión.
        return redirect("/")

    usuario_id = session["id_usuario"]
    
    libro = Libros.buscar_id(id)
    if not libro:
        return redirect("/")
    
    data = {
        "id" : id # CORRECCIÓN: Se ajustó al identificador correcto que espera el método eliminar de favoritos.
    }

    Favoritos.eliminar(data)
    flash("Libro eliminado de favoritos correctamente!! ❤︎", "success")
    return redirect(url_for("inicio_libros"))