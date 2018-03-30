import os
from flask import Flask
from flask import render_template
from flask import request
import wiringpi
import signal

SERVO_PIN = 18  # BCM pin
FREQUENCY = 50 # hz
SINGLE_CYCLE = 1000.0 / FREQUENCY  # ms
OFF_DUTY_CYCLE = (1.0 / SINGLE_CYCLE) * 100.0  # %
ON_DUTY_CYCLE = (2.1 / SINGLE_CYCLE) * 100.0  # %

app = Flask(__name__)

pwm = {
    SERVO_PIN: None
}
is_notifying = False

def setup_gpio():
    wiringpi.wiringPiSetupGpio()
    wiringpi.pinMode(SERVO_PIN, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)

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

    wiringpi.pwmWrite(SERVO_PIN, 100)

    return 'honk'


@app.route('/stop')
def stop():
    # stop doing pwm and clear reference
    wiringpi.pwmWrite(SERVO_PIN, 210)
    is_notifying = False

    return 'stopped'


if __name__ == '__main__':
    setup_gpio()
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, cleanup_gpio)
    app.run(host='0.0.0.0', port=80, debug=True)
