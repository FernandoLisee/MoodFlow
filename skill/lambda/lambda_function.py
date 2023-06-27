# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from textblob import TextBlob
from translate import Translator
import requests
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá, como foi o seu dia hoje?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class MeuDiaIntentHandler(AbstractRequestHandler):
    """Handler for Meu Dia Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MeuDiaIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # speak_output = user_output
        text = handler_input.request_envelope.request.intent.slots['texto'].value
        
        textResponse = self.traduz_texto(text)
        textResponse = self.analyseText(textResponse)
        
        speak_output = self.chamaLink(textResponse)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
        
    def chamaLink(self, estado_espirito):
       # Define as informações da API do Spotify
        base_url = 'https://api.spotify.com/v1/'
        playlist_name = f'Estado de Espírito {estado_espirito.capitalize()}'
        headers = {
            'Authorization': 'Bearer TOKEN',
            'Content-Type': 'application/json'
        }
        # Mapeamento dos estados de espírito para os gêneros correspondentes
        generos = {
            'feliz': ['rock', 'pop', 'reggae'],
            'triste': ['indie', 'rock alternativo'],
            'calmo': ['musica classica', 'jazz', 'lofi'],
            'animado': ['funk', 'hip hop'],
            'motivado': ['metal', 'rap', 'eletronica']
        }
        
        # Verifica se o estado de espírito é válido
        if estado_espirito not in generos:
            print('Estado de espírito inválido.')
            return
        
        # Cria uma playlist vazia
        data = {
            'name': playlist_name,
            'public': False
        }
        response = requests.post(base_url + 'me/playlists', headers=headers, data=json.dumps(data))
        playlist_id = response.json()['id']
        
        # Obtém até 10 músicas aleatórias dos gêneros correspondentes
        tracks = []
        for genero in generos[estado_espirito]:
            response = requests.get(base_url + 'search', headers=headers, params={'q': f'genre:"{genero}"', 'type': 'track', 'limit': 10})
            tracks += response.json()['tracks']['items']
            if len(tracks) >= 10:
                break
        
        # Adiciona as faixas à playlist
        track_uris = [track['uri'] for track in tracks]
        data = {
            'uris': track_uris
        }
        response = requests.post(base_url + 'playlists/' + playlist_id + '/tracks', headers=headers, data=json.dumps(data))
        
        if response.status_code == 201:
            return f'Playlist {playlist_name} criada com sucesso! Ouça quando achar necessário'
        else:
            return 'Ocorreu um erro ao criar a playlist.'

    # Mapeia a polaridade para um estado de espírito correspondente   
    def analyseText(self, textResponse):
        polaridade = 0
        
        item = TextBlob(textResponse)
        
        polaridade += item.sentiment.polarity
        polaridadeResponse = ''
        
        if (polaridade >= -0.25 and polaridade <= 0.25):
            polaridadeResponse = 'motivado'
        elif (polaridade > -0.5 and polaridade < -0.25):
            polaridadeResponse = 'relaxado'
        elif (polaridade < -0.5):
            polaridadeResponse = 'triste'
        elif (polaridade > 0.25 and polaridade < 0.5):
            polaridadeResponse = 'animado'
        elif (polaridade >= 0.5):
            polaridadeResponse = 'feliz'
            
            
        return polaridadeResponse
        
    def traduz_texto(self, text):
        tradutor = Translator(to_lang="en", from_lang="pt")
        traducao = tradutor.translate(text)
        
        return traducao

# Código extraido do developer console da Alexa

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input: HandlerInput):
        user_input = handler_input.request_envelope.request.input_transcript
        print(user_input)
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Não entendi"
        reprompt = "Não entendi"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MeuDiaIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()