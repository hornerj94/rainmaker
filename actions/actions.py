
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from weather import getWeatherData

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
            if selection == "Temperatur":
                message = "Die aktuelle Temperatur in {} ist {} Grad Celsius."                
                response = message.format(location, data['main']['temp'])
            elif selection == "Windgeschwindigkeit":
                velocityKilometerPerHour = self.getWindVelocityInKmH(
                    data['wind']['speed'])

                message = "Die aktuelle Windgeschwindigkeit in {} ist {} " \
                     + "km/h. Das entspricht eine" \
                     + self.getWindVelocityTitle(velocityKilometerPerHour) \
                     + "."          
                response = message.format(location, velocityKilometerPerHour)
            elif selection == "Luftfeuchtigkeit":
                message = "Die aktuelle Luftfeuchtigkeit in {} ist {} %."                
                response = message.format(location, data['main']['humidity'])
            elif selection == "Wetter":
                messages = list()
                messages.append("Wetterbericht für " + location)
                messages.append("Temperatur" + "\n"
                    "Aktuell " + str(data['main']['temp']) + " °C" + "\n"
                    "Gefühlt " + str(data['main']['feels_like']) + " °C" + "\n"
                    "Minimal " + str(data['main']['temp_min']) + " °C" + "\n"
                    "Maximal " + str(data['main']['temp_max']) + " °C")
                messages.append("Luftfeuchtigkeit " \
                    + str(data['main']['humidity']) + " %")

                velocityKilometerPerHour = self.getWindVelocityInKmH(
                    data['wind']['speed'])
                messages.append("Windgeschwindigkeit " \
                    + str(velocityKilometerPerHour) + " km/h"  + "\n" \
                    + "Das entspricht eine" \
                    + self.getWindVelocityTitle(velocityKilometerPerHour))

                for i in messages:         
                    dispatcher.utter_message(text=i)
                
                print("http://openweathermap.org/img/wn/" \
                        + data['weather'][0]['icon'] + "@2x.png")

                dispatcher.utter_message(
                    image = "http://openweathermap.org/img/wn/" \
                        + data['weather'][0]['icon'] + "@2x.png")
                
                response = data['weather'][0]['description']
                
        dispatcher.utter_message(text=response)

        return [SlotSet('location', location), SlotSet('selection', None)]

#------------------------------------------------------------------------------

    def getWindVelocityInKmH(self, velocityMeterPerSecond: int) -> int:
        velocityMeterPerSecond = velocityMeterPerSecond
        velocityMeterPerHour = velocityMeterPerSecond * 60 * 60

        return round(velocityMeterPerHour / 1000)

#------------------------------------------------------------------------------

    def getWindVelocityTitle(self, velocityKilometerPerHour: int) ->  str:
        if velocityKilometerPerHour < 1:
            return "r Windstille"
        elif velocityKilometerPerHour >= 1 and velocityKilometerPerHour < 6:
            return "m leisen Zug"
        elif velocityKilometerPerHour >= 6 and velocityKilometerPerHour < 12:
            return "r leichten Brise"
        elif velocityKilometerPerHour >= 12 and velocityKilometerPerHour < 20:
            return "m schwachen Wind"
        elif velocityKilometerPerHour >= 20 and velocityKilometerPerHour < 29:
            return "m mäßigen Wind"
        elif velocityKilometerPerHour >= 29 and velocityKilometerPerHour < 39:
            return "m frischen Wind"
        elif velocityKilometerPerHour >= 39 and velocityKilometerPerHour < 50:
            return "m starken Wind"
        elif velocityKilometerPerHour >= 50 and velocityKilometerPerHour < 62:
            return "m steifen Wind"
        elif velocityKilometerPerHour >= 62 and velocityKilometerPerHour < 75:
            return "m stürmischen Wind"
        elif velocityKilometerPerHour >= 75 and velocityKilometerPerHour < 89:
            return "m Sturm"
        elif velocityKilometerPerHour >= 89 and velocityKilometerPerHour < 103:
            return "m schweren Sturm"
        elif velocityKilometerPerHour >= 103 and velocityKilometerPerHour < 118:
            return "m orkanartigen Sturm"
        elif velocityKilometerPerHour >= 118:
            return "m Orkan"
            
#------------------------------------------------------------------------------