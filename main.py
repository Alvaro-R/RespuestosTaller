"""
Alumno: Álvaro Román Gómez
Fecha: 13/10/2020

"""
from methods import *


"""
Cargamos los diferentes datos de los ficheros CSV.
"""
print(cs(f"CARGA DE DATOS".center(200),"white2").bold())
#CARGA DE DATOS
carga = Carga()
#CARGA DE DATOS DE FABRICANTES
carga.carga_datos_fabricantes("fabricantes.csv")
#CARGA DE DATOS DE PIEZAS
carga.carga_datos_piezas("piezas.csv")

"""
Se muestra el menú con las diferentes opciones.
"""

# compra = Compras.create(id_compra="001",fecha_compra="12/05/1991",vendedor="Alvaro",pieza=,precio=)
# Piezas.get

ejecutar_menu()






