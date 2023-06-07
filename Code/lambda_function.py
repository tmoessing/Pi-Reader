
from __future__ import print_function
import random
import json
import os



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, content, speech_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + speech_output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------



def handle_ReadPiIntents_intent(intent_name, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    pi = '3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420198'

    session_attributes = {}
    card_title      = "You Thought, of The Day"
    card_content    =  pi
                  
    speech_output   = pi

    reprompt_text   =  "Go ahead and ask me, if you need help just ask! "                        \

    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_launch_request(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title      = "Pi Reader"
    card_content    = "Welcome to Pi Reader"                      \


    speech_output   =  "Welcome to Pi Reader, To hear the first thousand digits of pi say, digits of pi. You can say stop at any time"

    reprompt_text   =  "To hear the first thousand digits of pi say, digits of pi. You can say stop at any time"

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))


def handle_help_intent(intent_name, session):

    session_attributes = {}
    card_title      = "Help"
    card_content    = "To hear the first thousand digits of pi say, read digits of pi"

    speech_output   = "To hear the first thousand digits of pi say, read digits of pi, or read pi. You can say stop, or cancel at any time as it might get annoying after a while"


    reprompt_text   = "To hear the first thousand digits of pi say, read digits of pi, or read pi. You can say stop, or cancel at any time as it might get annoying after a while"

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_end_intent():

    session_attributes = {}
    card_title      = "Goodbye"
    card_content    = "Goodbye"

    speech_output   = "Goodbye, enjoy the rest of your day!"

    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, None, should_end_session))

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
    return handle_launch_request(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ReadPiIntents" :
        return handle_ReadPiIntents_intent(intent_name, session)
    elif intent_name == "AMAZON.HelpIntent" or intent_name == "AMAZON.FallbackIntent":
        return handle_help_intent(intent_name,session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.NavigateHomeIntent" :
        return handle_end_intent()
    else:
        print("what the what is " + intent_name)
        raise ValueError("Invalid intent")

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
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.9c90b2dc-79cb-458a-bd73-47f27140bfea"):
         raise ValueError("Invalid Application ID")
    

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
