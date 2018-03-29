import os
from flask import Flask, request
import RPi.GPIO as GPIO
import atexit

ACTUATOR_CHANNEL = 12

app = Flask(__name__)

pwm = {
    ACTUATOR_CHANNEL: None
}

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ACTUATOR_CHANNEL, GPIO.OUT)

def cleanup_gpio():
    GPIO.cleanup()


@app.route('/')
def index():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(os.path.abspath(dir_path), 'index.html')
    # app.send_static_file(os.path.join(os.path.abspath(dir_path), 'index.html'))

@app.route('/notify')
def notify():
    str_duration = request.args.get('duration', '1')
    try:
        duration = float(str_duration)
    except ValueError:
        return 'duration is not a number', 400
    # start pwming and store global
    if pwm[ACTUATOR_CHANNEL] is not None:
        return 'already doing something', 400
    p = GPIO.PWM(ACTUATOR_CHANNEL, 0.5)
    p.start(1)
    pwm[ACTUATOR_CHANNEL] = p

    return 'honk'

@app.route('/stop')
def stop():
    # stop doing pwm and clear reference
    if pwm[ACTUATOR_CHANNEL] is None:
        return 'not doing anything', 400
    pwm[ACTUATOR_CHANNEL].stop()
    pwm[ACTUATOR_CHANNEL] = None

    return 'stopped'


if __name__ == '__main__':
    setup_gpio()
    atexit.register(cleanup_gpio)
    app.run(host='0.0.0.0', port=80, debug=True)
