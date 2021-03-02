import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


class VKontakteBot:

    def __init__(self, token):
        self.message_handlers = []
        self.next_step = dict()
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        # self.longpoll = VkBotLongPoll(self.vk_session, 202506545)

    def process_event(self, event):
        # print(type(event))
        # print(event['type'], VkBotEventType.MESSAGE_NEW, event['type'] == VkBotEventType.MESSAGE_NEW)
        if event['type'] == 'message_new':
            text = self.get_text(event).lower()
            chat_id = event['object']['message']['peer_id']
            print(text, chat_id)
            if chat_id in self.next_step:
                func, arguments = self.next_step[chat_id]
                del self.next_step[chat_id]
                func(event, **arguments)
                return
            for handler in self.message_handlers:
                if text == handler['command']:
                    handler['function'](event)
                    return
            print('fuck', text)  # self.message_handlers)

    def send_message(self, chat_id, text, reply_markup=None):
        print(chat_id, text)
        arguments = dict(
            peer_id=chat_id,
            message=text,
            random_id=get_random_id()
        )
        if reply_markup is not None:
            arguments['keyboard'] = reply_markup.get_keyboard()
        self.vk.messages.send(**arguments)
        return chat_id

    def message_handler(self, command: str):

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, command)
            self.add_message_handler(handler_dict)
            return handler

        return decorator

    def add_message_handler(self, handler_dict):
        self.message_handlers.append(handler_dict)

    def register_next_step_handler(self, chat_id, callback, **kwargs):
        self.next_step[chat_id] = (callback, kwargs)

    @staticmethod
    def _build_handler_dict(handler, command):
        return {
            'function': handler,
            'command': command.lower()
        }

    @staticmethod
    def get_text(event):
        raw_text = event['object']['message']['text']
        if raw_text.startswith('[club202506545|'):
            if len(raw_text.split()) == 1:
                text = 'помощь'
            else:
                text = raw_text[raw_text.find(' ') + 1:]
        else:
            text = raw_text
        return text
