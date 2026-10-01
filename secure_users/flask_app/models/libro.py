from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Libros:
    def __init__(self, data):
        self.id_libro = data["id_libro"]
        self.titulo = data["titulo"]
        self.autor_id = data["autor_id"]
        self.genero_id = data["genero_id"]
        self.descripcion = data["descripcion"]
        # CORRECCIÓN: se agrega usuario_id porque la tabla libros ahora tiene
        # esa columna con FK a usuarios. Sin este atributo no se puede saber
        # quién creó cada libro y no se puede aplicar la regla de "un usuario
        # no puede modificar ni eliminar registros que no le pertenecen".
        self.usuario_id = data["usuario_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def ver_libros(cls):
        # CORRECCIÓN: se agrega usuario_id al SELECT. Si no se selecciona,
        # el __init__ lanza KeyError al intentar leer data["usuario_id"].
        query = """
            SELECT 
                id_libro,
                titulo,
                autor_id,
                genero_id,
                descripcion,
                usuario_id,
                created_at,
                updated_at
            FROM libros
            ORDER BY id_libro;
        """
        
        resultados = connectToMySQL('esquema_biblioteca').query_db(query)
        
        libros = []
        for libro in resultados:
            libros.append(cls(libro))
        
        return libros
    
    @classmethod
    def buscar_id(cls, id):
        # CORRECCIÓN: usuario_id agregado al SELECT por la misma razón
        # que en ver_libros. Se usa en el controlador para comparar con
        # session["id_usuario"] antes de permitir editar o eliminar.
        query = """
            SELECT 
                id_libro,
                titulo,
                autor_id,
                genero_id,
                descripcion,
                usuario_id,
                created_at,
                updated_at
            FROM libros
            WHERE id_libro = %(id_libro)s;
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
        # usuario_id NO se actualiza en modificar porque el dueño del libro
        # no cambia: el libro sigue perteneciendo al mismo usuario que lo creó.
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
    
        # CORRECCIÓN: se arregla la indentación del diccionario.
        # Estaba mal alineado y aunque Python lo acepta, rompe la
        # consistencia visual del resto del archivo.
        data = {
            "id_libro" : id
        }
        return connectToMySQL("esquema_biblioteca").query_db(query, data)
    
    @classmethod
    def guardar(cls, data):
        # CORRECCIÓN: se agrega usuario_id al INSERT para que cada libro
        # quede asociado al usuario que lo creó. El valor viene del
        # controlador usando session["id_usuario"].
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
        # CORRECCIÓN: usuario_id agregado al SELECT para que __init__ no falle.
        query = """
            SELECT 
                id_libro,
                titulo,
                autor_id,
                genero_id,
                descripcion,
                usuario_id,
                created_at,
                updated_at
            FROM libros
            WHERE autor_id = %(autor_id)s;
        """
        data = {
            "autor_id": autor
        }
        
        libros = []
        resultados = connectToMySQL('esquema_biblioteca').query_db(query, data)
        for libro in resultados:
            libros.append(cls(libro))
        
        # CORRECCIÓN CRÍTICA: antes retornaba None aunque hubiera resultados.
        # El error estaba en que se llenaba la lista pero se devolvía None
        # al final, por lo que el controlador siempre recibía None.
        # Ahora retorna la lista completa de libros, vacía si no hay resultados.
        return libros

    @classmethod
    def buscar_genero(cls, genero):
        # CORRECCIÓN: usuario_id agregado al SELECT por la misma razón
        # que en los otros métodos de búsqueda.
        query = """
            SELECT 
                id_libro,
                titulo,
                autor_id,
                genero_id,
                descripcion,
                usuario_id,
                created_at,
                updated_at
            FROM libros
            WHERE genero_id = %(genero_id)s;
        """
        data = {
            "genero_id": genero
        }
        
        libros = []
        resultados = connectToMySQL('esquema_biblioteca').query_db(query, data)
        for libro in resultados:
            libros.append(cls(libro))
        
        return libros