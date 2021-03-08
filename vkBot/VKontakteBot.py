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
            if '@all' in text:
                return
            chat_id = self.get_chat_id(event)
            print(text, chat_id)
            if chat_id in self.next_step:
                func, arguments = self.next_step[chat_id]
                del self.next_step[chat_id]
                func(event, **arguments)
                return
            for handler in self.message_handlers:
                if handler['command'] == text:
                    handler['function'](event)
                    return

            # Если запрос пользователя не был понят
            print('fuck', text)  # self.message_handlers)
            for handler in self.message_handlers:
                if handler['command'] == '':
                    handler['function'](event)

    def send_message(self, chat_id, text, reply_markup=None, reply_to_id=None):
        print(chat_id, text)
        arguments = dict(
            peer_id=chat_id,
            message=text,
            random_id=get_random_id()
        )
        if reply_markup is not None:
            arguments['keyboard'] = reply_markup.get_keyboard()
        # if reply_to_id is not None:
        #     arguments['forward_messages'] = str(reply_to_id)
        #     # print(self.vk.messages.getByConversationMessageId(
        #     #     peer_id=chat_id,
        #     #     conversation_message_ids=str(reply_to_id),
        #     # ))

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
        raw_text = raw_text.replace('[club202506545|@superhighlyintelligenttimetable]', '')
        text = raw_text.strip()
        if not text:
            text = 'помощь'
        return text

    @staticmethod
    def get_chat_id(event):
        return event['object']['message']['peer_id']
