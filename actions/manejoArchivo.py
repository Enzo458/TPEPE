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
        tareas = pd.read_csv(dire,index_col= 0)
        print(tareas)
        for tarea in tareas.to_dict('index'):
            print(tarea)
            dic = tarea
        return dic
        

def tareaBuscar(dire, id)-> dict:
        tareas = pd.read_csv(dire)
        try: 
            dic = tareas.loc[tareas["idTarea"] == id]
            return dic
        except KeyError:
            return None

def guardarTarea(dire, id, dicc):
        tareas = pd.read_csv(dire)
        try: 
            tareas.loc[tareas["idTarea"] == id] = dicc
            tareas.to_csv(dire)
        except KeyError:
            return None            