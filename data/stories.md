## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

<!-- Test Stories -->
## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## Ask for help
* ask_for_help
  - utter_ask_for_help

## Insult
* insult
  - utter_insult

## Information
* information_personal_data
  - utter_information_personal_data

## Stop Data use
* stop_using_my_data
  - utter_stop_using_my_data

## Stop advertisement
* stop_advertisement
  - utter_stop_advertisement

## Delete personal data
* delete_personal_data
  - utter_delete_personal_data

## confused
* confused
  - utter_confused
  - utter_ask_for_help

## ask about hclc
* ask_about_hclc
  - utter_ask_about_hclc

## Datenschutz
* datenschutz_begriff
  - utter_datenschutz_begriff

## funpart
* fun_part
  - utter_fun_part

## ask about trust
* ask_about_trust
  - utter_ask_about_hclc
  - utter_ask_about_trust
