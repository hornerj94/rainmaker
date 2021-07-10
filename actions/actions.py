
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from weather import Weather

class WeatherAction(Action):

    def name(self) -> Text:
        return "weather_action"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot('location')
        temperature=Weather(city)['temp']
        response = "Die aktuelle Temperatur in {} ist {} Grad Celsius.".format(city,temperature)
        
        dispatcher.utter_message(response)

        return [SlotSet('location',city)]