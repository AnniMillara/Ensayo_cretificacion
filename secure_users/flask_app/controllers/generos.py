from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.libro import Libros
from flask_app.models.genero import Generos

@app.route("/generos")
def generos():
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    generos = Generos.generos_lista()
    return render_template(
        'generos.html',
        generos=generos
    )

@app.route("/generos/eliminar/<int:id>")
def eliminar_genero(id):
    if "id_usuario" not in session:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("inicio"))
    
    libros_asociados = Libros.buscar_genero(id)
    
    if libros_asociados:
        flash("No puedes eliminar un género que tiene libros asociados.", "danger")
        return redirect(url_for('generos'))
    
    Generos.eliminar(id)
    flash("Género eliminado correctamente.", "success")
    return redirect(url_for('generos'))

@app.route("/generos/ingresar", methods=["POST"])
def nuevo_genero():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el género.", "danger")
        return redirect(url_for('generos'))
    
    nombre = request.form.get("nombre", "").strip()
    
    datos = {
        "nombre": nombre
    }
    
    if not Generos.validar_genero(datos):
        return redirect(url_for('generos'))
    
    repite = Generos.buscar_nombre(nombre)
    if repite:
        flash("Ese género ya fue ingresado.", "danger")
        return redirect(url_for('generos'))
    
    Generos.guardar(datos)
    flash("Género guardado correctamente.", "success")
    return redirect(url_for('generos'))

@app.route("/generos/modificar/<int:id>", methods=["POST"])
def modificar_genero(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder modificar el género.", "danger")
        return redirect(url_for('generos'))
    
    genero = Generos.buscar_id(id)
    if not genero:
        flash("Género no encontrado.", "danger")
        return redirect(url_for('generos'))
    
    nombre = request.form.get("nombre", "").strip()
    
    datos = {
        "id_genero": id,
        "nombre": nombre
    }
    
    if not Generos.validar_genero(datos):
        return redirect(url_for('generos'))
    
    Generos.modificar(datos)
    flash("Género modificado correctamente.", "success")
    return redirect(url_for('generos'))