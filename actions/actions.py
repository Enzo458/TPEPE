# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import datetime
import os
import re
import actions.manejoArchivo as manejoArchivo
from os import name
from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

FALTASANUALESMAX= 24


class ActionInfoEmpledo(Action):
#
     def name(self) -> Text:
         return "action_info_empleado"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            direccionArch= os.getcwd() +"\\recursos\\empleados\\" + next(tracker.get_latest_entity_values("idEmpleado"), None) + ".json"
            dicc= manejoArchivo.leerArchivo(direccionArch)
            if(dicc is None):
                dispatcher.utter_message("idEmpleado incorrecto")
                return [SlotSet("identificadorEmpleado", None)]
            else:
                dispatcher.utter_message("Nombre:"+str(dicc["nombre"])+"\n"+ 
                    "IdEmpleado: "+str(dicc["idEmpleado"])+"\n"+ 
                    "Faltas: "+str(dicc["faltas"])+"\n"+ 
                    "Turno: "+str(dicc["turno"])+"\n" 
                    "Tareas: "+str(dicc["tareas_momento"])+"\n")
                return [SlotSet("identificadorEmpleado", str(dicc["idEmpleado"]))]
            

class registrarNotificacionDeAusencia(Action):
     def name(self)-> Text:
         return "action_registar_notificacion_falta"
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any])-> List[Dict[Text, Any]]:
            idEmpleado= tracker.get_slot("identificadorEmpleado")
            mensaje= "empleado no identificado"
            if(idEmpleado is not None):
                direccion= str(os.getcwd()) +"\\recursos\\empleados\\" + idEmpleado+ ".json"
                empleado= manejoArchivo.leerArchivo(direccion)
                date= datetime.datetime.now()
                empleado["faltas"].append(str(date.day)+"/"+str(date.month)+"/"+str(date.year))
                faltasEmp= empleado["faltas"]
                faltasAnuales= len(re.findall(str(date.year),str(empleado["faltas"])))
                if(faltasAnuales > FALTASANUALESMAX):
                    dispatcher.utter_message(
                        template= "utter_faltas_sansion",
                        nroFaltas = faltasAnuales
                    )
                else:
                    if(faltasAnuales > FALTASANUALESMAX * 0.6):
                        dispatcher.utter_message(
                            template= "utter_faltas_aviso_exceso",
                            nroFaltas= faltasAnuales
                        )
                    else:
                        dispatcher.utter_message(
                            template= "utter_faltas_registrada",
                            name= empleado["nombre"],
                            nroFaltas= faltasAnuales
                        )
                manejoArchivo.escribirArchivo(direccion,empleado)
            return[]


class ActionPedirTiempo(Action):
     def name(self) -> Text:
         return "action_pedir_tiempo"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        idEmpleado= tracker.get_slot("identificadorEmpleado")
        mensaje= "empleado no identificado"
        if(idEmpleado is not None):
            direccion= str(os.getcwd()) +"\\recursos\\empleados\\" + lista_empleados+ ".json"
            empleado= manejoArchivo.leerArchivo(direccion)
            tareas_momen = len(str(empleado["tareas_momento"]))
            if (tareas_momen > 2):
                dispatcher.utter_message(
                        template= "utter_tarea_pedida_negativa"
                )
            else:
                 dispatcher.utter_message(
                     template= "utter_tarea_pedida_positiva"
                 )
        return [SlotSet("identificadorEmpleado", str(empleado["idEmpleado"]))]


class ActionPedirTarea(Action):
    def name(self) -> Text:
        return "action_proponer_tarea"
    
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        idEmpleado= tracker.get_slot("identificadorEmpleado")
        mensaje= "empleado no identificado"
        if(idEmpleado is not None):
                direccionE= str(os.getcwd()) +"\\recursos\\empleados\\" + idEmpleado+ ".json"
                empleado= manejoArchivo.leerArchivo(direccionE)
                date= datetime.datetime.now()
                direcionT= os.getcwd() +"\\recursos\\tareas\\tareas" + ".csv"
                tareaProp= manejoArchivo.tareaSinRes(direcionT)
                if(tareaProp is None):
                    dispatcher.utter_message(
                        template= "utter_tareas_error",
                        nombre= empleado["nombre"],
                        motivo= "no hay tareas para asignar"
                    )
                else:
                    if(len(empleado["tareas_momento"])>= 3):
                     dispatcher.utter_message(
                        template= "utter_tareas_error",
                        nombre= empleado["nombre"],
                        motivo= "no es posible asignar mas tareas, termina tus tareas ya asignadas"
                        )
                    else:
                        dispatcher.utter_message(
                            template= "utter_proponer_tarea",
                            name= empleado["nombre"],
                            desTarea= tareaProp["descripcion"]
                        )
                        return[SlotSet("idTarea", str(tareaProp["idTarea"]))]
        return[]


class ActionConfirmarTarea(Action):
    def name(self) -> Text:
        return "action_confirmar_tarea"
    
    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        idEmpleado= tracker.get_slot("identificadorEmpleado")
        idTareaProp= tracker.get_slot("idTarea")
        direccionE= str(os.getcwd()) +"\\recursos\\empleados\\" + idEmpleado+ ".json"
        empleado= manejoArchivo.leerArchivo(direccionE)
        date= datetime.datetime.now()
        direcionT= os.getcwd() +"\\recursos\\tareas\\tareas" + ".csv"
        tareaProp= manejoArchivo.tareaBuscar(direcionT,idTareaProp)
        empleado['tareas_momento'].append(tareaProp["idTarea"])        
        tareaProp['responsable']=empleado["idEmpleado"]
        tareaProp['fecha_inicio']=str(date.day)+"/"+str(date.month)+"/"+str(date.year)
        fechaestimada= date + datetime.timedelta(days=int(tareaProp['fecha_estimada']))
        tareaProp['fecha_estimada']=str(fechaestimada.day)+"/"+str(fechaestimada.month)+"/"+str(fechaestimada.year)
        manejoArchivo.guardarTarea(direcionT,idTareaProp,tareaProp)
        manejoArchivo.escribirArchivo(direccionE,empleado)
        dispatcher.utter_message(
                        template= "utter_tareas_cofirmar_asignacion",
                        nombre= empleado["nombre"],
                        nombreTarea= tareaProp["nombre"],
                        fechaEstimada= tareaProp["fecha_estimada"]
                        )
        return[]
        