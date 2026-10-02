from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Favoritos:
    def __init__(self, data):
        self.id = data["id"]
        self.libro_id = data["libro_id"]
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def ver_favoritos(cls, usuario_id):
        query = """
            SELECT 
                id,
                libro_id,
                usuario_id,
                created_at,
                updated_at
            FROM favoritos
            WHERE usuario_id = %(usuario_id)s
            ORDER BY id;
        """
        
        data = {
            "usuario_id" : usuario_id
        }
        resultados = connectToMySQL('esquema_biblioteca').query_db(query, data)
        
        favoritos = []
        for favorito in resultados:
            favoritos.append(cls(favorito))
        
        return favoritos
    
    @classmethod
    def libros_favoritos(cls, usuario_id):
        from flask_app.models.libro import Libros
        
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
                autores.nombre AS autor_nombre,
                autores.apellido AS autor_apellido,
                generos.nombre AS genero_nombre,
                usuarios.nombre AS usuario_nombre,
                usuarios.apellido AS usuario_apellido
            FROM favoritos
            JOIN libros ON favoritos.libro_id = libros.id_libro
            JOIN autores ON libros.autor_id = autores.id_autor
            JOIN generos ON libros.genero_id = generos.id_genero
            JOIN usuarios ON libros.usuario_id = usuarios.id_usuario
            WHERE favoritos.usuario_id = %(usuario_id)s
            ORDER BY favoritos.id;
        """
        
        data = {
            "usuario_id": usuario_id
        }
        resultados = connectToMySQL('esquema_biblioteca').query_db(query, data)
        
        libros = []
        for libro in resultados:
            libros.append(Libros(libro))
        
        return libros
    
    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id,
                libro_id,
                usuario_id,
                created_at,
                updated_at
            FROM favoritos
            WHERE id = %(id)s;
        """
        
        data = {
            "id" : id
        }
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def buscar_libro_usuario(cls, libro_id, usuario_id):
        query = """
            SELECT 
                id,
                libro_id,
                usuario_id,
                created_at,
                updated_at
            FROM favoritos
            WHERE libro_id = %(libro_id)s AND usuario_id = %(usuario_id)s;
        """
        
        data = {
            "libro_id" : libro_id,
            "usuario_id" : usuario_id
        }
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def favorito_de(cls, libro_id):
        query = """
            SELECT 
                usuarios.id_usuario,
                usuarios.nombre,
                usuarios.apellido,
                usuarios.email,
                favoritos.created_at AS fecha_favorito
            FROM favoritos
            JOIN usuarios ON favoritos.usuario_id = usuarios.id_usuario
            WHERE favoritos.libro_id = %(libro_id)s
            ORDER BY usuarios.nombre;
        """
        
        data = {
            "libro_id": libro_id
        }
        
        return connectToMySQL('esquema_biblioteca').query_db(query, data)
    
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM favoritos
            WHERE id = %(id)s;
        """
        
        data = {
            "id": id
        }
        
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO favoritos(
                libro_id,
                usuario_id,
                created_at,
                updated_at
            ) VALUES (
                %(libro_id)s,
                %(usuario_id)s,
                NOW(),
                NOW()
            );
        """
        
        return connectToMySQL("esquema_biblioteca").query_db(query, data)