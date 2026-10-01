from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.libro import Libros
from flask_app.models.genero import Generos

@app.route("/generos")
def generos():
    generos = Generos.generos_lista()
    return render_template(
        'autores.html',
        generos=generos
    )

@app.route("/generos/eliminar/<int:id>")
def eliminar_genero(id):
    puede = Libros.buscar_genero(id)
    
    if puede:
        Generos.eliminar(id)
        flash("Genero eliminado correctamente!!", "success")
        return redirect(url_for('generos'))
    
    flash("Ups, parece que algo salio mal", "danger")
    return redirect(url_for('generos'))

@app.route("/generos/ingresar", methods=["POST"])
def nuevo_genero():
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el/la nuevo genero.", "danger")
        return redirect(url_for('generos'))
    
    nombre = request.form.get("nombre", " ").strip()
    
    datos = {
        "nombre" : nombre
    }
    
    puede = Generos.validar_genero(datos)
    if not puede:
        return url_for('autores')
    
    repite = Generos.buscar_nombre(nombre)
    if repite:
        flash("Ese genero ya fue ingresado!!!", "danger")
        return url_for('autores')
    
    Generos.guardar(datos) # CORRECCIÓN: Se le pasa 'datos' (diccionario) en lugar de 'nombre' (string) porque la función guardar espera un diccionario.
    flash("Genero guardado correctamente!!")
    return url_for('autores')

@app.route("/Genero/modificar/<int:id>")
def modificar_genero(id):
    if "id_usuario" not in session:
        flash("Inicia sesión para poder ingresar el/la autor/a.", "danger")
        return redirect(url_for('autores'))
        
    nombre = request.form.get("nombre", " ").strip()
        
    datos = {
        "id_genero" : id, # CORRECCIÓN: Se agregó el id del género para que la base de datos sepa exactamente qué registro actualizar.
        "nombre" : nombre
    }
    
    puede = Generos.validar_genero(datos)
    if not puede:
        return url_for('autores')
    
    Generos.modificar(datos) # CORRECCIÓN: Se cambió de 'id' a 'datos' para que el método de actualización reciba la información correcta.
    flash("Genero modificado correctamente!!")
    return url_for('autores')