from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_home(self, event):
        send_text_message(event.reply_token, "現在位置:目錄\n活動攻略:取得本次活動攻略\n情報:各情報網站網址\n返回:回目錄\nhelp:取得指令")
    def on_enter_mapinfo(self, event):
         send_text_message(event.reply_token, "現在位置:活動攻略\n請輸入E1~6其中一種指令取得攻略(例:E2)\n返回:回目錄\nhelp:取得指令")
    def on_enter_information(self, event):
         send_text_message(event.reply_token, "現在位置:情報\n請輸入:\n巴哈,ptt,日wiki,英wiki,推特 其中一種指令取得網址\n返回:回目錄\nhelp:取得指令")
