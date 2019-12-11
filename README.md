# 遊戲資訊助手-LINE Chat Bot

(重要)攻略圖為PTT艦收板，Eins(九夜)所有，非常感謝整理<br>
      另外攻略資訊還在整理中，最新資料請至各情報網站查詢<br>
## 簡介
將Chat Bot加為好友後只要用簡單指令就能取得活動攻略、各情報網站網址

## 功能
1.查詢活動海域攻略:根據E1~E6的輸入返回一圖流攻略，再次感謝Eins大<br>
2.查詢各情報網站網址:巴哈、ptt、日文wiki、英文wiki、官方twiiter等<br>

## FSM
![](https://github.com/e24054075/line-chat-bot/blob/master/img/show-fsm.png)

<br>
分成三個狀態:<br>
1.home:目錄，介紹指令與功能<br>
2.mapinfo:活動攻略提供區，輸入E1~E6就會提供這次海域的攻略圖<br>
3.information:遊戲情報網站提供區，提供各個情報網站網址<br>

## QRCode
![](https://github.com/e24054075/line-chat-bot/blob/master/img/qrcode.png)