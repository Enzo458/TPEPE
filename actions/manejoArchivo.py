import json
import os
import csv
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
        try:
            with open (dire) as archivo:
                dict= csv.DictReader(archivo)
                tareaDis= None
                for row in dict:
                    if(row["responsable"] is None):
                        tareaDis= row
            return tareaDis
        except FileNotFoundError:
            return None

def tareaBuscar(dire, id)-> dict:
        try:
            with open (dire) as archivo:
                dict= csv.DictReader(archivo)
                tareaDis= None
                for row in dict:
                    if(row["idTarea"] == id):
                        tareaDis= row
            return tareaDis
        except FileNotFoundError:
            return None

def guardarTarea(dire, id, dicc):
        tareas = pd.read_csv(dire)
        try: 
            tareas.loc[tareas["idTarea"] == id] = dicc
            tareas.to_csv(dire)
        except KeyError:
            return None            