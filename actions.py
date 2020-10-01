# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from rasa.core.tracker_store import InMemoryTrackerStore

class GenerateLetter(Action) :

	def name(self) -> Text:
		return "generate_letter"

	def run(self,file_name, dispatcher:CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):

		# nimmt Musterschreiben-Dateiname und gibt Mustertext als String wieder
		def get_letter_text(file_name):
			return open(file_name,"r").read()

		# durchsucht txt-Datei nach Parametern mit {PARAMETER_NAME} als Form und gibt alle Parameternamen als Liste wieder
		def list_needed_slots(text):
			slots = []
			is_slot = False
			current_slot = []

			for char in text:
				if char == "{":
					is_slot = True

				if char == "}":
					is_slot = False
					slot = "".join(current_slot)
					slots.append(slot[1:])
					current_slot = []
				
				while is_slot == True:
					current_slot.append(char)
					break

			return slots


		# nimmt Liste an benötigten Parametern und gibt jeweilige Werte aus der Session wieder
		def get_session_data_from_memory(parameter):
			
			session_data = {}

			for i in range(len(parameter)):
				key = parameter[i]
				value = tracker.current_state()['slots'][key]

				session_data.update({key:value}) 

			return session_data

		# nimmt Mustertext, Parameterliste, und jeweilige Session-Werte und gibt fertig formuliertes Schreiben als String wieder
		def fill_in_session_data(text, slots, session_data):
			for slot in range(len(slots)):
				current_session_data = slots[slot]
				text = text.replace("{"+slots[slot]+"}", session_data[current_session_data])

			return text

		a = get_letter_text(file_name)
		b = list_needed_slots(a)
		c =	get_session_data_from_memory(b)


		dispatcher.utter_message("Dein fertiges " + file_name + " wird generiert...")
		dispatcher.utter_message(fill_in_session_data(a,b,c))

class CompanyForm(FormAction):

    def name(self):
        return "company_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "company_name",
            "privacy_email",
            ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"company_name": [self.from_entity(entity="company_name"),
                             self.from_text()],
                "privacy_email": [self.from_entity(entity="privacy_email"),
                             self.from_text()]}
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        dispatcher.utter_message("Vielen Dank für die Eingabe.")
        return []

class DeleteDataForm(FormAction):

    def name(self):
        return "delete_data_form"

    @staticmethod
    def required_slots(tracker):

        if tracker.get_slot('reason_for_deletion') == 'nicht_mehr_benötigt':
            return [
                "reason_for_deletion",
                ]
                # Call Einwilligungswiderrruf
        elif tracker.get_slot('reason_for_deletion') == 'unrechtmäßige_einwilligung':
                return [
                    "reason_for_deletion", #Welcher dieser Löschungsgründe könnte deiner Meinung nach infrage kommen? Was ist der Grund für die Datenlöschung?
                    "consent_given", # Hast du eine Einwilligung zur Datenverarbeitung erteilt?; Ja -> weiter, Nein -> Du kannst in jedem Fall deine Daten löschen, End form, Ich weiß nicht mehr -> Das Unternehmen muss den Nachweis erbringen, dass eine Einwilligung erfolgt ist.  Schau oder frage doch mal nach!....
                    ]
        elif tracker.get_slot('consent_given') == 'ja':
                return [
                    "reason_for_deletion", #Welcher dieser Löschungsgründe könnte deiner Meinung nach infrage kommen? Was ist der Grund für die Datenlöschung?
                    "consent_given", # Hast du eine Einwilligung zur Datenverarbeitung erteilt?; Ja -> weiter, Nein -> Du kannst in jedem Fall deine Daten löschen, End form, Ich weiß nicht mehr -> Das Unternehmen muss den Nachweis erbringen, dass eine Einwilligung erfolgt ist.  Schau oder frage doch mal nach!....
                    ]
        elif tracker.get_slot('consent_given') == 'nein':
                return [
                    "reason_for_deletion", #Welcher dieser Löschungsgründe könnte deiner Meinung nach infrage kommen? Was ist der Grund für die Datenlöschung?
                    "consent_given", # Hast du eine Einwilligung zur Datenverarbeitung erteilt?; Ja -> weiter, Nein -> Du kannst in jedem Fall deine Daten löschen, End form, Ich weiß nicht mehr -> Das Unternehmen muss den Nachweis erbringen, dass eine Einwilligung erfolgt ist.  Schau oder frage doch mal nach!....
                    ]
                    # "Du kannst in jedem Fall deine Daten löschen. Go to Generierung Musterschreiben"

        elif tracker.get_slot('consent_given') == 'ich_weiß_es_nicht':
                return [
                    "reason_for_deletion", #Welcher dieser Löschungsgründe könnte deiner Meinung nach infrage kommen? Was ist der Grund für die Datenlöschung?
                    "consent_given", # Hast du eine Einwilligung zur Datenverarbeitung erteilt?; Ja -> weiter, Nein -> Du kannst in jedem Fall deine Daten löschen, End form, Ich weiß nicht mehr -> Das Unternehmen muss den Nachweis erbringen, dass eine Einwilligung erfolgt ist.  Schau oder frage doch mal nach!....
                    ]
                    # Call Nachweis Einwilligung

        else:
            return [
                "reason_for_deletion", #Welcher dieser Löschungsgründe könnte deiner Meinung nach infrage kommen? Was ist der Grund für die Datenlöschung?
                ]


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        dispatcher.utter_message("Vielen Dank für die Eingabe.")
        return []

# reason_for_deletion: nicht mehr benötigt (Form beenden, Intent Einwilligungswiderrruf)
# reason_for_deletion: unrechtmäßige Einwilligung


class PersonalDataForm(FormAction):
    """Die Nutzerdaten werden erhoben"""

    def name(self):
        return "personal_data_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "name",
            "email",
            "kundennummer",
            "anschrift",
            "plz",
            "stadt",
            "land"
            ]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"name": [self.from_entity(entity="name"),
                             self.from_text()],
                "email": [self.from_entity(entity="email"),
                             self.from_text()],
                "kundennummer": [self.from_entity(entity="kundennummer"),
                                     self.from_text()],
                "anschrift": [self.from_entity(entity="anschrift"),
                                     self.from_text()],
                "plz": [self.from_entity(entity="plz"),
                                     self.from_text()],
                "stadt": [self.from_entity(entity="stadt"),
                                     self.from_text()],
                "land": [self.from_entity(entity="land"),
                                     self.from_text()]
                             }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:

        dispatcher.utter_message("Danke für die Angabe deiner Daten!")
        return []
