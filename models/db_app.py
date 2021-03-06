# -*- coding: utf-8 -*-

#2.14.6-stable+timestamp.2016.05.10.00.21.47
#(Ejecutando en Rocket 1.2.6, Python 2.7.3)
"""
buscar actualizaciones

Pruebe la interfaz móvil

Nueva aplicación

Nombre de la aplicación:

Crear
Suba e instale una aplicación empaquetada
# Archivo para definir las tablas comunes para todos
"""

# -*- coding: utf-8 -*-
class IS_CUIT(object):
    def __init__(self, error_message='Debe ser un CUIT válido en formato XX-YYYYYYYY-Z'):
        self.error_message = error_message
    def __call__(self, value):
        # validaciones mínimas
        
        if len(value) == 13 and value[2] == "-" and value[11] == "-":
            base = [5,4,3,2,7,6,5,4,3,2]
            cuit = value.replace("-","") # remuevo las barras
            # calculo el dígito verificador:
            aux = 0
            for i in range(0,10):
                aux += int(cuit[i])*base[i]
            aux = 11-(aux-(int(aux / 11)*11))
            if aux==11:
                aux = 0
            if aux==10:
                aux = 9
            if aux == int(cuit[10]):
                return (value, None)
        return (value,self.error_message)
    def formatter(self, value):
        return value

class IS_NOT_COMA(object):
    def __init__(self, error_message='Error'):
        self.error_message = error_message
    def __call__(self, value):
        # validaciones mínimas
        print value
        if ',' in str(value):
            return (value,self.error_message)
            
        return (value, None)
        
    def formatter(self, value):
        return value

db.define_table("cliente",
    Field("id_cliente","id"),
    Field("condicion_frente_al_iva","string",label="Condición frente al IVA"),
    Field("nombre_de_fantasia","string",label="Nombre de Fantasía"),
    Field("razon_social","string",label="Razón Social"),
   
    Field("dni","string",label="D.N.I."),
    Field("tipo_factura",label="Tipo de Factura"),
    Field("direccion","string",label="Dirección"),
    Field("numero","string",label="Número"),
    Field("localidad","string"),
    Field("telefono","string",label="Teléfono"),
    Field("email","string",label="E-Mail"),
)
#################Validaciones de Cliente##################

db.cliente.condicion_frente_al_iva.requires=IS_IN_SET(["Responsable Inscripto","Consumidor Final"],error_message='Seleccione una opción' )
db.cliente.tipo_factura.requires=IS_IN_SET(["A","B"],error_message='Seleccione una opción' )
db.cliente.dni.requires=[IS_NOT_EMPTY(error_message='Complete el campo'),
			IS_NOT_IN_DB(db,"cliente.dni",error_message='DNI ya existe')]
db.cliente.telefono.requires=IS_NOT_EMPTY(error_message='Complete el campo')
db.cliente.direccion.requires=IS_NOT_EMPTY(error_message='Complete el campo')
db.cliente.numero.requires=IS_NOT_EMPTY(error_message='Complete el campo')
db.cliente.localidad.requires=IS_NOT_EMPTY(error_message='Complete el campo')
db.cliente.razon_social.requires=IS_NOT_EMPTY(error_message='Complete el campo')

#################TABLA PROVEEDOR##################
db.define_table("proveedor",
      Field("id_proveedor", "id"),
      Field("razon_social", 'string',label="Razón Social"),
      Field("ingreso_bruto", 'string',label="Ingresos Brutos"),
      Field("condicion_iva", 'string',label="Condición Frente al IVA"),
      
      Field("domicilio", 'string',label="Domicilio"),
      Field("localidad", 'string',label="Localidad"),
      Field("codigo_postal", 'integer',label="Código Postal"),
      Field("provincia", 'string',label="Provincia"),
      Field("pais", 'string',label="País"),
      Field("telefono", 'string',label="Teléfono"),
      Field("celular", 'string',label="Celular"),
      Field("email_proveedor", 'string',label="Email"),
      Field("pagina_web", 'string',label="Página Web"),
      format='%(razon_social)s %(id_proveedor)s )',
    )
db.proveedor.condicion_iva.requires=IS_IN_SET(["Responsable Inscripto","Monotributista"],error_message='Seleccione una opción' )

db.proveedor.cuit.requires=[IS_NOT_EMPTY(error_message='Complete el campo'),
                           IS_CUIT()]

db.proveedor.ingreso_bruto.requires=[IS_NOT_EMPTY(error_message='Complete el campo'),
						             IS_NOT_IN_DB(db,"proveedor.ingreso_bruto",error_message='El número de Ingresos Brutos ya existe'), 
                                     IS_CUIT()]

db.proveedor.razon_social.requires=[IS_NOT_EMPTY(error_message='Complete el campo'),
                                    IS_NOT_IN_DB(db,"proveedor.razon_social",error_message='Razón Social ya existe')]

db.proveedor.domicilio.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.localidad.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.codigo_postal.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.provincia.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.pais.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.telefono.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.celular.requires=IS_NOT_EMPTY(error_message='Complete el campo')

db.proveedor.email_proveedor.requires=[IS_NOT_EMPTY(error_message='Complete el campo'),
                                       IS_EMAIL(error_message='La casilla de e-mail no tiene el formato correcto'),
                                       IS_NOT_IN_DB(db,"proveedor.email_proveedor",error_message='El e-mail ya existe')]

db.proveedor.pagina_web.requires=IS_NOT_EMPTY(error_message='Complete el campo')

################################################################################################################################



db.define_table("producto",
    Field("id_producto","id"),
    Field("detalle_producto","string"),
   
    Field("precio_compra","float"),
    Field("precio_venta","float"),
    Field("alicuota_iva","float"),
    Field("marca","string"),
    Field("categoria","string"),
)


db.producto.categoria.requires=IS_IN_SET(["Hardware","Software"])
db.producto.alicuota_iva.requires=IS_IN_SET({10.5: "10.5%",21: "21%"})
db.producto.id_producto.requires=IS_NOT_EMPTY()
db.producto.id_producto.requires=IS_NOT_IN_DB(db,"producto.id_producto")
db.producto.detalle_producto.requires=IS_NOT_EMPTY()
db.producto.precio_venta.requires=IS_NOT_COMA(error_message="No ingresar con coma")
db.producto.precio_compra.requires=IS_NOT_COMA(error_message="No ingresar con coma")
