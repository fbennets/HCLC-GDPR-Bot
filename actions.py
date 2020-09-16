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
