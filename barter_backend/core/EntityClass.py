from typing import List
from barter_backend.core.GDatos import GDatos
class FilterData:
    """
    Clase para representar un filtro de datos utilizado en consultas de base de datos.

    Atributos:
    - PropName (str): Nombre de la propiedad a filtrar.
    - FilterType (str): Tipo de filtro a aplicar (por ejemplo, "=", ">=", "in", etc.).
    - Values (List[str]): Lista de valores para aplicar el filtro.
    """
    def __init__(self, PropName: str, FilterType: str, Values: List[str]):
        self.PropName = PropName
        self.FilterType = FilterType
        self.Values = Values

    PropName: str
    FilterType: str
    Values: List[str]


class EntityClass:
    """
    Clase base para modelos de entidad en un sistema de base de datos.

    Atributos:
    - filterData (List[FilterData]): Lista de objetos FilterData que representan los filtros aplicados.
    """
    def __init__(self, *args, **kwargs):
        self.filterData: List[FilterData] = []

    def Save(self):
        """
        Guarda la instancia actual en la base de datos utilizando el servicio GDatos.
        """
        return GDatos.InserObject(self)

    def Update(self):
        """
        Actualiza la instancia actual en la base de datos utilizando el servicio GDatos.
        """
        return GDatos.UpdateObject(self)

    def Get(self):
        """
        Recupera una lista de instancias que coinciden con los filtros actuales utilizando el servicio GDatos.
        """
        return GDatos.GetList(self)

    def Where(self, filterData: List[FilterData]):
        """
        Establece los filtros de la instancia actual y recupera una lista filtrada utilizando el servicio GDatos.

        Parámetros:
        - filterData (List[FilterData]): Lista de objetos FilterData que representan los filtros a aplicar.
        """
        self.filterData = filterData
        return GDatos.GetList(self)