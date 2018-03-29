from flask import Flask, request
from flask.ext.api import status
import pigpio
import atexit

app = Flask(__name__)
gpio = pigpio.pi()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/notify')
def notify():
    str_duration = request.args.get('duration', '1')
    try:
        duration = float(str_duration)
    except ValueError:
        content = {'error': 'duration is not a number'}
        return content, status.HTTP_400_BAD_REQUEST
    # gpio here

    return "honk"

@app.route('/stop')
def stop():
    return "stopped"
    # gpio here

def close_gpio():
    gpio.stop()

if __name__ == '__main__':
    atexit.register(close_gpio)
    app.run(host='0.0.0.0', port=80)
