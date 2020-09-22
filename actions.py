from rasa_sdk.forms import FormAction
from datenanfragen import search_company 
import json

class CompanySearchForm(FormAction):
    def name(self):
        return "company_search_form"

    @staticmethod
    def required_slots(tracker):
        return ["company_name"]


    def slot_mappings(self):
        return {"company_name": self.from_text(intent=None)}
    

    def submit(self, dispatcher, tracker, domain):
        companyButtons=list(map(lambda b: { "title": json.loads(b)["name"], "payload": "payload"}, search_company(tracker.get_slot("company_name"),5)))
        dispatcher.utter_message(text="Handelt es sich um eines der nachfolgenden Unternehmen? ", buttons=companyButtons)
        return []
