#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import argparse
import os.path
import json

import google.auth.transport.requests
import google.oauth2.credentials

import RPi.GPIO as GPIO
import time
import pygame

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.event import Event
from google.assistant.library.event import IterableEventQueue
from google.assistant.library.file_helpers import existing_file


DEVICE_API_URL = 'https://embeddedassistant.googleapis.com/v1alpha2'


def process_device_actions(event, device_id):
    if 'inputs' in event.args:
        for i in event.args['inputs']:
            if i['intent'] == 'action.devices.EXECUTE':
                for c in i['payload']['commands']:
                    for device in c['devices']:
                        if device['id'] == device_id:
                            if 'execution' in c:
                                for e in c['execution']:
                                    if 'params' in e:
                                        yield e['command'], e['params']
                                    else:
                                        yield e['command'], None


def process_event(event, device_id):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
        device_id(str): The device ID of the new instance.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in process_device_actions(event, device_id):
            print('Do command', command, 'with params', str(params))
            if command == "action.devices.commands.OnOff":
                if params['on']:
                    print('Turning the LED on.')
                else:
                    print('Turning the LED off.')
            if command == "com.acme.commands.blink_light":
                number = int(params['number'])
                for i in range(int(number)):
                    print('Device is blinking.')
                    time.sleep(1)
                    time.sleep(1)
            if command == "com.acme.commands.5Words":
                print("starting 5 words visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/5Words.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.beach":
                print("starting beach visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/Beach.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.bubbles":
                print("starting bubbles visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/Bubbles.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.deepbreathing":
                print("starting deep breathing visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/DeepBreathing.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.fire":
                print("starting fire white noise")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/fire.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.massage":
                print("starting massage visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/Massage.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.meditation":
                print("starting meditation visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/Meditation.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.rain":
                print("starting rain white noise")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/rain.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.relaxation":
                print("starting relaxation visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/Relaxation.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.visualization":
                print("starting basic visualization")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/Visualization.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.waterfall":
                print("starting waterfall white noise")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/waterfall.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.waterfountain":
                print("starting water-fountain white noise")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/water-fountain.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
            if command == "com.acme.commands.waterstream":
                print("starting water-stream white noise")
                time.sleep(3)
                pygame.mixer.init()
                pygame.mixer.music.load("/home/jnv/Music/water-stream.mp3")
                pygame.mixer.music.play()
                time.sleep(10)
    
def register_device(project_id, credentials, device_model_id, device_id):
    """Register the device if needed.

    Registers a new assistant device if an instance with the given id
    does not already exists for this model.

    Args:
       project_id(str): The project ID used to register device instance.
       credentials(google.oauth2.credentials.Credentials): The Google
                OAuth2 credentials of the user to associate the device
                instance with.
       device_model_id(str): The registered device model ID.
       device_id(str): The device ID of the new instance.
    """
    base_url = '/'.join([DEVICE_API_URL, 'projects', project_id, 'devices'])
    device_url = '/'.join([base_url, device_id])
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    r = session.get(device_url)
    print(device_url, r.status_code)
    if r.status_code == 404:
        print('Registering....')
        r = session.post(base_url, data=json.dumps({
            'id': device_id,
            'model_id': device_model_id,
            'client_type': 'SDK_LIBRARY'
        }))
        if r.status_code != 200:
            raise Exception('failed to register device: ' + r.text)
        print('\rDevice registered.')


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    parser.add_argument('--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=True,
                        help='The device model ID registered with Google')
    parser.add_argument(
        '--project_id',
        type=str,
        metavar='PROJECT_ID',
        required=False,
        help='The project ID used to register device instances.')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' +
        Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials, args.device_model_id) as assistant:
        events = assistant.start()

        print('device_model_id:', args.device_model_id + '\n' +
              'device_id:', assistant.device_id + '\n')

        if args.project_id:
            register_device(args.project_id, credentials,
                            args.device_model_id, assistant.device_id)

        for event in events:
            process_event(event, assistant.device_id)


if __name__ == '__main__':
    main()
