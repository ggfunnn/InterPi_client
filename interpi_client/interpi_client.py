from flask import request
import time
import requests
import RPi.GPIO as GPIO
import os
import configparser


class Interpi_client(object):
    def __init__(self):
        pass

    def __del__(self):
        os.system('pkill python3')

    def ring(self):

        if request.method == 'POST':

            path = os.path.dirname(os.path.realpath(__file__))
            os.system('aplay ' + path + '/sound.wav')

            return {'result': 'OK'}

        else:
            return {'result': 'Error 400: Bad request method'}


class Button_daemon(object):
    """Class of deamon which waits for the gpio button input"""
    def __init__(self):
        path = os.path.dirname(os.path.realpath(__file__))
        config = configparser.ConfigParser()
        config.read(path + '/config.ini')

        self.ipaddress = config['button_daemon']['Server_ipaddress']
        self.port = config['button_daemon']['Server_port']
        self.hostname = config['button_daemon']['Hostname']

        self.PINS = {
            'Wicket_button': int(config['button_daemon']['Wicket_button_pin'])
            }

    def __del__(self):
        GPIO.cleanup()

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.PINS['Wicket_button'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def wait(self):
        last_state = 'locked'

        while True:

            if GPIO.input(self.PINS['Wicket_button']) and last_state == 'locked':
                self.__unlock()
                last_state = 'unlocked'

            if not GPIO.input(self.PINS['Wicket_button']) and last_state == 'unlocked':
                self.__lock()
                last_state = 'locked'

            time.sleep(0.1)

    def __unlock(self):
#       TODO: excepiton
        request_url = 'http://' + self.ipaddress + ':' + self.port + '/unlock/'

        r = requests.post(url=request_url, params={'name': self.hostname})

        if r.json() == {'result': 'OK'}:
#           TODO: log
            pass

    def __lock(self):
        request_url = 'http://' + self.ipaddress + ':' + self.port + '/lock/'

        r = requests.post(url=request_url, params={'name': self.hostname})

        if r.json() == {'result': 'OK'}:
#           TODO: log
            pass
