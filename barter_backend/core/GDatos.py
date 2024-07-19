from typing import List
import psycopg2
import os
from bcapital.settings.base import *

class GDatos:
    def CrearConexion():
        return psycopg2.connect(
            database=DB_NAME_DEV,
            user=DB_USER_DEV,
            password=DB_PASSWORD_DEV,
            host=DB_HOST_DEV,
            port=DB_PORT)

    @staticmethod
    def InserObject(Object):
        StringQuery = GDatos.CreateInsertQuery(Object)
        # Crear un cursor para ejecutar la consulta
        conexion = GDatos.CrearConexion()
        cursor = conexion.cursor()
        try:
            # Ejecutar la consulta INSERT
            cursor.execute(StringQuery + " RETURNING id")
            # Recuperar el identificador autoincremental recién creado
            # cursor.execute("SELECT LAST_INSERT_ID()")
            # Obtener el resultado
            id_insertado = cursor.fetchone()[0]
            # Imprimir el identificador autoincremental
            print(
                f"Identificador autoincremental recién creado: {id_insertado}")
            # Hacer commit para guardar los cambios en la base de datos
            conexion.commit()
            return
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

    @staticmethod
    def UpdateObject(Object):
        StringQuery = GDatos.CreateUpdateQuery(Object)
        # Crear un cursor para ejecutar la consulta
        conexion = GDatos.CrearConexion()
        cursor = conexion.cursor()
        try:
            # Ejecutar la consulta Updtae
            cursor.execute(StringQuery)
            # Hacer commit para guardar los cambios en la base de datos
            conexion.commit()
            return
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

    @staticmethod
    def GetListData(entity, filterData: List):
        StringQuery = GDatos.CreateSelectQuery(entity, filterData)
        conexion = GDatos.CrearConexion()
        cursor = conexion.cursor()
        try:
            # Ejecutar la consulta SELECT
            cursor.execute(StringQuery)
            # Obtener los resultados
            resultados = cursor.fetchall()
            # Crear una lista de objetos del tipo especificado
            return resultados
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

    @staticmethod
    def CreateInsertQuery(entity):
        # Obtener las propiedades y valores no nulos del entity
        propiedades = [propiedad for propiedad in dir(entity) if not callable(
            getattr(entity, propiedad)) 
            and not propiedad.startswith("__")
            and propiedad != "filterData"]
        valores = [getattr(entity, propiedad) for propiedad in propiedades]

        # Filtrar las propiedades y valores para excluir los nulos
        propiedades_no_nulas = []
        valores_no_nulos = []
        for propiedad, valor in zip(propiedades, valores):
            if valor is not None:
                propiedades_no_nulas.append(propiedad)
                # Convertir los valores a cadenas, rodeando con comillas solo si no son numéricos
                valor_formateado = f"'{valor}'" if not isinstance(
                    valor, (int, float)) else str(valor)
                valores_no_nulos.append(valor_formateado)

        # Generar la consulta INSERT dinámicamente
        consulta = f"INSERT INTO {type(entity).__name__} ({', '.join(propiedades_no_nulas)}) VALUES ({', '.join(valores_no_nulos)})"
        return consulta

    @staticmethod
    def CreateUpdateQuery(entity):
        # Obtener las propiedades y valores no nulos del entity
        propiedades = [propiedad for propiedad in dir(entity) if not callable(getattr(
            entity, propiedad)) and 
            not propiedad.startswith("__") 
            and propiedad != 'id'
            and propiedad != "filterData"]
        valores = [getattr(entity, propiedad) for propiedad in propiedades]

        # Filtrar las propiedades y valores para excluir los nulos
        propiedades_no_nulas = []
        valores_no_nulos = []
        for propiedad, valor in zip(propiedades, valores):
            if valor is not None:
                propiedades_no_nulas.append(propiedad)
                # Convertir los valores a cadenas, rodeando con comillas solo si no son numéricos
                valor_formateado = f'"{valor}"' if not isinstance(
                    valor, (int, float)) else str(valor)
                valores_no_nulos.append(f"{propiedad} = {valor_formateado}")

        # Construir la cláusula SET para la actualización
        set_clause = ', '.join(valores_no_nulos)

        # Construir la cláusula WHERE para la condición de actualización basada en el ID
        where_clause = f"WHERE id = {entity.id}"

        # Generar la consulta UPDATE dinámicamente
        consulta = f"UPDATE {type(entity).__name__} SET {set_clause} {where_clause}"

        return consulta

    @staticmethod
    def CreateSelectQuery(entity, filter_data_list: List):
        # Obtener las propiedades y valores no nulos del entity
        propiedades = [propiedad for propiedad in dir(entity)
                       if not callable(getattr(entity, propiedad))
                       and not propiedad.startswith("__")
                       and propiedad != "filterData"]
        valores = [getattr(entity, propiedad) for propiedad in propiedades]

        # Filtrar las propiedades y valores para excluir los nulos y propiedades no deseadas
        propiedades_no_nulas = []
        valores_no_nulos = []
        for propiedad, valor in zip(propiedades, valores):

            # print(f"{propiedad} - {valor} is no null: {valor is not None} -and: {isinstance(valor, (list))}")
            # print(valor is not None and isinstance(valor, (list, object)) == False)
            if valor is not None and isinstance(valor, list) == False:
                propiedades_no_nulas.append(propiedad)
                # Convertir los valores a cadenas, rodeando con comillas solo si no son numéricos
                valor_formateado = f"'{valor}'" if not isinstance(
                    valor, (int, float)) else str(valor)
                valores_no_nulos.append(f"{propiedad} = {valor_formateado}")

        # Construir la cláusula WHERE para la condición de selección
        where_clause = ''
        condition = ''
        if len(valores_no_nulos) != 0:
            where_clause = ' AND '.join(valores_no_nulos)

        # Agregar las condiciones de FilterData a la cláusula WHERE
        for filter_data in filter_data_list:
            prop_name = filter_data.PropName
            filter_type = filter_data.FilterType
            values = filter_data.Values

            # Construir la condición según el FilterType
            if filter_type == "like":
                condition = f"{prop_name} {filter_type} '%{values[0]}%'"
            elif filter_type in ("=", ">", "<", ">=", "between"):
                condition = f"{prop_name} {filter_type} {values[0]}"
                if filter_type == "between":
                    condition += f" AND {values[1]}"
            elif filter_type in ("in", "not in"):
                condition = f"{prop_name} {filter_type} ({', '.join(map(str, values))})"
            else:
                # Tratar otros casos según sea necesario
                pass

            # Agregar la condición a la cláusula WHERE
            if len(where_clause) == 0:
                where_clause += f" {condition}"
            else:
                where_clause += f" AND {condition}"

        # Generar la consulta SELECT dinámicamente
        if len(where_clause) != 0:
            consulta = f"SELECT {', '.join(propiedades)} FROM {type(entity).__name__} WHERE {where_clause}"
        else:
            consulta = f"SELECT {', '.join(propiedades)} FROM {type(entity).__name__}"

        return consulta

    @staticmethod
    def GetList(entity):
        # Crear una lista de instancias de la entity a partir de los resultados del método select
        instancias = []
        resultados = GDatos.GetListData(entity, entity.filterData)
        propiedades = [propiedad for propiedad in dir(entity)
                       if not callable(getattr(entity, propiedad))
                       and not propiedad.startswith("__")
                       and propiedad != "filterData"]
        for resultado in resultados:
            # Crea una instancia de la entity con los argumentos proporcionados por el resultado
            atributos = {str(propiedades[i]): resultado[i]
                         for i in range(0, len(propiedades))}
            instancia = type(entity)(**atributos)
            instancias.append(instancia)

        return instancias

    @staticmethod
    def obtener_tablas():
        # Configurar la conexión a la base de datos
        conexion = GDatos.CrearConexion()
        # Crear un cursor
        cursor = conexion.cursor()
        try:
            # Consulta SQL para obtener la lista de tablas en el esquema 'public'
            query = """
                SELECT table_name
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """
            # Ejecutar la consulta
            cursor.execute(query)
            # Obtener los resultados
            tablas = cursor.fetchall()
            return [tabla[0] for tabla in tablas]
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()

    @staticmethod
    def obtener_info_columnas(table_name):
        # Configurar la conexión a la base de datos
        conexion = GDatos.CrearConexion()
        # Crear un cursor
        cursor = conexion.cursor()
        try:
            # Consulta SQL para obtener información de las columnas de una tabla específica
            query = f"""
                SELECT
                    column_name,
                    data_type
                FROM
                    information_schema.columns
                WHERE
                    table_name = '{table_name}'
            """
            # Ejecutar la consulta
            cursor.execute(query)
            # Obtener los resultados
            resultados = cursor.fetchall()
            return resultados
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conexion.close()
