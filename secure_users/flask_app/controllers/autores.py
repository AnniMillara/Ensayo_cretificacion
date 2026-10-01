from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.libro import Libros
from flask_app.models.autor import Autores

@app.route("/autores")
def autores():
    autores = Autores.autores_lista() # CORRECCIÓN: Se agregaron los paréntesis para ejecutar el método de la clase.
    return render_template(
        'autores.html',
        autores=autores
    )

@app.route("/autores/detalle/<int:id>")
def detalle_autor(id):
    autor = Autores.buscar_id(id)
    libros_suyos = Libros.buscar_autor(id)
    
    return render_template(
            'autor_detalle.html',
            autor=autor,
            libros_suyos=libros_suyos
        )

@app.route("/autores/eliminar/<int:id>")
def eliminar_autor(id):
    puede = Libros.buscar_autor(id)
    
    if puede:
        Autores.eliminar(id)
        flash("Autor eliminado correctamente!!", "success")
        return redirect(url_for('autores'))
    
    flash("Ups, parece que algo salio mal", "danger")
    return redirect(url_for('autores'))

@app.route("/autores/ingresar", methods=["POST"])
def nuevo_autor():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el/la autor/a.", "danger")
        return redirect(url_for('autores'))
    
    nombre = request.form.get("nombre", " ").strip()
    apellido = request.form.get("apellido", " ").strip()
    
    datos = {
        "nombre" : nombre,
        "apellido" : apellido
    }
    
    puede = Autores.validar_autor(datos) # CORRECCIÓN: Se agregaron los paréntesis a la validación.
    if not puede:
        return url_for('autores')
    
    repite = Autores.buscar_nombre_completo(nombre, apellido)
    if repite:
        flash("Ese autor ya fue ingresado!!!", "danger")
        return url_for('autores')
    
    Autores.guardar(datos)
    flash("Autor guardado correctamente!!")
    return url_for('autores')

@app.route("/autores/modificar/<int:id>")
def modificar_autor(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el/la autor/a.", "danger")
        return redirect(url_for('autores'))
        
    nombre = request.form.get("nombre", " ").strip()
    apellido = request.form.get("apellido", " ").strip()
        
    datos = {
        "id_autor" : id, # CORRECCIÓN: Se añadió el id del autor para que sepa a qué registro aplicar el cambio.
        "nombre" : nombre,
        "apellido" : apellido
    }
    
    puede = Autores.validar_autor(datos)
    if not puede:
        return url_for('autores')
    
    Autores.modificar(datos)
    flash("Autor modificado correctamente!!")
    return url_for('autores')