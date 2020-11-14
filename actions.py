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
from pyjarowinkler import distance
import zipfile
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import io
import os
import weasyprint 


company_zip = zipfile.ZipFile('./search/src/companies.zip', 'r')
companies = []
for name in company_zip.namelist():
    c_file = company_zip.open(name)
    c_data = c_file.read()
    try:
        c_obj = json.loads(c_data)
        companies.append({
            "company_name": c_obj["name"], 
            # "address": c_obj["address"], 
            "privacy_email": c_obj["email"]
        })
    except:
        pass

class generate_letter(FormAction) :
	@staticmethod
	def required_slots(tracker):
		return [
    		"company_name",
			"privacy_email"
		]

	def slot_mappings(self):
		return {"privacy_email": [self.from_entity(entity="privacy_email"), self.from_text()]}

	def name(self) -> Text:
		return "generate_letter"

	# nimmt Musterschreiben-Dateiname und gibt Mustertext als String wieder
	def get_letter_text(self,file_name):
		return open(file_name,"r").read()

	# durchsucht txt-Datei nach Parametern mit {PARAMETER_NAME} als Form und gibt alle Parameternamen als Liste wieder
	def list_needed_slots(self,text):
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

	def get_file_name(self):
		return None

	def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
		file_name = self.get_file_name()
		a = self.get_letter_text(file_name)
		b = self.list_needed_slots(a)
		c =	self.get_session_data_from_memory(b,tracker)
		d = self.fill_in_session_data(a,b,c)

		"""
		dispatcher.utter_message("Dein fertiges Schreiben wird generiert...")
		dispatcher.utter_message(d)
		"""
		smtp_server = smtplib.SMTP_SSL("securemail.linevast.de", 465, context=ssl.create_default_context())
		smtp_server.login(os.environ["HCLC_EMAIL"], os.environ["HCLC_PWD"])

		dispatcher.utter_message("Vielen Dank für Ihre Angaben! Ich generiere nun einen individualisierten Antrag, um ihn sodann der von Ihnen angegebenen E-Mail-Adresse zuzuleiten.")
		
		message = MIMEMultipart("alternative")
		message["Subject"] = "[HCLC] Ihr DSGVO-Antrag wurde erstellt"
		message["From"] = "Humboldt Consumer Law Clinic <{}>".format(os.environ["HCLC_EMAIL"])
		message["To"] = tracker.get_slot("email")

		message.attach(MIMEText("<p>Hallo {},</p><p>Ihr angefordertes Musterschreiben zur Weiterleitung an {} finden Sie im Anhang.</p><p>Mit freundlichen Grüßen</p><p>Ihre HCLC</p>".format(tracker.get_slot("name"), tracker.get_slot("privacy_email")), "html"))

		mustertextHtml = weasyprint.HTML(string=d)
		mustertextCss = weasyprint.CSS(string="p { font-family: Arial}")
		
		mustertextBuffer = io.BytesIO(mustertextHtml.write_pdf(stylesheets=[mustertextCss]))

		mustertextAttachment = MIMEApplication(
            mustertextBuffer.read(),
            Name="DSGVO-Antrag.pdf"
        )

		message.attach(mustertextAttachment)

		smtp_server.sendmail(os.environ["HCLC_EMAIL"], tracker.get_slot("email"), message.as_string())

		return []


	# nimmt Liste an benötigten Parametern und gibt jeweilige Werte aus der Session wieder
	def get_session_data_from_memory(self,parameter,tracker):
		
		session_data = {}

		for i in range(len(parameter)):
			key = parameter[i]
			value = tracker.current_state()['slots'][key]

			session_data.update({key:value}) 

		return session_data

	# nimmt Mustertext, Parameterliste, und jeweilige Session-Werte und gibt fertig formuliertes Schreiben als String wieder
	def fill_in_session_data(self,text, slots, session_data):
		for slot in range(len(slots)):
			current_session_data = slots[slot]
			text = text.replace("{"+slots[slot]+"}", session_data[current_session_data])

		return text

class generate_datenauskunft(generate_letter) :

	def name(self) -> Text:
		return "generate_datenauskunft"


	def get_file_name(self):
		return "datenauskunft.txt"

class generate_werbewiderspruch(generate_letter) :

	def name(self) -> Text:
		return "generate_werbewiderspruch"

	def get_file_name(self):
		return "werbewiderspruch.txt"

class generate_einwilligungswiderruf(generate_letter) :

	def name(self) -> Text:
		return "generate_einwilligungswiderruf"

	def get_file_name(self):
		return "einwilligungswiderruf.txt"

class generate_datenloeschantrag(generate_letter) :

	def name(self) -> Text:
		return "generate_datenloeschantrag"

	def get_file_name(self):
		return "datenloeschantrag.txt"

class CompanyForm(FormAction):
    def name(self):
        return "company_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "company_name"
            ]

    def slot_mappings(self):
        return {"company_name": [self.from_entity(entity="company_name"),
                             self.from_text()]}

    def next_intent(self):
        return "chitchat"

    def search_company(self, name, limit):
        return (sorted(companies, reverse=True, key=(lambda c:distance.get_jaro_distance(name,c["company_name"],winkler=True))))[:limit]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        #dispatcher.utter_message("Vielen Dank für die Eingabe.")
        companyButtons=list(map(lambda b: { "title": b["company_name"], "payload": "/"+self.next_intent()+json.dumps(b)}, self.search_company(tracker.get_slot("company_name"),5)))
        companyButtons.append({"title": "Keines dieser Unternehmen", "payload": "/"+self.next_intent()})
        dispatcher.utter_message(text="Handelt es sich um eines der nachfolgenden Unternehmen? ", buttons=companyButtons)


        return []

class InformationPersonalDataCompanyForm(CompanyForm):
    def name(self):
        return "information_personal_data_company_form"
    
    def next_intent(self):
        return "generate_datenauskunft_intent"

class StopUsingMyDataCompanyForm(CompanyForm):
    def name(self):
        return "stop_using_my_data_company_form"
    
    def next_intent(self):
        return "generate_einwilligungswiderruf_intent"

class StopAdvertisementCompanyForm(CompanyForm):
    def name(self):
        return "stop_advertisement_company_form"
    
    def next_intent(self):
        return "generate_werbewiderspruch_intent"

class DeletePersonalDataCompanyForm(CompanyForm):
    def name(self):
        return "delete_personal_data_company_form"
    
    def next_intent(self):
        return "generate_datenloeschantrag_intent"

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
