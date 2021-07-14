
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

        city = tracker.get_slot('location')

        data = getWeatherData(city)
        mainData = data['main']
        temperature = mainData['temp']
        response = "Die aktuelle Temperatur in {} ist {} Grad Celsius.".format(
            city,temperature)
        
        dispatcher.utter_message(response)

        return [SlotSet('location',city)]

#------------------------------------------------------------------------------