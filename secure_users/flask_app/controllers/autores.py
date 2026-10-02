from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.libro import Libros
from flask_app.models.autor import Autores

@app.route("/autores")
def autores():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    autores = Autores.autores_lista()
    return render_template(
        'autores.html',
        autores=autores
    )

@app.route("/autores/detalle/<int:id>")
def detalle_autor(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    autor = Autores.buscar_id(id)
    if not autor:
        flash("Autor no encontrado.", "danger")
        return redirect(url_for('autores'))
    
    libros_suyos = Libros.buscar_autor(id)
    
    return render_template(
        'autor_detalle.html',
        autor=autor,
        libros_suyos=libros_suyos
    )

@app.route("/autores/eliminar/<int:id>")
def eliminar_autor(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    libros_asociados = Libros.buscar_autor(id)
    
    if libros_asociados:
        flash("No puedes eliminar un autor que tiene libros asociados.", "danger")
        return redirect(url_for('autores'))
    
    Autores.eliminar(id)
    flash("Autor eliminado correctamente.", "success")
    return redirect(url_for('autores'))

@app.route("/autores/ingresar", methods=["POST"])
def nuevo_autor():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el autor.", "danger")
        return redirect(url_for('autores'))
    
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    
    datos = {
        "nombre": nombre,
        "apellido": apellido
    }
    
    if not Autores.validar_autor(datos):
        return redirect(url_for('autores'))
    
    repite = Autores.buscar_nombre_completo(nombre, apellido)
    if repite:
        flash("Ese autor ya fue ingresado.", "danger")
        return redirect(url_for('autores'))
    
    Autores.guardar(datos)
    flash("Autor guardado correctamente.", "success")
    return redirect(url_for('autores'))

@app.route("/autores/modificar/<int:id>", methods=["POST"])
def modificar_autor(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder modificar el autor.", "danger")
        return redirect(url_for('autores'))
    
    autor = Autores.buscar_id(id)
    if not autor:
        flash("Autor no encontrado.", "danger")
        return redirect(url_for('autores'))
    
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    
    datos = {
        "id_autor": id,
        "nombre": nombre,
        "apellido": apellido
    }
    
    if not Autores.validar_autor(datos):
        return redirect(url_for('autores'))
    
    Autores.modificar(datos)
    flash("Autor modificado correctamente.", "success")
    return redirect(url_for('autores'))