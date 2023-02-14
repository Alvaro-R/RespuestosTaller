"""
Alumno: Álvaro Román Gómez
Fecha: 13/10/2020

"""
import re
from datetime import datetime

from models import Fabricantes, Piezas, Compras, ComprasPiezas

def check_registro_pieza(registro):
    """
    A partir de un número de registro de pieza devulve verdadero si cumple con el formato establecido.
    """
    return bool(re.match(r"^[A-Z]{1}[0-9]{5}$",registro))

def check_formato_fecha(fecha):
    """
    A partir de un fecha devuelve verdadero si la fecha cumple con el formato establecido.
    """
    try:
        datetime.strptime(fecha,"%d/%m/%Y")
        return True
    except ValueError:
        return False

def lista_fabricantes():
    """
    A partir de la tabla de fabricantes devuelve un listado con todos los nombres.
    """
    lista = []
    for i in Fabricantes.select():
        lista.append(i.nombre_fabricante)
    return lista

def check_fabricante(fabricante):
    """
    A partir de un nombre de un fabricante devuelve verdadero si ya existe en la base de datos.
    """
    return fabricante in lista_fabricantes()

def lista_registros_fabricantes():
    """
    A partir de la tabla de fabricantes devuelve un listado con todos los números de registro.
    """
    lista = []
    for i in Fabricantes.select():
        lista.append(i.numero_registro_fabricante)
    return lista

def check_registro_fabricante_existe(registro):
    """
    A partir de un número de registro de un fabricante devuelve verdadero si ya existe en la base de datos.
    """
    return registro in lista_registros_fabricantes()

def lista_compras():
    """
    A partir de la tabla de ordenes de compra devuelve un listado con todos los ID de cada orden.
    """
    lista = []
    for i in Compras.select():
        lista.append(i.id_compra)
    return lista

def check_compras(compra):
    """
    A partir de un ID de compra devuelve si ya existe o no en la base de datos.
    """
    return compra in lista_compras()

def lista_piezas():
    """"
    A partir de la tabla de piezas devuelve un listado con sus números de registro.
    """
    lista = []
    for i in Piezas.select():
        lista.append(i.numero_registro_pieza)
    return lista

def check_piezas(pieza):
    """
    A partor del número de registro de una pieza devuelve verdadero si la pieza existe en la base de datos.
    """
    return pieza in lista_piezas()

def check_precio(precio):
    """
    Comprueba que el valor dado tiene formato de float y devuelve verdadero si es así.
    """
    try:
        float(precio)
        return True
    except ValueError:
        return False

def check_unidades(unidades):
    """
    Devuelve verdadero si el formato del input es integer.
    """
    try:
        int(unidades)
        return True
    except ValueError:
        return False

def check_registro_fabricante(registro):
    """
    Devuelve verdadero si el número de registro del fabricante cumple con el formato establecido.
    """
    return bool(re.match(r"^[A-Z]{3}[0-9]{3}$", registro))

def check_cif_fabricante(cif):
    """
    Devuelve verdadero si el CIF del fabricante cumple con el formato establecido.
    """
    return bool(re.match(r"^[A-Z]{1}[0-9]{7}[A-Z]{1}$", cif)) or bool(re.match(r"^[A-Z]{1}[0-9]{8}$", cif))

def check_string_noempty(string):
    """
    Devuelve vedadero si el input tiene formato string y no está vacío.
    """
    try:
        str(string)
        if string != "":
            return True
    except ValueError:
        return False

def check_id_orden(orden):
    """
    Devuelve verdadero si el ID de una orden de compra cumple con el formato establecido.
    """
    return bool(re.match(r"^FV[0-9]{5}$",orden))

def lista_ordenes():
    """
    Devuelve una lista con los ID de las órdenes de compra.
    """
    lista = []
    for i in Compras.select():
        lista.append(i.id_compra)
    return lista

def check_orden(orden):
    """
    Devuelve verdadeor si el ID de una orden existe en la base de datos.
    """
    return orden in lista_ordenes()

def date_seasons(date):
    """
    A partir de una fecha asocia un estación del año: invierno, primavera, verano, otoño.
    """
    year = date.split("/")[2]
    month = date.split("/")[1]
    day = date.split("/")[0]
    fecha = datetime.strptime(f"{day}/{month}/{year}","%d/%m/%Y")
    if datetime.strptime(f"22/3/{year}","%d/%m/%Y") < fecha < datetime.strptime(f"21/6/{year}","%d/%m/%Y"):
        season = "primavera".upper()
    elif datetime.strptime(f"22/6/{year}","%d/%m/%Y") < fecha < datetime.strptime(f"21/9/{year}","%d/%m/%Y"):
        season = "verano".upper()
    elif datetime.strptime(f"22/9/{year}","%d/%m/%Y") < fecha < datetime.strptime(f"21/12/{year}","%d/%m/%Y"):
        season = "otoño".upper()
    else:
        season = "invierno".upper()
    return season










