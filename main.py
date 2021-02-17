from flask import Flask, request

from vkBot.brainOfVKBot import *


# TODO
#  1) write TO DO list


# server = Flask(__name__)
#
#
# @server.route('/' + token, methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return 'Ну типа Super Highly Intelligent Bot запущен', 200
#
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://super-highly-intelligent-tt.herokuapp.com/' + token)
#     return 'Ну типа Super Highly Intelligent Bot запущен, а я нужен для вебхука', 200


if __name__ == '__main__':
    print('lego')
    run_vk_bot()
    # server.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))
    # print('lego lego lego')
    # bot.polling(none_stop=True)
