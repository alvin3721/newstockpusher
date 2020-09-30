import requests
import time
import json
import datetime
import re
import queue
import telegram

#Telegram bot的token
token = 'xxxxxxxxxxxxxxxxxxxx'

#Telegram Chat id
chatid = '-1001243935394'

bot = telegram.Bot(token=token)


today = datetime.date.today().strftime('%m-%d')

print('Today: ' + today)

r = requests.get('https://www.jisilu.cn/data/new_stock/apply/')
while r.status_code != 200:
    time.sleep(10)
    r = requests.get('https://www.jisilu.cn/data/new_stock/apply/')
txt = r.text.replace('\/','/').encode('utf-8').decode('unicode_escape')
print(txt)
txt = txt.replace('<a href="/setting/member/">会员</a>','')
print(txt)
txt = txt.replace('<span style="font-weight:bolder;color:red">','').replace('<span style="color:#aaa;font-style:italic">','').replace('<a href="/question/abstract/71606">购买</a>','').replace('<span style="font-weight:bolder">','').replace('<span style="color:red;font-weight:bolder">','').replace('<span title="股票现价" style="color:#aaa;font-style:italic">','').replace('</span>','')
# txt = re.sub('\<span style="?!"*"\>', '', txt)
print(txt)
js = json.loads(txt)
rows = js['rows']
sq = queue.Queue()
for row in rows:
    apply_dt = row['cell']['apply_dt']
    if apply_dt.startswith(today):
        sq.put(row)

text = ''
if not sq.empty():
    text = '今日(' + today + ')新股申购：\n'

while not sq.empty():
    js = sq.get()
    js = js['cell']
    print(js)
    name = js['stock_nm']
    id = js['stock_cd']
    need_market_value_show = js['need_market_value_show']
    issue_price = js['issue_price']
    individual_limit_show = js['individual_limit_show']
    text += '\n<b>' + name + '</b>(' + id + ')\n' + '发行价：' + issue_price + '\n' + '顶格需配市值：' + need_market_value_show + '万元\n' + '顶格申购限额：' + individual_limit_show + '万股\n'


bot.sendMessage(chatid, text, parse_mode='HTML')  #推送到telegram
