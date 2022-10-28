from tkinter import *
import psycopg2


class Series:

    def __init__(self):

        self.cnn= psycopg2.connect(host="localhost", user="postgres",password="39142048",database="DBSeries")
    
        
    
    def __str__(self):

        datos=self.fConsulta_serie()
        aux=""
        for row in datos:
            aux=aux + str(row) + "\n"
        return aux
    
    
    def fCons_serie(self):

        cur=self.cnn.cursor()
        cur.execute("SELECT * FROM series")
        datos = cur.fetchall()
        cur.close()
        return datos
    

    def fBuscar_serie(self,id):

        cur = self.cnn.cursor()
        sql= "SELECT * FROM Series WHERE id= {}".format(id)
        cur.execute(sql)
        datos = cur.fetchone()
        cur.close()
        return datos
    

    def fInsertar_serie(self,Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,Estado,ATP):

        cur= self.cnn.cursor()
        sql= '''INSERT INTO series(id,Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,Estado,ATP) 
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format (Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,Estado,ATP) 
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()
        cur.close()
        return n


    def fElim_serie(self,id):

        cur= self.cnn.cursor()
        sql= '''DELETE FROM series WHERE id= {}'''.format (id) 
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    
    
    
    
    def fMod_serie(self,id,Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,ATP):

        cur= self.cnn.cursor()
        sql= '''UPDATE series SET Titulo= '{}',Descripcion= '{}',Genero= '{}',Precio= '{}',Fecha_estreno= '{}',Estrellas= '{}',ATP= '{}', 
        WHERE id={}'''.format (Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,ATP,id) 
        cur.execute(sql)
        n=cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
    

    def fAnular_serie(self,Estado,id):
                
            cur= self.cnn.cursor()
            sql= '''UPDATE series SET Estado= 'AN'
            WHERE id={}'''.format (Estado,id) 
            cur.execute(sql)
            n=cur.rowcount
            self.cnn.commit()
            cur.close()
            return n

    
    """def alta(self,Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,ATP):
        #co=self.abrir()
        cursor=self.cnn.cursor()
        sql='''INSERT INTO series(Titulo, Descripcion, Genero, Precio, Estrellas, Fecha_estreno, ATP) VALUES ('{}','{}','{}','{}','{}','{}','{}')'''.format (Titulo,Descripcion,Genero,Precio,Fecha_estreno,Estrellas,ATP) 
        cursor.execute(sql)
        n=cursor.rowcount
        self.cnn.commit()    
        cursor.close()
        return n"""
   
