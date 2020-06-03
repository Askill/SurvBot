from flask import Flask, request
import requests
import motion_detector as md
import com
import _thread
import config
import telebot

app = Flask(__name__)
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    config.monitor = True
    print("start")

@bot.message_handler(commands=['stop'])
def stop(message):
    config.monitor = False
    print("stop")

# Process webhook calls
@app.route("/", methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return "", 403

if __name__ == '__main__':
    com.initEndpoint()
    _thread.start_new_thread(md.compare, () )
    app.run(host='0.0.0.0', port=5003, threaded=True, debug=False)