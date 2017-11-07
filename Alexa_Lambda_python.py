#"""
#This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
#The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
#as testing instructions are located at http://amzn.to/1LzFrj6

#For additional samples, visit the Alexa Skills Kit Getting Started guide at
#http://amzn.to/1LGWsLG
#"""

from __future__ import print_function
import urllib2
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


#### Ignition Web Call variables####
baseURL = 'https://sparksvm.eastus.cloudapp.azure.com/main/system/webdev/Alexa/alexaFunctions/'

IgnitionBackground1 = "https://i.imgur.com/9QGCB5e.png";



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
		"directives": [
        {
          "template": {
            "backButtonBehavior": "VISIBLE",
            "backgroundImage": {
              "contentDescription": "The Image",
              "sources": [
                {
                  "url": "https://example.com/barimage.png",
                  "size": "x-small",
                  "widthPixels": 0,
                  "heightPixels": 0
                }
              ]
            },
            "title": "Mohawk Austin",
            "textContent": {
              "primaryText": {
                "text": "<font size='4'><b>Happy Hour 5-8 PM: Over 60 Beers, 60 Spirits and 16 Drafts</b></font>"
              }
            }
          }
        }
      ],
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Ignition demo. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    print(intent['slots'])
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "Hmm. I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    #return get_welcome_response()
	
    homeScreenResponse = getHomeScreen()
    print('Response: ' + str(homeScreenResponse))

    return homeScreenResponse


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Intent_ShowProduction":
        productionStatusResponse = showProductionStatus()
        return productionStatusResponse
    elif intent_name == "Intent_ViewTPM":
        productionStatusResponse = showProductionStatus()
        return productionStatusResponse
		
    elif intent_name == "Intent_ShowLine":
        return showLineDetails(intent, session)
		
    
 
    elif intent_name == "Intent_MainMenu":
        homeScreenResponse = getHomeScreen()
        return homeScreenResponse
        #return set_color_in_session(intent, session)

			###########################
    #elif event['request']['type'] == "ElementSelected":
       # return testClick()
    elif intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        #return get_welcome_response()
        homeScreenResponse = getHomeScreen()
        return homeScreenResponse
    elif intent_name == "AMAZON.PreviousIntent":
        return goBack()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    
    else:
        homeScreenResponse = getHomeScreen()
        return homeScreenResponse


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
        return on_launch(event['request'], event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    elif event['request']['type'] == "Display.ElementSelected":
        return elementSelected(event['request']['token'])
    else:
        #return on_session_ended(event['request'], event['session'])
        return on_launch(event['request'], event['session'])

def getHomeScreen():
    response = urllib2.urlopen(baseURL + "getHomeScreen",context=ctx)
    homeScreenResponse = json.load(response)   
	
    return homeScreenResponse

def goBack():
    response = urllib2.urlopen(baseURL + "goBack",context=ctx)
    goBackResponse = json.load(response)
    
    return goBackResponse

def showLineDetails(intent,session):
	print(intent['slots'])
	if 'LineName' in intent['slots']:
		lineName = intent['slots']['LineName']['value']
		speech_output = "I now know the line name is " + lineName + ". That is all I can do for now. haha"
        
	else:
		speech_output = "I will read the info now " + str(intent['slots'])
	
	lineDetailsResponse = {
	  "version": "1.0",
	  "response": {
		"card": None,
		"outputSpeech": {
		  "type": "PlainText",
		  "text": speech_output
		},
		"reprompt": {
		  "outputSpeech": {
			"type": "PlainText",
			"text": "How can I help you?"
		  }
		}
	  }
	}
	
	return lineDetailsResponse

def elementSelected(token):

	if token == 'productionStatus':
		return showProductionStatus()
	else:

		speech_output = "I can tell you clicked on " + token + ".  I dont know what to do next."
		
		lineDetailsResponse = {
		  "version": "1.0",
		  "response": {
			"card": None,
			"outputSpeech": {
			  "type": "PlainText",
			  "text": speech_output
			},
			"reprompt": {
			  "outputSpeech": {
				"type": "PlainText",
				"text": "How can I help you?"
			  }
			}
		  }
		}
		
		return lineDetailsResponse

def showProductionStatus():

	response = urllib2.urlopen(baseURL + "showProductionStatus",context=ctx)
	productionStatusResponse = json.load(response)

	
	return productionStatusResponse
