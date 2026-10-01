from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Generos:
    def __init__(self, data):
        self.id_genero = data["id_genero"]
        self.nombre = data["nombre"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def generos_lista(cls):
        query = """
            SELECT 
                id_genero,
                nombre,
                created_at,
                updated_at
            FROM generos
            ORDER BY id_genero;
        """
        
        resultados = connectToMySQL('esquema_biblioteca').query_db(query)
        
        generos = []
        for genero in resultados:
            generos.append(cls(genero))
        
        return generos
    
    @classmethod
    def buscar_id(cls, id):
        query = """
            SELECT 
                id_genero,
                nombre,
                created_at,
                updated_at
            FROM generos
            WHERE id_genero = %(id_genero)s;
        """
        
        data = {
            "id_genero" : id
        }
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def buscar_nombre(cls, nombre):
        query = """
            SELECT 
                id_genero,
                nombre,
                created_at,
                updated_at
            FROM generos
            WHERE nombre = %(nombre)s;
        """
        
        data = {
            "nombre" : nombre
        }
        
        resultado = connectToMySQL('esquema_biblioteca').query_db(query, data)
        if resultado:
            return cls(resultado[0])
        return None
    
    @classmethod
    def modificar(cls, data):
        query = """
            UPDATE generos
            SET
                nombre = %(nombre)s,
                updated_at = NOW()
            WHERE id_genero = %(id_genero)s;
        """
        
        return connectToMySQL('esquema_biblioteca').query_db(query, data)
    
    @classmethod
    def eliminar(cls, id):
        query = """
            DELETE FROM generos
            WHERE id_genero = %(id_genero)s;
        """
        
        data = {
            "id_genero": id
        }
        
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO generos(
                nombre,
                created_at,
                updated_at
            ) VALUES (
                %(nombre)s,
                NOW(),
                NOW()
            );
        """
        
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @staticmethod
    def validar_genero(datos):
        es_valido = True

        if not datos["nombre"].strip():
            flash("El nombre del género es obligatorio.", "danger")
            es_valido = False
        elif len(datos["nombre"].strip()) < 2:
            flash("El nombre del género debe tener al menos 2 caracteres.", "danger")
            es_valido = False
        elif Generos.buscar_nombre(datos["nombre"].strip()):
            flash("Este género ya existe.", "danger")
            es_valido = False

        return es_valido