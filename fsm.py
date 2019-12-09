from transitions.extensions import GraphMachine
import os
from utils import send_text_message
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_music(self, event):
        text = event.message.text
        return (text.lower() == "音樂" or text.lower() == "music")

    def is_going_to_exam(self, event):
        text = event.message.text
        return (text.lower() == "考古試題" or text.lower() == "考古" or text.lower() == "讀書" or text.lower() == "study")

    def is_going_to_first(self, event):
        text = event.message.text
        return text.lower() == "大一"

    def is_going_to_first_1(self, event):
        text = event.message.text
        return text.lower() == "大一上"

    def is_going_to_first_2(self, event):
        text = event.message.text
        return text.lower() == "大一下"    

    def is_going_to_second(self, event):
        text = event.message.text
        return text.lower() == "大二"

    def is_going_to_second_1(self, event):
        text = event.message.text
        return text.lower() == "大二上"

    def is_going_to_second_2(self, event):
        text = event.message.text
        return text.lower() == "大二下" 

    def is_going_to_third(self, event):
        text = event.message.text
        return text.lower() == "大三"

    def is_going_to_third_1(self, event):
        text = event.message.text
        return text.lower() == "大三上"

    def is_going_to_third_2(self, event):
        text = event.message.text
        return text.lower() == "大三下"

    def is_going_to_bye(self, event):
        text = event.message.text
        if text.lower() == "bye":
            message = TextSendMessage(text='歐趴天使降臨~\n(回到主選單)')
            line_bot_api.reply_message(event.reply_token, message)
        return text.lower() == "bye"

    def on_enter_music(self, event):
        print("I'm entering music")

        reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/11/30/H34sWY.jpg',
                        action=
                            URITemplateAction(
                                label='讀書',
                                uri='https://www.youtube.com/results?search_query=讀書音樂'
                            ),
                    ),
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/11/30/02tuzp.jpg',
                        action=
                            URITemplateAction(
                                label='抒情',
                                uri='https://www.youtube.com/results?search_query=抒情'
                            ),
                    ),
                    ImageCarouselColumn(
                        image_url='https://upload.cc/i1/2019/11/30/9eSz58.jpg',
                        action=
                            URITemplateAction(
                                label='嗨歌',
                                uri='https://www.youtube.com/results?search_query=嗨歌'
                            ),
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, message)

    def on_exit_music(self, event):
        print("Leaving music")

    def on_enter_exam(self, event):
        print("I'm entering exam")

        reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.cc/i1/2019/11/28/dkP276.jpg',
                title='年級選擇',
                text='請選擇你的年級唷！',
                actions=[
                    MessageTemplateAction(
                        label='大一',
                        text='大一'
                    ),
                    MessageTemplateAction(
                        label='大二',
                        text='大二'
                    ),
                    MessageTemplateAction(
                        label='大三',
                        text='大三'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, message)

    def on_exit_exam(self, event):
        print("Leaving exam")
    
    def on_enter_first(self, event):
        print("I'm entering first")

        reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.cc/i1/2019/11/28/jnhiXF.jpg',
                title='學期選擇',
                text='請選擇上/下學期唷！',
                actions=[
                    MessageTemplateAction(
                        label='大一上',
                        text='大一上'
                    ),
                    MessageTemplateAction(
                        label='大一下',
                        text='大一下'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, message)

    def on_exit_first(self, event):
        print("Leaving first")

    def on_enter_first_1(self, event):
        print("I'm entering first1")

        text = event.message.text
        reply_token = event.reply_token
        if text != 'bye':
            message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://upload.cc/i1/2019/11/29/hrF7R9.jpg',
                    title='科目選擇',
                    text='請選擇欲查看科目唷！',
                    actions=[
                        URITemplateAction(
                            label='程設(一)',
                            uri='https://drive.google.com/drive/folders/1YxdEEiwbb9-96BeOOI-Chyx2R-XV7ZmX?usp=sharing'
                        ),
                        URITemplateAction(
                            label='普物(一)',
                            uri='https://drive.google.com/drive/folders/1dCuFcm17UNgVeiHs-eI_9xxh-R5Uv0HO?usp=sharing'
                        ),
                        URITemplateAction(
                            label='計概',
                            uri='https://drive.google.com/open?id=1yPyTLjPKt65zlTIduLX7ZrRGF9MlgEfK'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(reply_token, message)

    def on_exit_first_1(self, event):
        print("Leaving first_1")

    def on_enter_first_2(self, event):
        print("I'm entering first_2")

        text = event.message.text
        reply_token = event.reply_token
        if text != 'bye':
            message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://upload.cc/i1/2019/11/29/5rEpa3.jpg',
                    title='科目選擇',
                    text='請選擇欲查看科目唷！',
                    actions=[
                        URITemplateAction(
                            label='程設(二)',
                            uri='https://drive.google.com/open?id=1euMre2zzWOR2kKHesyK0ZZiNhnU2Mcb2'
                        ),
                        URITemplateAction(
                            label='普物(二)',
                            uri='https://drive.google.com/open?id=1eKKPESEfyN8YmWCq_OC_T9XuFyGK0BzR'
                        ),
                        URITemplateAction(
                            label='計概',
                            uri='https://drive.google.com/open?id=1yPyTLjPKt65zlTIduLX7ZrRGF9MlgEfK'
                        ),
                        URITemplateAction(
                            label='線代',
                            uri='https://drive.google.com/open?id=1zPiF4tqFkfn0-DA2blyCPVdSfcQT__lr'
                        ),
                        URITemplateAction(
                            label='數導',
                            uri='https://drive.google.com/open?id=1m5EAobDdEWMRMa1Lgj--jZgu-7MYEYE2'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(reply_token, message)

    def on_exit_first_2(self, event):
        print("Leaving first2")

    def on_enter_second(self, event):
        print("I'm entering second")
        reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.cc/i1/2019/11/28/UeHCFP.jpg',
                title='學期選擇',
                text='請選擇上/下學期唷！',
                actions=[
                    MessageTemplateAction(
                        label='大二上',
                        text='大二上'
                    ),
                    MessageTemplateAction(
                        label='大二下',
                        text='大二下'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, message)

    def on_exit_second(self, event):
        print("Leaving second")

    def on_enter_second_1(self, event):
        print("I'm entering second1")

        text = event.message.text
        reply_token = event.reply_token
        if text != 'bye':
            message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://upload.cc/i1/2019/11/29/KbgZrn.jpg',
                    title='科目選擇',
                    text='請選擇欲查看科目唷！',
                    actions=[
                        URITemplateAction(
                            label='資結',
                            uri='https://drive.google.com/open?id=0B7s9hgRn7CYqZ0lKLUJkYzVkQjQ'
                        ),
                        URITemplateAction(
                            label='數導',
                            uri='https://drive.google.com/open?id=0B7s9hgRn7CYqczNmU0pQdllQanM'
                        ),
                        URITemplateAction(
                            label='工數',
                            uri='https://drive.google.com/open?id=0B7s9hgRn7CYqUTNHWHNfRVdmZFU'
                        ),
                        URITemplateAction(
                            label='機統',
                            uri='https://drive.google.com/open?id=1fltY-SdsGppiyMmTmv3ueV0ej5dYiEhP'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(reply_token, message)

    def on_exit_second_1(self, event):
        print("Leaving second1")

    def on_enter_second_2(self, event):
        print("I'm entering second2")

        text = event.message.text
        reply_token = event.reply_token
        if text != 'bye':
            message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://upload.cc/i1/2019/11/29/IOtgXF.jpg',
                    title='科目選擇',
                    text='請選擇欲查看科目唷！',
                    actions=[
                        URITemplateAction(
                            label='計組',
                            uri='https://drive.google.com/open?id=0B7s9hgRn7CYqbnpnSGhSeGpUU2M'
                        ),
                        URITemplateAction(
                            label='離散',
                            uri='https://drive.google.com/drive/folders/0B7s9hgRn7CYqMXY1NndtM3RHakE?usp=sharing'
                        ),
                        URITemplateAction(
                            label='演算法',
                            uri='https://drive.google.com/open?id=0B7s9hgRn7CYqaXFhazRtQjVDdUE'
                        ),
                        URITemplateAction(
                            label='JAVA',
                            uri='https://drive.google.com/open?id=0B7s9hgRn7CYqbUJQV2tQbU9iNDA'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(reply_token, message)

    def on_exit_second_2(self, event):
        print("Leaving second2")

    def on_enter_third(self, event):
        print("I'm entering third")

        reply_token = event.reply_token
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://upload.cc/i1/2019/11/28/k8FwXP.jpg',
                title='學期選擇',
                text='請選擇上/下學期唷！',
                actions=[
                    MessageTemplateAction(
                        label='大三上',
                        text='大三上'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(reply_token, message)

    def on_exit_third(self, event):
        print("Leaving third")

    def on_enter_third_1(self, event):
        print("I'm entering third1")

        text = event.message.text
        reply_token = event.reply_token
        if text != 'bye':
            message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://upload.cc/i1/2019/11/29/Oj2h5g.jpg',
                    title='科目選擇',
                    text='請選擇欲查看科目唷！',
                    actions=[
                        URITemplateAction(
                            label='作業系統',
                            uri='https://drive.google.com/open?id=13kKH4ijOQvM3Df5lNdg9eFg6Ey91SgZT'
                        ),
                        URITemplateAction(
                            label='計理',
                            uri='https://drive.google.com/open?id=1uGQSITF3zm-KMW8ltbdMoUU4H8U-W-jr'
                        ),
                        URITemplateAction(
                            label='微算機',
                            uri='https://drive.google.com/open?id=150xS1neA9s8AL1KebBnqgCA6oczqs48Z'
                        ),
                        URITemplateAction(
                            label='無線',
                            uri='https://drive.google.com/open?id=1A2IjW7RzzG3Whm-GZdxyOOcIzt1Tu9eX'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(reply_token, message)

    def on_exit_third_1(self, event):
        print("Leaving third1")

    def on_enter_bye(self, event):
        print("I'm going back user")

    def on_exit_bye(self, event):
        print("bye")    