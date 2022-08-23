import json
import os
from pprint import pprint
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="vk1.a.TXRMCNOWnhiNNWE1rxY98HdRyJE7gCz0IbKwAtz2JZDRbejiGm_wf27h4AWHE8ZAxehogaMOXIJDYPJFTf35fT4SlZj5Dcrng6w5mde0fgehQGnzhwXi5SMgUBTsT5OKbukYQZkF9xbmfYIwZHbnxWoZFYxUxs4zKUurACbBx_HUmIPTndyc_KukGxP8tUvO")

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)




# if __name__ == '__main__':
#     load_dotenv()





