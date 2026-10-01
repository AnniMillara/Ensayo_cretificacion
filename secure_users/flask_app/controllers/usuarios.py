from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuarios
from flask_app.models.favorito import Favoritos

# Inicion con registro / login
@app.route("/")
def inicio():
    return redirect(url_for('login.html'))

# Registro de nuevo usuario
@app.route("/registro", methods=["POST"])
def registro():
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "").strip()
    confirmar_contrasena = request.form.get("confirmar_contrasena", "").strip()

    datos = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasena": contrasena,
        "confirmar_contrasena": confirmar_contrasena
    }

    if not Usuarios.validar_usuario(datos):
        return redirect(url_for("inicio"))

    hash_contrasena = bcrypt.generate_password_hash(contrasena).decode("utf-8")

    data = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasena": hash_contrasena
    }

    nuevo_id = Usuarios.guardar(data)
    session["id_usuario"] = nuevo_id

    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("perfil"))

# Ingresar
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "").strip()

    if not email or not contrasena:
        flash("Email y contraseña son obligatorios.", "danger")
        return redirect(url_for("inicio"))

    usuario = Usuarios.buscar_email(email)

    if not usuario:
        flash("Email o contraseña incorrectos.", "danger")
        return redirect(url_for("inicio"))

    if not bcrypt.check_password_hash(usuario.contrasena, contrasena):
        flash("Email o contraseña incorrectos.", "danger")
        return redirect(url_for("inicio"))

    session["id_usuario"] = usuario.id_usuario
    flash("Bienvenido de vuelta!!", "success")
    return redirect(url_for("perfil"))

# Ruta perfil de usuario
@app.route("/perfil/<int:id>")
def ruta_perfil(id):
    usuario = Usuarios.buscar_id(id)
    favs = Favoritos.ver_favoritos(id)
    
    return render_template(
        "perfil.html",
        usuario=usuario,
        favoritos=favs
    )

# Ruta que muestra la página de confirmación antes de borrar la cuenta.
@app.route("/perfil/confirmar_eliminar/<int:id>")
def confirmar_eliminar(id):
    # Verifica que haya sesión activa y que el id de la URL sea el mismo
    # del usuario logueado.
    if "id_usuario" not in session or session["id_usuario"] != id:
        flash("No puedes eliminar este perfil.", "danger")
        return redirect(url_for("inicio"))
    
    # Trae los datos del usuario para mostrarlos en la vista
    usuario = Usuarios.buscar_id(id)
    if not usuario:
        # Si el id no existe en la BD, no tiene sentido seguir.
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("inicio"))
    
    # Muestra la plantilla con los botones "Sí, eliminar" y "Cancelar".
    # El borrado real recién ocurre si el usuario hace clic en el primero.
    return render_template(
        "confirmar_eliminar.html",
        mensaje=f"Vas a eliminar tu perfil, {usuario.nombre}. Esta acción no se puede deshacer.",
        accion=url_for("eliminar_usuario", id=usuario.id_usuario),
        cancelar=url_for("perfil")
    )

# Ruta que ejecuta el borrado real.
@app.route("/perfil/eliminar/<int:id>")
def eliminar_usuario(id):
    # Misma validación de seguridad.
    if "id_usuario" not in session or session["id_usuario"] != id:
        flash("No puedes eliminar este perfil.", "danger")
        return redirect(url_for("inicio"))
    
    # Borra el registro de la base de datos.
    Usuarios.eliminar(id)
    # Limpia la sesión para que el usuario quede desconectado.
    session.clear()
    flash("Perfil eliminado correctamente.", "success")
    return redirect(url_for("inicio"))
