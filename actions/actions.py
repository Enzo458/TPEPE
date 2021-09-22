# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
import os
from os import name
from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionHelloWorld(Action):
#
     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")
        
        return []


class ActionInfoEmpledo(Action):
#
     def name(self) -> Text:
         return "action_info_empleado"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            direccionArch= os.getcwd() +"\\recursos\\empleados\\" + next(tracker.get_latest_entity_values("idEmpleado"), None) + ".json"
            dicc= leerArchivo(direccionArch)
            dispatcher.utter_message(dicc["nombre"])
        
            return []


def leerArchivo(dire)-> dict:
        with open (dire, "r") as archivo:
            dict= json.load(archivo)
            archivo.close()
        return dict

def escribirArchivo(dire, dicc): 
        with open(dire, "w") as archivo:
            json.dump(dicc, archivo)
            archivo.close()
