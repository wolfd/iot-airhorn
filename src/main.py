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

@app.route('/')
def index():
    return 'what'
    #app.send_static_file('index.html')

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
    return 'stopped'
    # stop doing pwm and clear reference
    if pwm[ACTUATOR_CHANNEL] is None:
        return 'not doing anything', 400
    pwm[ACTUATOR_CHANNEL].stop()
    pwm[ACTUATOR_CHANNEL] = None
    

def cleanup_gpio():
    GPIO.cleanup()

if __name__ == '__main__':
    setup_gpio()
    atexit.register(cleanup_gpio)
    app.run(host='0.0.0.0', port=80, debug=True)
