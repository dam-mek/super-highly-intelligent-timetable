from flask import Flask, request
import json

from vkBot.brainOfVKBot import *


# TODO
#  1) write TO DO list


server = Flask(__name__)


# @server.route('/' + token, methods=['POST'])
# def getMessage():
#     # bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     print(request)
#     bot.process_new_updates(request.stream.read().decode("utf-8"))
#     return 'Ну типа Super Highly Intelligent Bot vk запущен', 200


@server.route('/', methods=["POST"])
def main():
    data = json.loads(request.data)
    print(data)
    if data["type"] == "confirmation":
        run_vk_bot()
        return "confirmation code"


# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://super-highly-intelligent-tt.herokuapp.com/' + token)
#     return 'Ну типа Super Highly Intelligent Bot запущен, а я нужен для вебхука', 200


if __name__ == '__main__':
    print('lego')
    # run_vk_bot()
    server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
