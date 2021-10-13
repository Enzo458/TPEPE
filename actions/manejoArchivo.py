import json
import os
import csv
import re
import pandas as pd
def leerArchivo(dire)-> dict:
        print(dire)
        try:
            with open (dire, "r") as archivo:
                dict= json.load(archivo)
                archivo.close()
            return dict
        except FileNotFoundError:
            return None

def escribirArchivo(dire, dicc)-> bool: 
        try:
            with open(dire, "w") as archivo:
                json.dump(dicc, archivo)
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

def guardarTarea(dire, id, dicc):
    df = pd.read_csv(dire, index_col=0,header=0)
    try:
        print(df.loc[df['idTarea']== id])
        df.loc[df['idTarea']== id, "resposable"] = dicc["responsable"]
        df.loc[df['idTarea']== id, "fecha_estimada"] = dicc["fecha_estimada"]
        df.to_csv(dire)
    except KeyError:
        print("ouch")
        pass