
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from weather import getWeatherData

class CurrentTemperatureAction(Action):
#------------------------------------------------------------------------------
    def name(self) -> Text:
        return "current_temperature_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')

        data = getWeatherData(location)

        if data['cod'] != 200:
            message = "Für {} konnten keine Daten ermittelt werden."                
            response = message.format(location)
        else:
            mainData = data['main']

            message = "Die aktuelle Temperatur in {} ist {} Grad Celsius."                
            response = message.format(location, mainData['temp'])
            
        dispatcher.utter_message(response)
        
        return [SlotSet('location', location)]

#------------------------------------------------------------------------------

class WeatherAction(Action):
#------------------------------------------------------------------------------
    def name(self) -> Text:
        return "weather_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')

        data = getWeatherData(location)

        if data['cod'] != 200:
            message = "Für {} konnten keine Daten ermittelt werden."                
            response = message.format(location)
        else:
            selection = tracker.get_slot('selection')

            print(tracker.get_slot('selection'))
        
            mainData = data['main']

            if selection == "Wetter":        
                message = "Aktuelle Temperatur {}: {} Grad Celsius." + "\n" \
                    + "Gefühlte Temperatur: {} Grad Celsius." + "\n" \
                    + "Erwartete Minimaltemperatur: {} Grad Celsius." + "\n" \
                    + "Erwartete Maxmaltemperatur: {} Grad Celsius." + "\n"                
                response = message.format(location, mainData['temp'], \
                    mainData['feels_like'], mainData['temp_min'], mainData['temp_max'])
            elif selection == "Temperatur":
                message = "Die aktuelle Temperatur in {} ist {} Grad Celsius."                
                response = message.format(location, mainData['temp'])

        dispatcher.utter_message(response)

        return [SlotSet('location', location)]

#------------------------------------------------------------------------------