import json
import os
import csv
import re
import pandas as pd
def leerArchivo(dire,id)-> dict:
        print(dire)
        try:
            with open (dire, "r") as archivo:
                dict= json.load(archivo)
                dict= dict["lista_empleado"][id]
                archivo.close()
            return dict
        except FileNotFoundError:
            return None

def escribirArchivo(dire, dicc, id)-> bool: 
        try:
            with open(dire,"r")as arch:
                dict=json.load(arch)
                arch.close()
            with open(dire, "w") as archivo:
                dict["lista_empleado"][id]=dicc
                json.dump(dict, archivo)
                archivo.close()
                return True
        except FileNotFoundError:
            return False

def tareaSinRes(dire)-> dict:

    with open(dire) as csvfile:
        tareas = csv.DictReader(csvfile)
        for row in tareas:
            if(row['responsable']==""):
                dict = row

    return dict
        
        

def tareaBuscar(dire, id)-> dict:
        
    with open(dire) as csvfile:
        tareas = csv.DictReader(csvfile)
        for row in tareas:
            if(row['idTarea']==id):
                dict = row
    return dict

def guardarTarea(dire, id, dicc)-> bool:
    df= pd.read_csv(dire,index_col=0)
    try:
        df.loc[int(id),:]=dicc
        df.to_csv(dire)
        return True
    except KeyError:
        print("key error")
        return False