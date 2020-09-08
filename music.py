import typing

from aiocqhttp.message import MessageSegment

from hoshino import Service

from .search_netease_cloud_music import search as search163
from .search_qq_music import search as searchqq

sv = Service(
    'music',
    enable_on_default=True,
    visible=True,
    help_="[点歌 好日子] 混合搜索\n"
          "[搜网易 好日子] 搜索网易云\n"
          "[搜QQ 好日子] 搜索QQ音乐",
    bundle='pcr娱乐'
)


temp = {}


@sv.on_prefix(['选', '选择'])
async def choose_song(bot, ev):
    key = f'{ev.group_id}-{ev.user_id}'
    if key not in temp:
        await bot.send(ev, '你还没有点歌呢!', at_sender=True)
        return
    song_dict = temp[key]
    song_idx = []
    for msg_seg in ev.message:
        if msg_seg.type == 'text' and msg_seg.data['text']:
            song_idx.append(msg_seg.data['text'].strip())
    if not song_idx:
        await bot.send(ev, '你想听什么呀?', at_sender=True)
    else:
        song_idx = ''.join(song_idx)
        if song_idx in song_dict:
            song = song_dict[song_idx]
            if song['type'] == '163':
                music = MessageSegment.music(song['type'], song['id'])
            else:
                music = MessageSegment(
                    type_='music',
                    data={
                        'id': str(song['id']),
                        'type': song['type'],
                        'content': song['artists']
                    }
                )
            del temp[key]
            await bot.send(ev, music)
        else:
            await bot.send(ev, '只能选择列表中有的歌曲哦', at_sender=True)
            return


@sv.on_prefix(('点歌', '搜歌曲'))
async def to_apply_for_title(bot, ev):
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == 'text' and msg_seg.data['text']:
            music_name.append(msg_seg.data['text'].strip())
    if not music_name:
        await bot.send(ev, '你想听什么呀?', at_sender=True)
    else:
        music_name = ''.join(music_name)
        song_list = search_netease_cloud_music(music_name)
        if song_list:
            sv.logger.info('成功获取到歌曲列表')
            key = f'{ev.group_id}-{ev.user_id}'
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ['我找到了这些~!']
            flag = True
            if song_list[0]['type'] == '163':
                msg.append('===网易云音乐===')
            for idx, song in enumerate(song_list):
                if song['type'] == 'qq' and flag:
                    msg.append('===QQ音乐===')
                    flag = False
                msg.append(
                    f'{idx}. {song["name"]} - {song["artists"]}'
                )
                temp[key][str(idx)] = song
            msg.append('发送[选择]+序号来听歌吧~')
            await bot.send(ev, '\n'.join(msg), at_sender=True)
        else:
            await bot.send(ev, '什么也没有找到的说OxO')


@sv.on_prefix(('搜网易', '搜163', '搜网易云'))
async def search_netease_cloud_music(bot, ev):
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == 'text' and msg_seg.data['text']:
            music_name.append(msg_seg.data['text'].strip())
    if not music_name:
        await bot.send(ev, '你想听什么呀?', at_sender=True)
    else:
        music_name = ''.join(music_name)
        song_list = search163(music_name, result_num=5)
        if song_list:
            sv.logger.info('成功获取到歌曲列表')
            key = f'{ev.group_id}-{ev.user_id}'
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ['我找到了这些~!']
            for idx, song in enumerate(song_list):
                msg.append(
                    f'{idx}. {song["name"]} - {song["artists"]}'
                )
                temp[key][str(idx)] = song
            msg.append('发送[选择]+序号来听歌吧~')
            await bot.send(ev, '\n'.join(msg), at_sender=True)
        else:
            await bot.send(ev, '什么也没有找到的说OxO')


@sv.on_prefix(('搜qq', '搜QQ', '搜qq音乐', '搜QQ音乐'))
async def search_qq_music(bot, ev):
    music_name = []
    for msg_seg in ev.message:
        if msg_seg.type == 'text' and msg_seg.data['text']:
            music_name.append(msg_seg.data['text'].strip())
    if not music_name:
        await bot.send(ev, '你想听什么呀?', at_sender=True)
    else:
        music_name = ''.join(music_name)
        song_list = searchqq(music_name, result_num=5)
        if song_list:
            sv.logger.info('成功获取到歌曲列表')
            key = f'{ev.group_id}-{ev.user_id}'
            temp[key] = {}
            # _music = MessageSegment.music(type_=_type, id_=_id)
            msg = ['我找到了这些~!']
            for idx, song in enumerate(song_list):
                msg.append(
                    f'{idx}. {song["name"]} - {song["artists"]}'
                )
                temp[key][str(idx)] = song
            msg.append('发送[选择]+序号来听歌吧~')
            await bot.send(ev, '\n'.join(msg), at_sender=True)
        else:
            await bot.send(ev, '什么也没有找到的说OxO')


def search_netease_cloud_music(music_name: str) -> typing.Union[list, dict]:
    result = []
    song_list = search163(music_name)
    if song_list:
        result += song_list
    song_list = searchqq(music_name)
    if song_list:
        result += song_list
    return result
