"""
Alumno: Álvaro Román Gómez
Fecha: 13/10/2020

"""
import json
from models import *
from validations import *
from stringcolor import *

class Carga:
    """
    Gestiona la carga de datos de piezas y fabricantes en la base de datos a partir de ficheros CSV.
    """
    def carga_datos_csv(self,fichero):
        """
        A partir de un fichero CSV devuelve una lista con los encabezados y una lista con el resto de líneas de datos.
        """
        with open(fichero,"r") as f:
            lines = f.readlines()
        header = lines[0]
        data = lines[1:]
        return header,data

    def carga_datos_fabricantes(self,fichero):
        """
        A partir de un fichero CSV crea un registro en la tabla de fabricantes para cada una de las líneas del archivo.
        """
        headers,data = self.carga_datos_csv(fichero)
        duplicados = []
        numero_linea = 0
        for line in data:
            numero_linea += 1
            try:
                data_line = line.split(",")
                numero_registro =data_line[0].upper()
                nombre = data_line[1].upper()
                localidad = data_line[2].upper()
                cif = data_line[3].upper()
                if check_registro_fabricante(numero_registro) and check_string_noempty(nombre) and check_string_noempty(localidad) and check_cif_fabricante(cif):
                    Fabricantes.create(numero_registro_fabricante=numero_registro,
                                        nombre_fabricante=nombre,
                                        localidad=localidad,
                                        cif=cif
                                        )
                else :
                    print(cs(f"El formato de algún campo de la línea de archivo {numero_linea} no coincide con el que debería ser y no se ha añadido a la base de datos.".center(200),"red4").bold())
                    pass
            except IntegrityError:
                duplicados.append(nombre)
        if duplicados != []:
            print(cs(f"Los fabricantes {', '.join(duplicados)} ya existían en la base de datos.".center(200),"red4").bold())
        print(cs("La información de los fabricantes ha sido cargada con éxito.".center(200),"green2").bold())

    def carga_datos_piezas(self,fichero):
        """
        A partir de un fichero CSV crea un registro en la tabla de piezas para cada una de las líneas del archivo.
        """
        headers, data = self.carga_datos_csv(fichero)
        duplicados = []
        numero_linea = 0
        for line in data:
            numero_linea += 1
            try:
                data_line = line.split(",")
                numero_registro = data_line[0].upper()
                fecha = data_line[2].split(" ")[0]
                nombre = data_line[1].upper()
                fabricante = data_line[3].upper()
                precio = data_line[5]
                if check_registro_pieza(numero_registro) and check_formato_fecha(fecha) and check_string_noempty(nombre) and check_fabricante(fabricante) and check_precio(precio):
                    Piezas.create(numero_registro_pieza=numero_registro,
                                    nombre_pieza= nombre,
                                    fecha_fabricacion=fecha,
                                    fabricante_pieza= Fabricantes.get(nombre_fabricante=fabricante),
                                    precio= float(precio),
                                    )
                else:
                    print(cs(f"El formato de algún campo de la línea de archivo {numero_linea} no coincide con el que debería ser y no se ha añadido a la base de datos.".center(200),"red4").bold())
                    pass
            except IntegrityError:
                duplicados.append(numero_registro)
        if duplicados != []:
            print(cs(f"Las piezas con números de registro {', '.join(duplicados)} ya existían en la base de datos.".center(200),"red4").bold())
        print(cs("La información de las piezas ha sido cargada con éxito.".center(200),"green2").bold())

def show_menu():
    """
    Muestra un menú con las opciones del programa.
    """
    print(cs("MENU PRINCIPAL".center(200),"white2").bold())
    print(cs("MENÚ PIEZAS".center(200),"blue").bold())
    print(cs("A - Crear Pieza".center(200),"blue"))
    print(cs("B - Info. Pieza".center(200),"blue"))
    print(cs("C - Modificar Pieza".center(200),"blue"))
    print(cs("D - Eliminar Pieza".center(200),"blue"))
    print(cs("MENÚ FABRICANTES".center(200),"purple").bold())
    print(cs("E - Crear Fabricante".center(200),"purple"))
    print(cs("F - Info. Fabricante".center(200),"purple"))
    print(cs("G - Modificar Fabricante".center(200),"purple"))
    print(cs("H - Eliminar Fabricante".center(200),"purple"))
    print(cs("MENÚ ÓRDENES DE COMPRA".center(200),"orange").bold())
    print(cs("I - Crear Órden de compra".center(200),"orange"))
    print(cs("J - Info. Órden de compra".center(200),"orange"))
    print(cs("MENÚ INFORMES".center(200),"gold").bold())
    print(cs("K - Generar informe".center(200),"gold"))
    print(cs("S - SALIR".center(200),"white2").bold())

def ejecutar_menu():
    while True:
        show_menu()
        input_data = input(">>> ").upper()
        if input_data == "S":
            print(cs("Programa finalizado".center(200),"white2").bold())
            print(cs("Hasta la próxima".center(200), "white2").bold())
            break
        elif input_data == "A":
            crear_pieza()

        elif input_data == "B":
            info_pieza()

        elif input_data == "C":
            mod_pieza()

        elif input_data == "D":
            delete_pieza()

        elif input_data == "E":
            crear_fabricante()

        elif input_data == "F":
            info_fabricante()

        elif input_data == "G":
            mod_fabricante()

        elif input_data == "H":
            delete_fabricante()

        elif input_data == "I":
            crear_orden()

        elif input_data == "J":
            info_orden()

        elif input_data == "K":
            informe()
        else:
            print(cs("Introduce una opción de menú correcta o S para salir.".center(200),"red4").bold())
            pass

#OPCIONES MENÚ PIEZAS
def crear_pieza():
    """
    Crea un registro de pieza en la base de datos a patir de los datos proporcionados.
    Los número de registro son únicos.
    """
    #INTRODUCIR DATOS DE PIEZA
    #NOMBRE DE PIEZA
    nombre_pieza = input("Nombre Pieza: ").upper()
    while True:
        if check_string_noempty(nombre_pieza):
            break
        else:
            nombre_pieza = input("No se admiten campos en blanco. Nombre Pieza: ").upper()

    #NUMERO DE REGISTRO
    numero_registro_pieza = input("Número de registro: ").upper()
    # VALIDACIÓN DEL FORMATO NÚMERO DE REGISTRO DE LA PIEZA
    while True:
        if check_registro_pieza(numero_registro_pieza):
            break
        else:
            numero_registro_pieza = input("El número de registro debe tener el siguiente formato: A#####. Introdúcelo de nuevo: ").upper()
    #VALIDAR QUE LA PIEZA YA EXISTE EN LA BASE DE DATOS
    while True:
        if check_piezas(numero_registro_pieza):
            print(cs(f"La pieza con número de registro {numero_registro_pieza} ya existe en la base de datos.","red2").bold())
            break
        #SI NO EXISTE PEDIR EL RESTO DE LOS DATOS
        else:
            #FECHA DE FABRICACIÓN PIEZA
            fecha_fabricacion_pieza = input("Fecha de fabricación: ")
            while True:
                if check_formato_fecha(fecha_fabricacion_pieza):
                    break
                else:
                    fecha_fabricacion_pieza = input("La fecha debe tener un formato dd/mm/aaaa: ")

            #FABRICANTE PIEZA
            fabricante_pieza = input("Fabricante de la pieza: ").upper()
            #VALIDACIÓN DEL FABRICANTE DE LA PIEZA
            while True:
                if check_fabricante(fabricante_pieza):
                    break
                else:
                    print(cs(f"El fabricante {fabricante_pieza} no existe en la base de datos.","red2").bold())
                    nuevo_fabricante = input("¿Quieres crear un nuevo fabricante? y/n: ").upper()
                    while True:
                        if nuevo_fabricante == "Y":
                            nuevo_fabricante = crear_fabricante()
                            fabricante_pieza = nuevo_fabricante[0]
                            print(cs(f"La pieza {nombre_pieza} con número de registro {numero_registro_pieza} ha sido asignada al nuevo fabricante.","green2").bold())
                            break
                        elif nuevo_fabricante == "N":
                            fabricante_pieza = input("Entonces vuelve a introducir un fabricante que exista en la base de datos: ").upper()
                            break
                        else:
                            nuevo_fabricante = input("No te he entendido. ¿Quieres crear un nuevo fabricante? y/n: ").upper()

            #VALIDACIÓN DEL PRECIO DE LA PIEZA
            precio = input("Precio: ")
            while True:
                if check_precio(precio):
                    precio = float(precio)
                    break
                else:
                    precio = input("Tienes que introducir un número entero o decimal. Precio: ")

            #CREAR REGISTRO DE PIEZA
            Piezas.create(nombre_pieza=nombre_pieza,
                          numero_registro_pieza=numero_registro_pieza,
                          fecha_fabricacion=fecha_fabricacion_pieza,
                          fabricante_pieza=Fabricantes.get(nombre_fabricante=fabricante_pieza),
                          precio=precio,
                          )
            print(cs(f"La pieza con número de registro {numero_registro_pieza} se ha creado con éxisto.","green2").bold())
            return nombre_pieza, numero_registro_pieza, fecha_fabricacion_pieza, fabricante_pieza, precio


def info_pieza():
    """
    Proporciona la información de la pieza identificada con su número de registro.
    """
    pieza = input("Introduce el número de registro de la pieza que quieres consultar: ").upper()
    #VALIDAR FORMATO DE NUMERO DE REGISTRO
    while True:
        if check_registro_pieza(pieza):
            break
        else:
            pieza = input("El número de registro debe tener el siguiente formato: A#####. Introdúcelo de nuevo: ").upper()
    #VERIFICAR SI LA PIEZA ESTÁ EN LA BASE DE DATOS
    if check_piezas(pieza):
        pieza_select = Piezas.select(Piezas.nombre_pieza,Piezas.numero_registro_pieza,Piezas.fecha_fabricacion,Fabricantes.localidad,Fabricantes.nombre_fabricante,Piezas.precio,Piezas.piezas_vendidas)\
                        .join(Fabricantes).where(Piezas.numero_registro_pieza==pieza)
        print(cs(f"Información de la pieza con número de registro {pieza}: ".upper(),"white2").bold())
        for i in pieza_select.objects():
            print(f"Pieza: {i.nombre_pieza}")
            print(f"Número de registro: {i.numero_registro_pieza}")
            print(f"Fecha de fabricación: {i.fecha_fabricacion}")
            print(f"Fabricante: {i.nombre_fabricante}")
            print(f"Lugar de fabricación: {i.localidad}")
            print(f"Precio: {i.precio}€")
            print(f"Número de unidades vendidas: {i.piezas_vendidas}")

    else:
        print(cs(f"La pieza con número de registro {pieza} no existe en la base de datos.","red2").bold())


def mod_pieza():
    """
    Permite modificar los diferentes campos de un pieza indentificada por su número de registro.
    Los números de registro y las unidades vendidas no pueden ser modificadas.

    """
    registro_pieza = input("Introduce el número de registro de la pieza que quieres modificar: ").upper()
    #VALIDAR FORMATO DE NUMERO DE REGISTRO
    while True:
        if check_registro_pieza(registro_pieza):
            break
        else:
            registro_pieza = input(f"El número de registro tiene que tener el formato A#####: ").upper()
    #VERIFICAR QUE LA PIEZA EXISTE EN LA BASE DE DATOS
    while True:
        if check_piezas(registro_pieza):
            pieza = Piezas.select().where(Piezas.numero_registro_pieza == registro_pieza)
            #MODIFICACION DATOS
            for i in pieza:
                #MODIFICACION DEL NOMBRE DE LA PIEZA
                confirmacion_nombre = input(f"¿Quieres modificar el nombre de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                while True:
                    if confirmacion_nombre == "Y":
                        nuevo_nombre = input("Introduce el nuevo nombre: ").upper()
                        while True:
                            if check_string_noempty(nuevo_nombre):
                                i.nombre_pieza = nuevo_nombre
                                i.save()
                                print(cs("Nombre de la pieza modificado correctamente.","green2").bold())
                                break
                            else:
                                nuevo_nombre = input("No se admiten campos en blanco. Introduce el nuevo nombre de la pieza: ").upper()
                        break
                    elif confirmacion_nombre == "N":
                        break
                    else:
                        confirmacion_nombre = input(f"No te he entendido. ¿Quieres modificar el nombre de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                #MODIFICACION DE LA FECHA DE FABRICACION
                confirmacion_fecha = input(f"¿Quieres modificar la fecha de fabricación de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                while True:
                    if confirmacion_fecha == "Y":
                        nueva_fecha = input("Introduce la nueva fecha de fabricación: ")
                        while True:
                            if check_formato_fecha(nueva_fecha):
                                i.fecha_fabricacion = nueva_fecha
                                i.save()
                                print(cs("Fecha de fabricación de la pieza modificado correctamente.","green2").bold())
                                break
                            else:
                                nueva_fecha = input("La fecha debe tener un formato dd/mm/aaaa: ")
                        break
                    elif confirmacion_fecha == "N":
                        break
                    else:
                        confirmacion_fecha = input(f"No te he entendido. ¿Quieres modificar la fecha de fabricación de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                #MODIFICACION DEL FABRICANTE
                confirmacion_fabricante = input(f"¿Quieres modificar el fabricante de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                while True:
                    if confirmacion_fabricante == "Y":
                        nuevo_fabricante = input("Introduce el nuevo fabricante: ").upper()
                        flag = True
                        while flag == True:
                            if check_fabricante(nuevo_fabricante):
                                i.fabricante_pieza = Fabricantes.get(Fabricantes.nombre_fabricante == nuevo_fabricante)
                                i.save()
                                print(cs("Fabricante de la pieza modificado correctamente.","green2").bold())
                                break
                            else:
                                print(cs(f"El fabricante {nuevo_fabricante} no existe en la base de datos.","red2").bold())
                                #CREAR NUEVO FABRICANTE
                                confirmacion_creacion = input("¿Quieres crear un nuevo fabricante? y/n (S para salir y no modificarlo): ").upper()
                                while True:
                                    if confirmacion_creacion == "Y":
                                        nuevo_fabricante = crear_fabricante()
                                        i.fabricante_pieza = Fabricantes.get(Fabricantes.nombre_fabricante == nuevo_fabricante[0])
                                        i.save()
                                        print(cs(f"Fabricante de la pieza modificado correctamente","green2").bold())
                                        break
                                    elif confirmacion_creacion == "N":
                                        nuevo_fabricante = input("Entonces vuelve a introducir un fabricante que exista en la base de datos: ").upper()
                                        break
                                    elif confirmacion_creacion == "S":
                                        flag = False
                                        print(cs("Fabricante no modificado.","red2").bold())
                                        break
                                    else:
                                        confirmacion_creacion = input("No te he entendido. ¿Quieres crear un nuevo fabricante? y/n: ").upper()
                        break
                    elif confirmacion_fabricante == "N":
                        break
                    else:
                        confirmacion_fabricante = input(
                            f"No te he entendido. ¿Quieres modificar el fabricante de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                #MODIFICAR PRECIO
                confirmacion_precio = input(f"¿Quieres modificar el precio de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
                while True:
                    if confirmacion_precio == "Y":
                        nuevo_precio = input("Introduce el nuevo precio: ")
                        while True:
                            if check_precio(nuevo_precio):
                                i.precio = nuevo_precio
                                i.save()
                                print("Precio de la pieza modificado correctamente.")
                                break
                            else:
                                nuevo_precio = input("Tienes que introducir un número entero o decimal. Nuevo precio: ")
                        break
                    elif confirmacion_precio == "N":
                        break
                    else:
                        confirmacion_precio = input(f"No te he entendido. ¿Quieres modificar el precio de la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
            #CONFIRMACION MODIFICACION DE DATOS
            print(cs(f"Datos de la pieza con número de registro {registro_pieza} modificados con éxito.","green2").bold())
            break
        else:
            print(cs(f"La pieza con número de registro {registro_pieza} no existe en la base de datos.","red2").bold())
            break


def delete_pieza():
    """
    Elimina el registro de una pieza identificada por su número de registro.
    """
    registro_pieza = input("Introduce el número de registro de la pieza que quieres eliminar: ").upper()
    #VALIDAR FORMATO NUMERO REGISTRO
    while True:
        if check_registro_pieza(registro_pieza):
            break
        else:
            registro_pieza = input(f"El número de registro tiene que tener el formato A#####: ").upper()

    while True:
        if check_piezas(registro_pieza):
            pieza = Piezas.select().where(Piezas.numero_registro_pieza==registro_pieza)
            confirmacion = input(cs(f"¿Seguro que quieres eliminar la pieza con número de registro {registro_pieza}?\nSe eliminarán todas las órdenes de compra relacionadas con esta pieza. y/n: ".upper(),"red4").bold()).upper()
            while True:
                if confirmacion == "Y":
                    for i in pieza:
                        compras_piezas = ComprasPiezas.select().where(ComprasPiezas.piezas_id == i.id)
                        if compras_piezas.exists():
                            for x in compras_piezas:
                                compras = Compras.select().where(Compras.id == x.compras_id)
                                for h in compras:
                                        compras_through = ComprasPiezas.select().where(ComprasPiezas.compras_id == h.id)
                                        for t in compras_through:
                                            t.delete_instance()
                                            i.delete_instance()
                                            x.delete_instance()
                                            h.delete_instance()
                        else:
                            i.delete_instance()

                        print(cs(f"La pieza con número de registro {i.numero_registro_pieza} ha sido eliminada con éxito.","green2").bold())
                    break
                elif confirmacion == "N":
                    for i in pieza:
                        print(cs(f"Pieza con número de registro {i.numero_registro_pieza} no eliminada.","red2").bold())
                    break
                else:
                    for i in pieza:
                        confirmacion = input(f"No te he entendido. ¿Quieres elminar la pieza con número de registro {i.numero_registro_pieza}? y/n: ").upper()
            break
        else:
            print(cs("Esa pieza no existe en la base de datos.","red2").bold())
            break

#OPCIONES MENÚ FABRICANTE
def crear_fabricante():
    """
    Crea un nuevo registro de fabricante a partir de la información proporcionada.
    """
    #VALIDACIÓN FORMATO NOMBRE FABRICANTE
    nombre_fabricante = input("Nombre Fabricante: ").upper()
    while True:
        if check_string_noempty(nombre_fabricante):
            break
        else:
            nombre_fabricante = input("No se admiten campos en blanco. Nombre del fabricante: ").upper()
    #VALIDAR QUE EXISTE EN LA BASE DE DATOS

    if check_fabricante(nombre_fabricante):
        print(cs(f"El fabricante {nombre_fabricante} ya existe en la base de datos.","red2").bold())
    else:
        #VALIDACIÓN FORMATO NÚMERO REGISTRO FABRICANTE
        numero_registro_fabricante = input("Número de registro: ").upper()
        while True:
            if check_registro_fabricante(numero_registro_fabricante):
                break
            else:
                numero_registro_fabricante = input("El número de registro tiene que tener el formato AAA###: ").upper()
        #VALIDAR SI EXISTE EL NÚMERO DE REGISTRO EN LA BASE DE DATOS
        if check_registro_fabricante_existe(numero_registro_fabricante):
            print(cs(f"El fabricante con número de registro {numero_registro_fabricante} ya existe en la base de datos.","red2").bold())
        else:
            #VALIDACIÓN LOCALIDAD FABRICANTE
            localidad = input("Localidad: ").upper()
            while True:
                if check_string_noempty(localidad):
                    break
                else:
                    localidad = input("No se admiten campos vacíos. Localidad: ").upper()
            #VALIDACIÓN CIF FABRICANTE
            cif = input("CIF: ").upper()
            while True:
                if check_cif_fabricante(cif):
                    break
                else:
                    cif = input("El CIF tiene que formato A#######A o A########: ").upper()

            Fabricantes.create(nombre_fabricante=nombre_fabricante,
                            numero_registro_fabricante=numero_registro_fabricante,
                            localidad=localidad,
                            cif=cif,
                            )
            print(cs(f"Fabricante {nombre_fabricante} con número de registro {numero_registro_fabricante} creado con éxito.","green2").bold())

            return nombre_fabricante,numero_registro_fabricante,localidad,cif


def info_fabricante():
    """
    Proporciona información de un fabricante identificado por su nombre.
    """
    fabricante = input("Introduce el nombre del fabricante sobre que quieres hacer la consulta: ").upper()
    #VALIDAR FORMATO NOMBRE FABRICANTE
    while True:
        if check_string_noempty(fabricante):
            break
        else:
            fabricante = input("No se adminten campos vacíos. Introduce el nombre del fabricante que quieres consultar: ")

    #VALIDAR SI EL FABRICANTE EXISTE EN LA BASE DE DATOS
    if check_fabricante(fabricante):
        fabricante_select = Fabricantes.select().where(Fabricantes.nombre_fabricante == fabricante)
        print(cs(f"Información del fabricante {fabricante}: ".upper(),"white2").bold())
        for i in fabricante_select:
            print(f"Nombre: {i.nombre_fabricante}")
            print(f"Número de registro: {i.numero_registro_fabricante}")
            print(f"Localidad: {i.localidad}")
            print(f"CIF: {i.cif}")
    else:
        print(cs(f"El fabricante {fabricante} no existe en la base de datos.","red2").bold())

def mod_fabricante():
    """
    Permite modificar la información de un fabricante identificado por su nombre.
    El número de registro no puede ser modificado.
    """
    nombre_fabricante = input("Introduce el nombre del fabricante que quieres modificar: ").upper()
    #VALIDACION FORMATO NOMBRE FABRICANTE
    while True:
        if check_string_noempty(nombre_fabricante):
            break
        else:
            nombre_fabricante = input("No se adminten campos vacíos. Introduce el nombre del fabricante que quieres modificar: ").upper()

    #COMPROBAR QUE EL FABRICANTE EXISTE EN LA BASE DE DATOS
    if check_fabricante(nombre_fabricante):
        fabricante = Fabricantes.select().where(Fabricantes.nombre_fabricante == nombre_fabricante)
        for i in fabricante:
            #MODIFICAR EL NOMBRE DEL FABRICANTE
            confirmacion_nombre = input(f"¿Quieres modificar el nombre del fabricante {nombre_fabricante}? y/n: ").upper()
            flag = True
            while True:
                if confirmacion_nombre == "Y":
                    nuevo_nombre = input("Introduce el nuevo nombre: ").upper()
                    #VALIDACION FORMATO NOMBRE FABRICANTE
                    while True:
                        if check_string_noempty(nuevo_nombre):
                            break
                        else:
                            nuevo_nombre = input("No se admiten campos en blanco. Introduce el nuevo nombre del fabricante: ").upper()

                    #VALIDAR SI EL NUEVO YA EXISTE EN LA BASE DE DATOS
                    if check_fabricante(nuevo_nombre):
                        print(cs(f"Ya existe un fabricante con el nombre {nuevo_nombre} en la base de datos.","red2").bold())
                        flag = False
                        break
                    else:
                        i.nombre_fabricante = nuevo_nombre
                        i.save()
                        print(cs("Nombre del fabricante modificado correctamente.","green2").bold())
                        break
                elif confirmacion_nombre == "N":
                    break
                else:
                    confirmacion_nombre = input(f"No te he entendido. ¿Quieres modificar el nombre del fabricante {nombre_fabricante}? y/n: ").upper()

            while flag == True:
                # MODIFICAR LA LOCALIDAD DEL FABRICANTE
                confirmacion_localidad = input(
                    f"¿Quieres modificar la localidad del fabricante {nombre_fabricante}? y/n: ").upper()
                while True:
                    if confirmacion_localidad == "Y":
                        nueva_localidad = input("Introduce la nueva localidad: ").upper()
                        while True:
                            if check_string_noempty(nueva_localidad):
                                i.localidad = nueva_localidad
                                i.save()
                                print("Localidad del fabricante modificada correctamente.")
                                break
                            else:
                                nueva_localidad = input("No se admiten campos vacíos. Localidad: ").upper()
                        break
                    elif confirmacion_localidad == "N":
                        break
                    else:
                        confirmacion_localidad = input(
                            f"No te he entendido. ¿Quieres modificar la localidad del fabricante {nombre_fabricante}? y/n: ").upper()
                # MODIFICAR EL CIF DEL FABRICANTE
                confirmacion_cif = input(
                    f"¿Quieres modificar el CIF del fabricante {nombre_fabricante}? y/n: ").upper()
                while True:
                    if confirmacion_cif == "Y":
                        nuevo_cif = input("Introduce el nuevo CIF: ")
                        while True:
                            if check_cif_fabricante(nuevo_cif):
                                i.cif = nuevo_cif
                                i.save()
                                print("CIF del fabricante modificada correctamente.")
                                break
                            else:
                                nuevo_cif = input(
                                    "El CIF tiene que formato A#######A o A########: ").upper()
                        break
                    elif confirmacion_cif == "N":
                        break
                    else:
                        confirmacion_cif = input(
                            f"No te he entendido. ¿Quieres modificar el CIF del fabricante {nombre_fabricante}? y/n: ").upper()
                # CONFIRMACION MODIFICACION DE DATOS
                print(cs(f"Datos del fabricante {nombre_fabricante} modificados con éxito.","green2").bold())
                break
    else:
        print(cs(f"El fabricante {nombre_fabricante} no existe en la base de datos.","red2").bold())


def delete_fabricante():
    """
    Elimina el registro de un fabricante identificado por su nombre.
    """
    nombre_fabricante = input("Introduce el nombre del fabricante que quieres eliminar: ").upper()
    #VALIDAR FORMATO NOMBRE FABRICANTE
    while True:
        if check_string_noempty(nombre_fabricante):
            break
        else:
            nombre_fabricante = input("No se adminten campos vacíos. Introduce el nombre del fabricante que quieres modificar: ").upper()

    if check_fabricante(nombre_fabricante):
        fabricante = Fabricantes.select().where(Fabricantes.nombre_fabricante==nombre_fabricante)
        #CONFIRMAR ELIMINACION DE REGISTRO
        confirmacion = input(cs(f"¿Seguro que quieres eliminar el fabricante {nombre_fabricante}? \nSe eliminarán todas las piezas y órdenes asociadas. y/n: ".upper(),"red4").bold()).upper()
        while True:
            if confirmacion == "Y":
                #ELIMINAR FABRICANTE Y REGISTROS ASOCIADOS
                for i in fabricante:
                    piezas = Piezas.select().where(Piezas.fabricante_pieza == i.id)
                    if piezas.exists():
                        for x in piezas:
                            print(f"pieza {x.nombre_pieza}")
                            compras_piezas = ComprasPiezas.select().where(ComprasPiezas.piezas_id == x.id)
                            if compras_piezas.exists():
                                for h in compras_piezas:
                                    compras = Compras.select().where(Compras.id == h.compras_id)
                                    for c in compras:
                                        compras_through = ComprasPiezas.select().where(ComprasPiezas.compras_id==c.id)
                                        for t in compras_through:
                                            t.delete_instance()
                                            c.delete_instance()
                                            h.delete_instance()
                                            x.delete_instance()
                            else:
                                print("No existen compras")
                                x.delete_instance()
                    else:
                        print("No existen piezas")
                        i.delete_instance()
                    i.delete_instance()

                    print(cs(f"El fabricante {nombre_fabricante} ha sido eliminado con éxito.","green2").bold())
                break
            elif confirmacion == "N":
                print(cs(f"Fabricante {nombre_fabricante} no eliminado.","green2").bold())
                break
            else:
                confirmacion = input(f"No te he entendido. ¿Quieres elminar el fabricante {nombre_fabricante}? y/n: ").upper()

    else:
        print(cs(f"El fabricante {nombre_fabricante} no existe en la base de datos.","red2").bold())

def crear_orden():
    """
    Crea un nuevo registro de compra a partir de la información proporcionada.
    El ID de la compra se genera de forma automática.
    """
    #GENERAR ID DE COMPRA
    try:
        id_compra = Compras.select(Compras.id_compra).order_by(-Compras.id_compra)[0]
        id_compra = id_compra.id_compra[-5:]
        id_compra = int(id_compra.lstrip("0"))
        id_compra += 1
        id_compra = "FV"+str(id_compra).zfill(5)
    except IndexError:
        id_compra = "FV"+"1".zfill(5)

    #DATOS FECHA COMPRA
    fecha_compra = input("Introduce la fecha de la compra: ")
    while True:
        if check_formato_fecha(fecha_compra):
            break
        else:
            fecha_compra = input("La fecha debe tener un formato dd/mm/aaaa: ")

    #DATOS VENDEDOR
    vendedor = input("Introduce el nombre del vendedor: ").upper()
    while True:
        if check_string_noempty(vendedor):
            break
        else:
            vendedor = input("No se adminten campos en blanco. Introduce el nombre del vendedor: ").upper()

    #DATOS PIEZAS
    lista_piezas = []
    otra_pieza = "Y"
    while otra_pieza != "N":
        input_pieza = input("Introduce el número de registro de la pieza: ").upper()

        while True:
            if input_pieza in lista_piezas:
                print("Esa pieza ya ha sido añadida la lista de compra.")
                break
            else:
                while True:
                    if check_piezas(input_pieza):
                        lista_piezas.append(input_pieza)
                        break
                    else:
                        input_pieza = input("Esa pieza no existe en la base de datos. Vuelve a introducir el número de registro con formato A#####: ").upper()
                break

        otra_pieza = input("¿Quieres añadir otra pieza a la orden de compra? y/n: ").upper()
        while True:
            if (otra_pieza == "Y") or (otra_pieza == "N"):
                break
            else:
                otra_pieza = input("No te he entendido. ¿Quieres añadir otra pieza a la orden de compra? y/n: ").upper()

    # CREAR REGISTRO DE COMPRA
    Compras.create(id_compra=id_compra, fecha_compra=fecha_compra, vendedor=vendedor)

    #CREAR RELACIÓN ORDEN DE COMPRA Y PIEZAS
    lista_indices_piezas = []
    lista_precios = []
    for i in lista_piezas:
        pieza = Piezas.get(Piezas.numero_registro_pieza == i)
        pieza.piezas_vendidas += 1
        pieza.save()
        lista_indices_piezas.append(pieza)
        precios = Piezas.select(Piezas.precio).where(Piezas.numero_registro_pieza==i)
        for i in precios:
            lista_precios.append(i.precio)

    compra = Compras.get(Compras.id_compra == id_compra)
    compra.piezas.add(lista_indices_piezas)
    #MODIFICAR PRECIO COMPRA
    precios_compra = Compras.select().where(Compras.id_compra==id_compra)
    for i in precios_compra:
        i.precio = sum(lista_precios)
        i.save()
    print(cs(f"Orden de compra {id_compra} creada con éxito.","green2").bold())


def info_orden():
    """
    Proporciona la información de un orden de compra identificada por su ID.
    """
    id_compra = input("Introduce el ID de la compra que quieres consultar: ").upper()
    #VALIDAR FORMATO
    while True:
        if check_id_orden(id_compra):
            break
        else:
            id_compra = input("El formato del ID debe ser FV#####: ").upper()
    #VALIDAR QUE EXISTE EN LA BASE DE DATOS
    while True:
        if check_orden(id_compra):
            #IMPRIMIR DATOS DE LA ORDEN DE COMPRA
            print(cs(f"Los datos de la orden de compra {id_compra} son los siguientes: ","white2").bold())
            compra = Compras.select().where(Compras.id_compra==id_compra)
            for i in compra:
                print(f"ID: {id_compra}")
                fecha = i.fecha_compra
                vendedor = i.vendedor
                print(f"Fecha de compra: {fecha}")
                print(f"Vendedor: {vendedor}")
                precio = i.precio
                pieza_compra = Compras.get(Compras.id_compra==id_compra)
                print("Piezas: ")
                for pieza in pieza_compra.piezas:
                    print(f"\t{pieza.nombre_pieza}")
                print(f"Precio total: {precio}")
            break
        else:
            print(cs("Esa orden de compra no existe en la base de datos.","red4").bold())
            break

#INFORME
#     """
#     Número de piezas vendidas
#     Ingresos totales por la venta de piezas
#     Fabricante más vendido
#     Fabricante menos vendido
#     Fabricante cuyas piezas son más caras
#     En qué época del año de fabrican mas piezas (invierno, primavera,verano, otoño)
#     En qué época del año de venden mas piezas (invierno, primavera,verano, otoño)
#     Listado completo de locaciones de fabricación de piezas, ordenado alfabéticamente.
#     Listado completo de fabricantes ordenados por su número de registro.
#     El empleado del mes (vendedor con más compras)
#     """

def piezas_vendidas():
    """
    A partir de la información de la base de datos devuelve el número total de piezas vendidas.
    """
    piezas_compra = ComprasPiezas.select()
    numero_piezas = 0
    for i in piezas_compra:
        numero_piezas += 1
    return numero_piezas

def ingresos_totales():
    """
    A partir de la información de la base de datos devuelve el total de ingresos.
    """
    compras = Compras.select(Compras.precio)
    ingreso_total = 0
    for i in compras:
        ingreso_total += i.precio
    return round(ingreso_total,2)

def fabricante_mas_vendido():
    """
    A partir de la información de la base de datos devuelve el fabricante más que más vende y el número de unidades vendidas
    por ese fabricante en formato tupla.
    """
    dic = {}
    piezas_compra = ComprasPiezas.select()
    for i in piezas_compra:
        consulta = Fabricantes.select().join(Piezas).where(Piezas.id==i.piezas.id)
        for fabricante in consulta:
            try:
                dic[fabricante.nombre_fabricante] += 1
            except KeyError:
                dic[fabricante.nombre_fabricante] = 1
    fabricante_mas_vendido = max(dic, key=dic.get)
    return fabricante_mas_vendido, dic[fabricante_mas_vendido]

def fabricante_piezas_caras():
    """
    A partir de la información de la base de datos devuelve el fabricante más caro de media y la media de sus precios
    en formato tupla.
    """
    dic = {}
    piezas_fabricante = Fabricantes.select().join(Piezas)
    for fabricante in piezas_fabricante:
        lista_piezas = []
        lista_precios = []
        for pieza in fabricante.piezas:
            lista_piezas.append(pieza)
            lista_precios.append(pieza.precio)
        dic[fabricante.nombre_fabricante] = sum(lista_precios)/len(lista_piezas)
    fabricante_mas_caro = max(dic, key=dic.get)
    return fabricante_mas_caro, dic[fabricante_mas_caro]

def epoca_fabricacion():
    """
    A partir de la información de la base de datos devuelve la época del año en la que se fabrican más piezas.
    """
    dic = {}
    piezas = Piezas.select(Piezas.fecha_fabricacion)
    for pieza in piezas:
        try:
            dic[date_seasons(pieza.fecha_fabricacion)] += 1
        except KeyError:
            dic[date_seasons(pieza.fecha_fabricacion)] = 1
    epoca_mas_fabricacion = max(dic, key=dic.get)
    return epoca_mas_fabricacion, dic[epoca_mas_fabricacion]

def epoca_ventas():
    """
    A partir de la información de la base de datos devuelve la época del año en la que se venden más piezas.
    """
    dic = {}
    compras = Compras.select(Compras.fecha_compra)
    for compra in compras:
        try:
            dic[date_seasons(compra.fecha_compra)] += 1
        except KeyError:
            dic[date_seasons(compra.fecha_compra)] = 1
    epoca_mas_ventas = max(dic,key=dic.get)
    return epoca_mas_ventas, dic[epoca_mas_ventas]


def listado_localidades():
    """
    A partir de la información de la base de datos devuelve el lista de localidades en las que se fabrican piezas.
    """
    fabricantes = Fabricantes.select().order_by(Fabricantes.localidad)
    lista_localidades = []
    for fabricante in fabricantes:
        lista_localidades.append(fabricante.localidad)
    lista_localidades = set(lista_localidades)
    return tuple(lista_localidades)

def listado_fabricantes():
    """
    A partir de la información de la base de datos devuelve el listado de fabricantes ordenados por su número de registro.
    """
    fabricantes = Fabricantes.select().order_by(Fabricantes.numero_registro_fabricante)
    lista_fabricantes = []
    for fabricante in fabricantes:
        lista_fabricantes.append(fabricante.nombre_fabricante)
    lista_fabricantes = set(lista_fabricantes)
    return tuple(lista_fabricantes)


def empleado_mes():
    """
    A partir de la información de la base de datos devuelve el empleado con más ventas.
    """
    dic = {}
    compras = Compras.select(Compras.vendedor)
    for compra in compras:
        try:
            dic[compra.vendedor] += 1
        except KeyError:
            dic[compra.vendedor] = 1
    empleado_mes = max(dic,key=dic.get)
    return empleado_mes, dic[empleado_mes]

def informe():
    """
    Genera un informe en formato JSON.
    """

    if lista_compras() != []:

        print(f"Número de piezas vendidas: {piezas_vendidas()}")
        print(f"Ingresos totales: {ingresos_totales()} €")
        print(f"El fabricante más vendido es {fabricante_mas_vendido()[0]} con {fabricante_mas_vendido()[1]} piezas vendidas")
        print(f"El fabricante con las piezas más caras es {fabricante_piezas_caras()[0]} con un precio promedio de {fabricante_piezas_caras()[1]} €")

        print(f"Las localidades de fabricación son las siguientes: {listado_localidades()}")
        print(f"El listado de fabricantes ordenados por número de registro es el siguiente: {listado_fabricantes()}")
        print(f"La época con mayor fabricación es {epoca_fabricacion()[0]} con {epoca_fabricacion()[1]} unidades fabricadas")
        print(f"La época con mayores ventas es {epoca_ventas()[0]} con {epoca_ventas()[1]} unidades vendidas")
        print(f"El empleado del mes es {empleado_mes()[0]} con {empleado_mes()[1]} ventas")

        informe = []
        informaciom_informe = {}
        informaciom_informe["Numero de piezas vendidas"] = piezas_vendidas()
        informaciom_informe["Ingresos totaltes"] = ingresos_totales()
        informaciom_informe["Fabricante mas vendido"] = fabricante_mas_vendido()[0]
        informaciom_informe["Fabricante mas caro"] = fabricante_piezas_caras()[0]
        informaciom_informe["Localidades de fabricacion"] = listado_localidades()
        informaciom_informe["Listado fabricantes"] = listado_fabricantes()
        informaciom_informe["Epoca con mayor fabricacion"] = epoca_fabricacion()[0]
        informaciom_informe["Epoca con mayores ventas"] = epoca_ventas()[0]
        informaciom_informe["Empleado del mes"] = empleado_mes()[0]
        informe.append(informaciom_informe)

        with open("informe_ventas.json", "w") as f:
            json.dump(informe,f)
            print(cs("Informe de ventas en formato JSON creado con éxito.","green2").bold())

    else:
        print(cs("No existen órdenes de compra en la base datos. El informe no puede ser generado.","red2").bold())