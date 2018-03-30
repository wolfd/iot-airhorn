import os
from flask import Flask
from flask import render_template
from flask import request
import RPi.GPIO as GPIO
import signal

SERVO_PIN = 18  # BCM pin
FREQUENCY = 50.0  # hz
SINGLE_CYCLE = 1000.0 / FREQUENCY  # ms
OFF_DUTY_CYCLE = (1.0 / SINGLE_CYCLE) * 100.0  # %
ON_DUTY_CYCLE = (2.1 / SINGLE_CYCLE) * 100.0  # %

app = Flask(__name__)

pwm = {
    SERVO_PIN: None
}
is_notifying = False

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm[SERVO_PIN] = GPIO.PWM(SERVO_PIN, FREQUENCY)
    pwm[SERVO_PIN].start(OFF_DUTY_CYCLE)

def cleanup_gpio():
    pwm[SERVO_PIN].stop()
    GPIO.cleanup()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notify')
def notify():
    # unused right now but I'm not going to remove it
    str_duration = request.args.get('duration', '1')
    try:
        duration = float(str_duration)
    except ValueError:
        return 'duration is not a number', 400
    # start pwming and store global
    if is_notifying is True:
        return 'already doing something', 400

    pwm[SERVO_PIN].ChangeDutyCycle(ON_DUTY_CYCLE)

    return 'honk'


@app.route('/stop')
def stop():
    # stop doing pwm and clear reference
    pwm[SERVO_PIN].ChangeDutyCycle(OFF_DUTY_CYCLE)
    is_notifying = False

    return 'stopped'


if __name__ == '__main__':
    setup_gpio()
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, cleanup_gpio)
    app.run(host='0.0.0.0', port=80, debug=True)
