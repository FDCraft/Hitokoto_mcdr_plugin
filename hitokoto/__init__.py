import json
import os
from typing import List, Callable, Any
import urllib.request
import urllib.error


from mcdreforged.api.all import *


class Config(Serializable):
      c: List[str] = [
            'a'
      ]
      min_length: int = 0
      max_length: int = 30

Prefix = '!!hitokoto'
config: Config
ConfigFilePath = os.path.join('config', 'hitokoto.json')


def get_url():
    url = 'https://v1.hitokoto.cn/?min_length={}&max_length={}'.format(config.min_length, config.max_length)
    for type in config.c:
        url = url + '&c={}'.format(type)
    return url

def get_hitokoto(url): 

    try:
        json_string = urllib.request.urlopen(url, timeout=30).read().decode('UTF-8', 'strict')
    except urllib.error.HTTPError as error:
        if error.code == 403:
            return '§b请求被限制了喵！'
        else:
            return '§b请求失败了喵！'
    except urllib.error.URLError:
        return '§b网络连接错误，请检查网络设置喵！'

    map = json.loads(json_string)
    who = '未知' if map['from_who'] is None else map['from_who']
    hitokoto = '§b[一言]§r{}——{} {}'.format(map['hitokoto'], who, map['from'])
    return hitokoto


def display_hitokoto(reply: Callable[[str], Any]):
    hitokoto = get_hitokoto(get_url())
    reply(hitokoto)


def on_player_joined(server: ServerInterface, player, info):
	display_hitokoto(lambda msg: server.tell(player, msg))


def on_load(server: PluginServerInterface, old):
    global config
    config = server.load_config_simple(file_name=ConfigFilePath, in_data_folder=False, target_class=Config)
    server.register_help_message(Prefix, '获取一句一言！')
    server.register_command(Literal(Prefix).runs(lambda src: display_hitokoto(src.reply)))