from tkinter import * 
from tkinter import ttk,messagebox as mb, Toplevel, Frame
from tkcalendar import DateEntry
import tkinter as tk
import psycopg2
from dbSeries import Series



class admSeries(tk.Tk):

    series=Series()
    
#----------------FUNCIONES-----------------    
    
    #FUNCION PARA REALIZAR BUSQUEDA
    def fBuscar(self):
        
            datos=(self.buscarCarga.get())
            respuesta=self.series.fBuscar_serie(datos)
            if len(respuesta)>0:
                self.txtTitulo.set(respuesta[0][0])
                #self.descripcionCarga.set(respuesta[0][1])
                #self.generoCarga.set(respuesta[0][2])
                #self.precioCarga.set(respuesta[0][3])
                #self.estrellasCarga.set(respuesta[0][4])
                #self.fechaCarga.set(respuesta[0][5])
                #self.atpCarga.set(respuesta[0][6])
                
            else:
                self.txtTitulo.set('')
                #self.descripcionCarga.set('')
                #self.generoCarga.set('')
                #self.precioCarga.set('')
                #self.estrellasCarga.set('')
                #self.fechaCarga.set('')
                #self.atpCarga.set('')
                
                mb.showinfo("Información", "No existe un artículo con dicho código")

    #FUNCION PARA GUARDAR DATOS DE SERIE
    def fGuardar(self): 
        if self.id ==-1:       
            self.series.fInsertar_serie(self.txtTitulo.get(),self.txtDescripcion.get(),self.box_value.get(), self.decPrecio.get(), self.varfecha.get(),self.spEstrellas.get(),self.atp.get())     
            mb.showinfo("Insertar", 'Elemento agregado correctamente.')
            self.habilitarBtn("normal")
            self.limpiarGrid()
            self.listar() 
        else:
            self.series.fMod_serie(self.id,self.txtTitulo.get(),self.txtDescripcion.get(),self.box_value.get(), self.decPrecio.get(), self.varfecha.get(),self.spEstrellas.get(),self.atp.get())
            mb.showinfo("Modificar", 'Elemento modificado correctamente.')
            self.id = -1 
            self.habilitarBtn("normal")           
            self.limpiarGrid()
            self.listar() 

    #FUNCION PARA MODIFICAR DATOS E SERIE
    def fModificar(self): 
        self.nueva_serie()      
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            mb.showwarning("Modificar", 'Debes seleccionar un elemento.')            
        else:            
            self.id= clave                         
            valores = self.grid.item(selected,'values')          
            self.txtTitulo.insert(0,valores[0])
            self.txtDescripcion.insert(0,valores[1])
            self.box_value.insert(0,valores[2])
            self.decPrecio.insert(0,valores[3])  
            self.varfecha.insert(0,valores[4])          
            self.spEstrellas.insert(0,valores[5])
            self.atp.insert(0,valores[6])
            self.txtTitulo.focus()

    #FUNCION PARA LIMPIAR TABLA
    def limpiarGrid(self):

        for item in self.grid.get_children():
            self.grid.delete(item)

    #FUNCION PARA BOTONES "CANCELAR"
    def fCancelar(self):
        r = mb.askquestion("Cancelar", "¿Esta seguro que desea cancelar la operación actual?")
        if r == mb.YES: 
            self.habilitarBtn("normal")
            self.agregar_serie.destroy()
            self.vbuscar.destroy()
            
    #FUNCION PARA LLENAR TABLA
    def listar(self):
        datos = self.series.fCons_serie()
        for row in datos:
            self.grid.insert("",END,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
                    
        if len(self.grid.get_children())>0:
            self.grid.selection_set(self.grid.get_children()[0])
    
    #FUNCION PARA HABILITAR/DESHABILITAR BOTONES DEL MENU PRINCIPAL
    def habilitarBtn(self,estado):
        self.btnAgregar.configure(state=estado)                
        self.btnModificar.configure(state=estado)
        self.btnBuscar.configure(state=estado)
            
    #FUNCION PARA ELIMINAR DATOS
    def borrar(self):

        selected= self.grid.focus()
        clave = self.grid.item(selected,"text")

        if clave == '':
                mb.showwarning("Error","Debes seleccionar un elemento")
                                        
        else:
                valores= self.grid.item(selected,'values')
                data= valores[0]
                n= self.series.fElim_serie(clave)
                r= mb.askquestion("Eliminar", "Desea eliminar el elemento seleccionado: "+ data)

                if r== mb.YES:
                        
                        n= self.series.fElim_serie(clave)
                        if n == 1:
                            mb.showwarning("Error", "No fue posible realizar la eliminacion")
                           
                        else:
                            mb.showinfo("Exito","Eliminacion realizada con exito")
                            self.limpiarGrid()
                            self.listar()
        """selected= self.grid.focus()
        id = self.grid.item(selected,"text")
        cantidad=self.baja(id)
        if cantidad==1:
            mb.showinfo("Información", "Se borró el artículo con dicho código")
        else:
            mb.showinfo("Información", "No existe un artículo con dicho código") """      

    #FUNCION PARA BOTON "SALIR" DEL MENU PRINCIPAL
    def btSalir(self):
        self.vbuscar.destroy()
        self.menuprincipal.destroy()     

    #FUNCION PARA ANULAR SERIE
    def fAnular(self):
        selected = self.grid.focus()                               
        clave = self.grid.item(selected,'text')        
        if clave == '':
            mb.showwarning("Modificar", 'Debes seleccionar un elemento.')            
        else:
            self.id=clave             
            self.series.fAnular()
            self.listar()

            
#--------------INTERFAZ--------------

    #VENTANA DE LOGIN
    def __init__(self, *args, **kwargs):

        self.cnn= psycopg2.connect(host="localhost", user="postgres",password="39142048",database="DBSeries")
        super().__init__(*args, **kwargs)       
        self.title("Inicio de sesion")
        self.config(width=350, height=350, bg="#1C7AE4")
        self.resizable(0,0)
        self.iconbitmap("logo.ico")
        self.id=-1
    
        #ENTRADAS
        lblHost= Label(self, text="Servidor/Host: ",bg="#1C7AE4", fg="white", font=("Times",12))
        lblHost.place(x=60, y=120)

        
        self.txtHost= Entry(self,borderwidth=2, font=("Times",12))
        self.txtHost.insert(0,"localhost")
        self.txtHost.place(x=160, y=120, height=25, width=130)
      

        lblUsuario= Label(self, text="Usuario: ",bg="#1C7AE4", fg="white", font=("Times",12))
        lblUsuario.place(x=95, y=160)

        
        self.txtUsuario= Entry(self,borderwidth=2, font=("Times",12))
        self.txtUsuario.insert(0,"postgres")
        self.txtUsuario.place(x=160, y=160, height=25, width=130)
    

        lblContraseña= Label(self, text="Contraseña: ",bg="#1C7AE4", fg="white", font=("Times",12))
        lblContraseña.place(x=75, y=200)

        self.txtContraseña= Entry(self,show="*",borderwidth=2, font=("Times",12))
        self.txtContraseña.insert(0,"39142048")
        self.txtContraseña.place(x=160, y=200, height=25, width=130)


        lblDB= Label(self, text="Base de datos: ",bg="#1C7AE4", fg="white", font=("Times",12))
        lblDB.place(x=60, y=240)

        
        self.txtDB= Entry(self,borderwidth=2, font=("Times",12))
        self.txtDB.insert(0,"DBseries")
        self.txtDB.place(x=160, y=240, height=25, width=130)
       
        #photo= PhotoImage(file= r"C:\Users\niko-\Desktop\Nueva carpeta\Add.png")
        #photoimage= photo.subsample(3,3)
        #BOTONES
        btnConectar = Button(self,text="Conectar",command=self.menup, bg="green", fg="white", borderwidth=3, font=("Times",12))
        btnConectar.place(x=60, y=290, width=100, height=30)


        btnSalir = Button(self,text="Salir", command=lambda:quit(), bg="red", fg="white", borderwidth=3, font=("Times",12))
        btnSalir.place(x=200, y=290, width=100, height=30)

    #VENTANA DE MENU PRINCIPAL
    def menup(self):

        self.menuprincipal=tk.Tk() 
        self.menuprincipal.title("Administrador de series")
        self.menuprincipal.config(width=800, height=450, bg="#1C7AE4")
        self.menuprincipal.resizable(0,0)
        self.menuprincipal.iconbitmap("logo.ico")
        self.destroy()
        
        
        label = Label(self.menuprincipal, text ="¡Bienvenido al administrador de series!", fg="white", bg="#1C7AE4", font=(20))
        label.place(x=15, y=5)  

        
        self.btnAgregar = Button(self.menuprincipal,text="Agregar",command=self.nueva_serie, activebackground="white", bg="white", fg="black")
        self.btnAgregar.place(x=20, y=410, width=80)

        self.btnModificar = Button(self.menuprincipal,text="Modificar",command=self.fModificar, activebackground="white", bg="white", fg="black")
        self.btnModificar.place(x=120, y=410, width=80) 

        btnEliminar = Button(self.menuprincipal,text="Eliminar",command=self.borrar, activebackground="white", bg="white", fg="black")
        btnEliminar.place(x=220, y=410, width=80)

        self.btnBuscar = Button(self.menuprincipal,text="Buscar",command=self.buscador, activebackground="white", bg="white", fg="black")
        self.btnBuscar.place(x=710, y=10, width=80) 

        btnAnular = Button(self.menuprincipal,text="Anular",command=self.fAnular, activebackground="white", bg="white", fg="black")
        btnAnular.place(x=320, y=410, width=80)

        btnSalir = Button(self.menuprincipal,text="Salir", command=self.btSalir, activebackground="white", bg="red", fg="white")
        btnSalir.place(x=710,y=410, width=80)

           
    #TABLA
        self.frame = Frame(self.menuprincipal,bg="#1C7AE4")
        self.frame.place(x=20,y=50,width=765, height=345) 
        self.grid=ttk.Treeview(self.frame,columns=("col1","col2","col3","col4","col5","col6","col7","col8"))
        self.grid.place(x=20,y=50,width=765,height=345)
                            
        self.grid.column("#0",width=40)
        self.grid.column("col1",width=135,anchor=CENTER)
        self.grid.column("col2",width=190,anchor=CENTER)
        self.grid.column("col3",width=90,anchor=CENTER)
        self.grid.column("col4",width=70,anchor=CENTER)
        self.grid.column("col5",width=70,anchor=CENTER)
        self.grid.column("col6",width=50,anchor=CENTER)
        self.grid.column("col7",width=50,anchor=CENTER)
        self.grid.column("col8",width=53,anchor=CENTER)
        self.grid.heading("#0",text="ID",anchor=CENTER)
        self.grid.heading("col1",text="Titulo",anchor=CENTER)
        self.grid.heading("col2",text="Descripcion",anchor=CENTER)
        self.grid.heading("col3",text="Genero",anchor=CENTER)
        self.grid.heading("col4",text="Precio",anchor=CENTER)
        self.grid.heading("col5",text="Fecha de estreno",anchor=CENTER)
        self.grid.heading("col6",text="Estrellas",anchor=CENTER)
        self.grid.heading("col7",text="Estado",anchor=CENTER)
        self.grid.heading("col8",text="ATP",anchor=CENTER)
        self.grid.pack(side=LEFT,fill = Y)        
        sb = Scrollbar(self.frame, orient=VERTICAL)
        sb.pack(side=RIGHT, fill = Y)
        self.grid.config(yscrollcommand=sb.set)
        sb.config(command=self.grid.yview)
        self.grid['selectmode']='browse'    

        self.listar()

    #VENTANA DEL BUSCADOR
    def buscador(self):
            self.vbuscar =tk.Tk() 
            self.vbuscar.title("Buscar") 
            self.vbuscar.config(width=300, height=150, bg="#1C7AE4")
            self.vbuscar.resizable(0,0)
            self.vbuscar.iconbitmap("pragma.ico")
            self.habilitarBtn("disabled")
                
            #BOTONES
            boton_cancelar = Button(self.vbuscar,text="Cancelar",command=self.fCancelar, bg="red", fg="white")
            boton_cancelar.place(x=200, y=100)

            self.boton_guardar = Button(self.vbuscar,text="Buscar",command=self.fBuscar, bg="green", fg="white")
            self.boton_guardar.place(x=100, y=100)


            #ENTRADAS
            self.lblTitulo= Label(self.vbuscar,text="Titulo: ", bg="#1C7AE4")
            self.lblTitulo.place(x=15, y=30, width=50)

            self.buscarCarga=tk.StringVar()
            self.txtbuscar = ttk.Entry(self.vbuscar, textvariable=self.buscarCarga)
            self.txtbuscar.place(x=100, y=30, width=150)
            self.txtbuscar.focus_set()
            
    #VENTANA DE AGREGAR/MODIFICAR SERIE
    def nueva_serie(self):
                            
            self.agregar_serie = tk.Tk() 
            self.agregar_serie.title("Agregar serie nueva") 
            self.agregar_serie.config(width=700, height=350, bg="#1C7AE4")
            self.agregar_serie.resizable(0,0)
            self.agregar_serie.iconbitmap("pragma.ico")
            self.agregar_serie.focus()
            self.habilitarBtn("disabled")
            
                
            #BOTONES
            boton_cancelar = Button(self.agregar_serie,text="Cancelar",command= self.fCancelar, bg="red", fg="white")
            boton_cancelar.place(x=600, y=310, width=80)

            boton_guardar = Button(self.agregar_serie,text="Guardar", command=self.fGuardar, bg="green", fg="white")
            boton_guardar.place(x=500, y=310, width=80)


            #ENTRADAS
            self.lblTitulo= Label(self.agregar_serie,text="Titulo: ",bg="#1C7AE4", font=("Times",11))
            self.lblTitulo.place(x=30, y=30, width=100)
            #
            self.txtTitulo = ttk.Entry(self.agregar_serie)
            self.txtTitulo.place(x=100, y=30, width=500,height=25)
            self.txtTitulo.focus_set()


            
            self.lblDescripcion= Label(self.agregar_serie,text="Descripcion: ",bg="#1C7AE4", font=("Times",11))
            self.lblDescripcion.place(x=10, y=70, width=100)
            #self.descripcionCarga=tk.StringVar()
            self.txtDescripcion = tk.Text(self.agregar_serie, padx=5,pady=5, borderwidth=2)
            self.txtDescripcion.place(x=100, y=70, width=500, height=140)



            self.lbGenero= Label(self.agregar_serie,text="Genero: ",bg="#1C7AE4", font=("Times",12))
            self.lbGenero.place(x=200, y=240, width=100)
            self.box_value=tk.StringVar()
            self.cmbGenero = ttk.Combobox(self.agregar_serie, state="readonly",textvariable=self.box_value, values=["Accion","Animada","Ciencia ficcion","Comedia","Drama","Policial","Terror"])
            self.cmbGenero.place(x=300, y=240,width=100)


            
            self.lblPrecio= Label(self.agregar_serie,text="Precio: ",bg="#1C7AE4")
            self.lblPrecio.place(x=15, y=240, width=100)
            validate_entry= lambda text: text.isdecimal()
            self.decPrecio = ttk.Entry(self.agregar_serie,validate="key", validatecommand=(self.agregar_serie.register(validate_entry),"%S"))
            self.decPrecio.place(x=100, y=240, width=50)
            


            self.lblEstrellas= Label(self.agregar_serie,text="Estrellas: ",bg="#1C7AE4")
            self.lblEstrellas.place(x=15, y=290, width=100)
            #self.estrellasCarga= tk.IntVar()
            self.spEstrellas = Spinbox(self.agregar_serie, from_ = 0, to = 5)
            self.spEstrellas.place(x=100, y=290, width=50)

  
            self.lblFechaEst= Label(self.agregar_serie,text="Fecha de estreno: ",bg="#1C7AE4")
            self.lblFechaEst.place(x=200, y=290, width=100)
            self.varfecha=tk.StringVar()
            self.calendario = DateEntry(self.agregar_serie, textvariable=self.varfecha, selectmode = 'day', 
                    year = 2020, month = 5, 
                    day = 22) 
            self.calendario.place(x=300, y=290) 

            
            self.atp=tk.IntVar()
            #self.atpCarga=tk.BooleanVar()
            self.cbATP= ttk.Checkbutton(self.agregar_serie, text="Apta para todo publico",variable=self.atp, onvalue=TRUE,offvalue=FALSE)
            self.cbATP.place(x=450, y=240, width=200)
            """self.lblEstado= Label(self.agregar_serie,text="Estado: ")
            self.lblEstado.place(x=10, y=130, width=100)

            self.txtEstado = Entry(self.agregar_serie)
            self.txtEstado.place(x=460, y=130, width=100)"""

                        
if __name__=='__main__':
    administrador= admSeries() 
    administrador.mainloop() 