from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.libro import Libros
from flask_app.models.autor import Autores
from flask_app.models.genero import Generos
from flask_app.models.favorito import Favoritos
from flask_app.models.usuario import Usuarios

@app.route("/libros")
def inicio_libros():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    libros = Libros.ver_libros()
    libros_favs = Favoritos.libros_favoritos(session["id_usuario"])
    return render_template(
        'libros.html',
        libros=libros,
        libros_favs=libros_favs
    )

@app.route("/libro/detalle/<int:id>")
def detalle_libro(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Ups, el libro no fue encontrado.", "danger")
        return redirect(url_for('inicio_libros'))
    
    en_favs = Favoritos.favorito_de(id)
    usuario_lo_tiene = Favoritos.buscar_libro_usuario(id, session["id_usuario"])
    
    return render_template(
        'libro_detalle.html',
        libro=libro,
        en_favs=en_favs,
        usuario_lo_tiene=usuario_lo_tiene
    )

@app.route("/libros/nuevo")
def nuevo_libro():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    return render_template(
        'nuevo_libro.html',
        autores=Autores.autores_lista(),
        generos=Generos.generos_lista()
    )

@app.route("/libros/crear", methods=["POST"])
def ingresar_libro():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    usuario = Usuarios.buscar_id(session["id_usuario"])
    if not usuario:
        session.clear()
        flash("Tu sesión ya no es válida. Inicia sesión de nuevo.", "danger")
        return redirect(url_for("inicio"))
    
    datos = {
        "titulo": request.form.get("titulo", "").strip(),
        "autor_id": request.form.get("autor_id", "").strip(),
        "genero_id": request.form.get("genero_id", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "usuario_id": session["id_usuario"]
    }
    
    if not Libros.validar_libro(datos):
        return redirect(url_for('nuevo_libro'))
    
    Libros.guardar(datos)
    flash("Libro guardado correctamente.", "success")
    return redirect(url_for('inicio_libros'))

@app.route("/libros/editar/<int:id>")
def editar_libro(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for('inicio_libros'))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('inicio_libros'))
    
    if libro.usuario_id != session["id_usuario"]:
        flash("No puedes modificar este libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    return render_template(
        'editar_libro.html',
        libro=libro,
        autores=Autores.autores_lista(),
        generos=Generos.generos_lista()
    )

@app.route("/libros/modificar/<int:id>", methods=["POST"])
def modificar_libro(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder modificar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Ups, parece que el libro no existe...", "danger")
        return redirect(url_for('inicio_libros'))
    
    if libro.usuario_id != session["id_usuario"]:
        flash("No puedes modificar este libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    datos = {
        "id_libro": id,
        "titulo": request.form.get("titulo", "").strip(),
        "autor_id": request.form.get("autor_id", "").strip(),
        "genero_id": request.form.get("genero_id", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip()
    }
    
    if not Libros.validar_libro(datos):
        return redirect(url_for('editar_libro', id=id))
    
    Libros.modificar(datos)
    flash("Libro modificado correctamente.", "success")
    return redirect(url_for('inicio_libros'))

@app.route("/libros/confirmar_eliminacion/<int:id>")
def confirmar_eliminacion(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Ups, parece que el libro no existe...", "danger")
        return redirect(url_for('inicio_libros'))
    
    if libro.usuario_id != session["id_usuario"]:
        flash("No puedes eliminar este libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    return render_template(
        "confirmar_eliminar.html",
        mensaje=f"Vas a eliminar el libro '{libro.titulo}' y ya no va a volver...",
        accion=url_for("eliminar_libro", id=libro.id_libro),
        cancelar=url_for("inicio_libros")
    )

@app.route("/libros/eliminar/<int:id>")
def eliminar_libro(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Ups, parece que el libro no existe...", "danger")
        return redirect(url_for('inicio_libros'))
    
    if libro.usuario_id != session["id_usuario"]:
        flash("No puedes eliminar este libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    Libros.eliminar(id)
    flash("Libro eliminado correctamente.", "success")
    return redirect(url_for('inicio_libros'))