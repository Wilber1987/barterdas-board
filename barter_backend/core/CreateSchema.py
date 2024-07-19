# Obtener la lista de tablas
from barter_backend.core.GDatos import GDatos

def CreateSchema():

    tablas = GDatos.obtener_tablas()

    # Guardar las clases en un archivo .py
    with open('./clases_generadas.py', 'w') as file:
        file.write("# Clases generadas dinámicamente\n")
        file.write("from EntityClass import EntityClass\n")
        file.write("import datetime\n\n")
        for table_name in tablas:
            print(table_name)
            class_name = table_name.capitalize()
            file.write(f"class {class_name}(EntityClass):\n")
            column_info = GDatos.obtener_info_columnas(table_name)
            class_body = "    def __init__(self, **kwargs):\n"
            class_body += "        super().__init__(**kwargs)\n"      
            
            for column in column_info:
                attribute_name = column[0]
                #attribute_type = column[1]  # Puedes cambiar esto según tu lógica
                data_type = column[1]
                attribute_type = ''
                # Mapear tipos de datos de PostgreSQL a tipos de datos de Python
                if data_type == 'integer' or  data_type == 'bigint' or  data_type == 'int':
                    attribute_type = 'int'
                elif data_type == 'decimal' or data_type == 'float' or data_type == 'float4' or data_type == 'float8':
                    attribute_type = 'float'
                elif data_type == 'timestamp' or data_type == 'date':
                    attribute_type = 'datetime'
                elif data_type == 'bool' or data_type == 'boolean':
                    attribute_type = 'bool'
                else :
                    attribute_type = 'str'
                
                class_body += f"        self.{attribute_name}: {attribute_type}\n"            
            class_body += "        for key, value in kwargs.items():\n"
            class_body += "            setattr(self, key, value)\n"
            file.write(f"{class_body}")
            file.write("\n")
           