from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.libro import Libros
from flask_app.models.favorito import Favoritos

@app.route("/libros")
def inicio_libros():
    libros = Libros.ver_libros()
    return render_template(
            'libros.html',
            libros=libros
        )

@app.route("/libros/<int:id>")
def libros(id):
    mis_libros = Favoritos.ver_favoritos(id)
    libros = Libros.ver_libros()
    return render_template(
        'libros.html',
        mis_libros=mis_libros,
        libros=libros
    )

@app.route("/libro/detalle/<int:id>")
def detalle_libro(id):
    libro = Libros.buscar_id(id)
    en_favs = Favoritos.favorito_de(id)
    
    if libro:
        return render_template(
            'libro_detalle.html',
            libro=libro,
            en_favs=en_favs
        )
    
    flash("Ups, el libro no fue encontrado ᴖ̈", "danger")
    return redirect(url_for('inicio_libros'))

@app.route("/libros/crear", metodhs=["POST"])
def ingresar_libro():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    titulo = request.form.get("titulo", " ").strip
    autor_id = request.form.get("autor_id", " ").strip
    genero = request.form.get("genero", " ").strip
    descripcion = request.form.get("descripcion", " ").strip
    
    datos = {
        "titulo" : titulo,
        "autor_id" : autor_id,
        "genero" : genero,
        "descripcion" : descripcion
    }
    
    libro_nuevo = Libros.validar_libro(datos)
    if not libro_nuevo:
        return redirect(url_for('inicio_libros'))
    
    Libros.guardar(datos)
    flash("Libro guardado correctamente", "success")
    return redirect(url_for('inicio_libros'))

@app.route("/libros/modificar/<int:id>", methods=["POST"])
def modificar_libro(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    titulo = request.form.get("titulo", " ").strip
    autor_id = request.form.get("autor_id", " ").strip
    genero = request.form.get("genero", " ").strip
    descripcion = request.form.get("descripcion", " ").strip
        
    datos = {
        "titulo" : titulo,
        "autor_id" : autor_id,
        "genero" : genero,
        "descripcion" : descripcion
    }
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Ups, parece que el libro no existe...", "danger")
        return redirect(url_for('inicio_libros'))

    # Corregido: misma validación de pertenencia que en la confirmación.
    # No basta con confiar en que el usuario llegó desde la pantalla previa.
    if libro.usuario_id != session["id_usuario"]:
        flash("No puedes eliminar este libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    libro_modificado = Libros.validar_libro(datos)
    if not libro_modificado:
        return redirect(url_for('inicio_libros'))
    
    Libros.modificar(datos)
    flash("Libro modificado correctamente!!", "success")
    return redirect(url_for('inicio_libros'))

@app.route("/libro/confirmar_eliminacion/<int:id>")
def confirmar_eliminacion(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder eliminar el libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    libro = Libros.buscar_id(id)
    if not libro:
        flash("Ups, parece que el libro no existe...", "danger")
        return redirect(url_for('inicio_libros'))
    
    # Corregido: faltaba validar que el libro pertenezca al usuario en sesión.
    # Sin esto, cualquiera podría borrar libros ajenos escribiendo la URL.
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
    
    # Corregido: misma validación de pertenencia que en la confirmación.
    # No basta con confiar en que el usuario llegó desde la pantalla previa.
    if libro.usuario_id != session["id_usuario"]:
        flash("No puedes eliminar este libro.", "danger")
        return redirect(url_for('inicio_libros'))
    
    Libros.eliminar(id)
    flash("Libro eliminado correctamente!!", "success")
    return redirect(url_for('inicio_libros'))