# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
import os
import datetime
from os import name
from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionInfoEmpledo(Action):
#
     def name(self) -> Text:
         return "action_info_empleado"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            direccionArch= os.getcwd() +"\\recursos\\empleados\\" + next(tracker.get_latest_entity_values("idEmpleado"), None) + ".json"
            dicc= leerArchivo(direccionArch)
            if(dicc is None):
                dispatcher.utter_message("idEmpleado incorrecto")
                return [SlotSet("identificadorEmpleado", None)]
            else:
                dispatcher.utter_message(dicc)
                return [SlotSet("identificadorEmpleado", str(dicc["idEmpleado"]))]
            

class registrarNotificacionDeAusencia(Action):
     def name(self)-> Text:
         return "action_registar_notificacion_falta"
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any])-> List[Dict[Text, Any]]:
            idEmpleado= tracker.get_slot("idEmpleado")
            mensaje= "empleado no identificado"
            if(idEmpleado is not None):
                direccion= os.getcwd() +"\\recursos\\empleados\\" + next(tracker.get_latest_entity_values("idEmpleado"), None) + ".json"
                dicc= leerArchivo(direccion)
                date= datetime.datetime.now()
                dicc["faltas"].append(str(date.day+"/"+date.month+"/"+date.year))
                mensaje= "tienes " + str(len(dicc["faltas"])) +" faltas acumuladas"
                escribirArchivo(direccion,dicc)
            dispatcher.utter_message(mensaje)
            return[]

def leerArchivo(dire)-> dict:
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

class ActionPedirTiempo(Action):
#
     def name(self) -> Text:
         return "action_pedir_tiempo"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        empleado= next(tracker.get_latest_entity_values("empleado"), None)
        message= "si"
        #ACA AGREGAR EL FUTURO ARCHIVO DE EMPLEADOS
        if str (empleado)== "Facundo":
            message=message+ "puede pedir un tiempo extra"

        dispatcher.utter_message(text=str(message))
        
        return [SlotSets("name", str(empleado))]
