"""
Alumno: Álvaro Román Gómez
Fecha: 13/10/2020

"""

from peewee import *

db = SqliteDatabase("piezas.db")

#CREAR MODELO DE FABRICANTES
class Fabricantes(Model):
    """
    Nombre(str)
    Número registro fabricante(str)
    CIF(str)
    """

    nombre_fabricante = CharField(unique=True)
    numero_registro_fabricante = CharField(unique=True)
    localidad = CharField()
    cif = CharField()

    class Meta():
        database = db

#CREAR MODELOS DE PIEZAS
class Piezas(Model):
    """
    Nombre(str)
    Número registro pieza(str)
    Fecha de fabricación(datetime)
    Fabricante(str)
    Localidad de fabricación(str)
    Precio(float)
    Nº piezas vendidas(int)

    """

    nombre_pieza = CharField()
    numero_registro_pieza = CharField(unique=True)
    fecha_fabricacion = DateField()
    fabricante_pieza = ForeignKeyField(Fabricantes,
                                 field=Fabricantes.id,
                                 null= True,
                                 on_update="CASCADE",
                                 on_delete="CASCADE",
                                 backref = "piezas"
                                 )
    precio = FloatField()
    piezas_vendidas = IntegerField(default=0)

    class Meta():
        database = db

#CREAR MODELO DE ÓRDENES DE COMPRA
class Compras (Model):
    """
    - ID compra(str)
    - Fecha de compra(datetime)
    - Vendedor(str)
    - Piezas que incluye la compra(tupla)
    - Precio total(float)
    """
    id_compra = CharField() #DAR FORMATO AL ID DE LA COMPRA
    fecha_compra = DateField() #DAR FORMATO AL CAMPO DE FECHA
    vendedor = CharField()
    piezas = ManyToManyField(Piezas,backref = "piezas",on_delete="CASCADE",on_update="CASCADE")
    precio = FloatField(default=0)

    class Meta():
        database = db

ComprasPiezas = Compras.piezas.get_through_model()

db.connect()
db.create_tables([Piezas,Fabricantes,Compras,ComprasPiezas])
db.close()



