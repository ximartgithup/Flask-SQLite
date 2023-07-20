import os
from flask import Flask, render_template, request
#importar el sqlite3 para el manejo de BD
import sqlite3
#importar el modulo de errores de sqlite3
from sqlite3 import Error
from forms import Producto
app= Flask(__name__)

app.secret_key = os.urandom( 24 ) #generamos la clave aleatoria

@app.route('/')
def index():
    return '<h1> Bienvenido </h1>'
#;;;;;;;;;;;;;;;;;;;;;;;,;;; Rutas;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
@app.route('/productos/')
def productos(): 
  productos = sql_select_productos()
  return render_template('products.html', productos = productos)

@app.route('/nuevo/', methods=['GET', 'POST'])
def nuevo():
   if  request.method == "GET": #Si la ruta es accedida a través del método GET entonces
        form = Producto() #Crea un nuevo formulario de tipo producto
        return render_template('nuevo.html', form=form) #redirecciona vista nuevo.html enviando la variable form
   if  request.method == "POST": #Si la ruta es accedida a través del método POST entonces
        cod = request.form["codigo"] #asigna variable cod con valor enviado desde formulario  en la vista html
        nom = request.form["nombre"] #asigna variable nom con valor enviado desde formulario en la vista html
        cant = request.form["cantidad"] #asigna vble cant con valor enviado desde formulario en la vista html
        guardar_productos(cod, nom, cant) #llamado de la función para insertar el nuevo producto
        return "Guardado correctamente"
   else:
         return "error de direccionamiento!"    

    

#-----------------------------
@app.route('/edit', methods=['GET'])
def editar_producto():
    id = request.args.get('id') #captura de la variable id enviada a través de la URL
    codigo = request.args.get('codigo') #captura de la vble código enviada a través de la URL
    nombre = request.args.get('nombre') #captura de la vble nombre enviada a través de la URL
    cantidad = request.args.get('cantidad') #captura de la vble cantidad enviada a través de la URL
    sql_edit_producto(id, codigo, nombre, cantidad) #llamado de la función de edición de la base de datos
    return "OK"

@app.route('/delete', methods=['GET'])
def borrar_producto():
	id = request.args.get('id') #captura de la variable id enviada a través de la URL
	sql_delete_producto(id) #llamado a la función de borrado de la base de datos
	return "OK"

#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; Rutas;;;;;;;;;;;;;;;;;;;;;;;;;;
#============== conexion ala BD======================
def Conexion():
    try:
        con=sqlite3.connect('DB/mydatabase.db')
        return con
    except Error:
        print(Error)

#=====Guardar productos================
def guardar_productos(codigo,nombre,cantidad):
        sql="Insert into productos (codigo,nombre, cantidad) values('"+codigo+"','"+nombre+"',"+cantidad+");"
        con=Conexion()
        cursorObj=con.cursor() # que es?
        cursorObj.execute(sql)
        con.commit()
        con.close()
#endGuardar
#--------- Para listar los productos-------------
def sql_select_productos():
        strsql = "select * from productos;"
        con = Conexion()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        productos = cursorObj.fetchall()
        return productos
#-------------- Para editar un producto--------------        
def sql_edit_producto(id, codigo, nombre, cantidad):
      strsql = "update productos set codigo = '"+codigo+"', nombre = '"+nombre+"',  	cantidad = "+cantidad+" where id = "+id+";"
      con = Conexion()
      cursorObj = con.cursor()
      cursorObj.execute(strsql)
      con.commit()
      con.close()
#-------------- Para Eliminar un producto--------------        
def sql_delete_producto(id):
        strsql = "delete from productos where id = "+id+";"
        con = Conexion()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        con.commit()
        con.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)