from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Libros:
    def __init__(self, data):
        self.id_libro = data["id_libro"]
        self.titulo = data["titulo"]
        self.autor_id = data["autor_id"]
        self.genero_id = data["genero_id"]
        self.descripcion = data["descripcion"]
        self.usuario_id = data["usuario_id"]
        # Estos dos vienen del JOIN con usuarios. Pueden venir None si el
        # SELECT no los trae, por eso el .get().
        self.usuario_nombre = data.get("usuario_nombre")
        self.usuario_apellido = data.get("usuario_apellido")
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def ver_libros(cls):
        query = """
            SELECT 
                libros.id_libro,
                libros.titulo,
                libros.autor_id,
                libros.genero_id,
                libros.descripcion,
                libros.usuario_id,
                libros.created_at,
                libros.updated_at,
                usuarios.nombre AS usuario_nombre,
                usuarios.apellido AS usuario_apellido
            FROM libros
            JOIN usuarios ON libros.usuario_id = usuarios.id_usuario
            ORDER BY libros.id_libro;
        """
        
        resultados = connectToMySQL('esquema_biblioteca').query_db(query)
        
        libros = []
        for libro in resultados:
            libros.append(cls(libro))
        
        return libros
    
    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                libros.id_libro,
                libros.titulo,
                libros.autor_id,
                libros.genero_id,
                libros.descripcion,
                libros.usuario_id,
                libros.created_at,
                libros.updated_at,
                usuarios.nombre AS usuario_nombre,
                usuarios.apellido AS usuario_apellido
            FROM libros
            JOIN usuarios ON libros.usuario_id = usuarios.id_usuario
            WHERE libros.id_libro = %(id_libro)s;
        """
        
        data = {
            "id_libro" : id
        }
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE libros
            SET
                titulo = %(titulo)s,
                autor_id = %(autor_id)s,
                genero_id = %(genero_id)s,
                descripcion = %(descripcion)s,
                updated_at = NOW()
            WHERE id_libro = %(id_libro)s;
        """
        
        return connectToMySQL('esquema_biblioteca').query_db(query, data)
    
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM libros
            WHERE id_libro = %(id_libro)s;
        """
        data = {
            "id_libro" : id
        }
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO libros(
                titulo,
                autor_id,
                genero_id,
                descripcion,
                usuario_id,
                created_at,
                updated_at
            ) VALUES (
                %(titulo)s,
                %(autor_id)s,
                %(genero_id)s,
                %(descripcion)s,
                %(usuario_id)s,
                NOW(),
                NOW()
            );
        """
        
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def buscar_autor(cls, autor):
        query = """
            SELECT 
                libros.id_libro,
                libros.titulo,
                libros.autor_id,
                libros.genero_id,
                libros.descripcion,
                libros.usuario_id,
                libros.created_at,
                libros.updated_at,
                usuarios.nombre AS usuario_nombre,
                usuarios.apellido AS usuario_apellido
            FROM libros
            JOIN usuarios ON libros.usuario_id = usuarios.id_usuario
            WHERE libros.autor_id = %(autor_id)s;
        """
        data = {
            "autor_id": autor
        }
        
        libros = []
        resultados = connectToMySQL('esquema_biblioteca').query_db(query, data)
        for libro in resultados:
            libros.append(cls(libro))
        
        return libros

    @classmethod
    def buscar_genero(cls, genero):
        query = """
            SELECT 
                libros.id_libro,
                libros.titulo,
                libros.autor_id,
                libros.genero_id,
                libros.descripcion,
                libros.usuario_id,
                libros.created_at,
                libros.updated_at,
                usuarios.nombre AS usuario_nombre,
                usuarios.apellido AS usuario_apellido
            FROM libros
            JOIN usuarios ON libros.usuario_id = usuarios.id_usuario
            WHERE libros.genero_id = %(genero_id)s;
        """
        data = {
            "genero_id": genero
        }
        
        libros = []
        resultados = connectToMySQL('esquema_biblioteca').query_db(query, data)
        for libro in resultados:
            libros.append(cls(libro))
        
        return libros
    
    @staticmethod
    def validar_libro(datos):
        es_valido = True

        if not datos["titulo"].strip():
            flash("El título es obligatorio.", "danger")
            es_valido = False
        elif len(datos["titulo"].strip()) < 2:
            flash("El título debe tener al menos 2 caracteres.", "danger")
            es_valido = False

        if not datos["descripcion"].strip():
            flash("La descripción es obligatoria.", "danger")
            es_valido = False
        elif len(datos["descripcion"].strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "danger")
            es_valido = False

        if not datos["autor_id"]:
            flash("Debes seleccionar un autor.", "danger")
            es_valido = False

        if not datos["genero_id"]:
            flash("Debes seleccionar un género.", "danger")
            es_valido = False

        return es_valido