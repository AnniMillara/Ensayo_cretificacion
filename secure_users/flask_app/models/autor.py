from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Autores:
    def __init__(self, data):
        self.id_autor = data["id_autor"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def autores_lista(cls):
        query = """
            SELECT 
                id_autor,
                nombre,
                apellido,
                created_at,
                updated_at
            FROM autores
            ORDER BY id_autor;
        """
        
        resultados = connectToMySQL('esquema_biblioteca').query_db(query)
        
        autores = []
        for autor in resultados:
            autores.append(cls(autor))
        
        return autores
    
    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_autor,
                nombre,
                apellido,
                created_at,
                updated_at
            FROM autores
            WHERE id_autor = %(id_autor)s;
        """
        
        data = {
            "id_autor" : id
        }
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE autores
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                updated_at = NOW()
            WHERE id_autor = %(id_autor)s;
        """
        
        return connectToMySQL('esquema_biblioteca').query_db(query, data)
    
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM autores
            WHERE id_autor = %(id_autor)s;
        """
    
        data = {
            "id_autor": id
        }
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO autores(
                nombre,
                apellido,
                created_at,
                updated_at
            ) VALUES (
                %(nombre)s,
                %(apellido)s,
                NOW(),
                NOW()
            );
        """
        
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def buscar_nombre_completo(cls, nombre, apellido):
        query = """
            SELECT id_autor, nombre, apellido, created_at, updated_at
            FROM autores
            WHERE nombre = %(nombre)s AND apellido = %(apellido)s;
        """
        data = {
            "nombre": nombre,
            "apellido": apellido
        }
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None

    @staticmethod
    def validar_autor(datos):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre es obligatorio.", "danger")
            es_valido = False
        elif len(datos["nombre"].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "danger")
            es_valido = False

        if not datos["apellido"].strip():
            flash("El apellido es obligatorio.", "danger")
            es_valido = False
        elif len(datos["apellido"].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "danger")
            es_valido = False

        return es_valido