import random
import json
from time import localtime
from requests import get, post
from datetime import datetime,date


# 获取随机颜色
# def get_color():
#     def get_colors(n):
#         return ["#" + "%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
#     color_list = get_colors(1000)
#     return random.choice(color_list)
#!!!有问题，待修复

def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败,请检查app_id和app_secret是否正确")
    return access_token

#获取天气
def get_weather(headers,region,key):
    weather_url='https://apis.tianapi.com/tianqi/index?key={}&city={}&type=7'.format(key,region)
    response = get(weather_url, headers=headers).json()
    if response["code"]=="230":
        print("key错误或为空")
    elif response["code"]=="260" or response["code"]=='250':
        print("城市错误或为空")
    temp1=response['result']['list'][0]
    today_date=temp1['date']
    today_temp=str(temp1['lowest']).replace('℃','')+'~'+str(temp1['highest']).replace('℃','')
    today_weather=temp1['weather']
    today_wind=temp1['wind']
    today_tips=response['result']['list'][0]['tips']
    
    temp2=response['result']['list'][1]
    tomorrow_date=temp2['date']
    tomorrow_temp=str(temp2['lowest']).replace('℃','')+'~'+str(temp2['highest']).replace('℃','')
    tomorrow_weather=temp2['weather']
    tomorrow_wind=temp2['wind']
    tomorrow_tips=response['result']['list'][1]['tips']

    return today_date,today_weather,today_temp,today_wind,today_tips,\
            tomorrow_date,tomorrow_weather,tomorrow_temp,tomorrow_wind,tomorrow_tips

#生日在这里
def bir(birthday):
    # 获取当前日期
    now=datetime.now()
    # 将用户的出生日期字符串转换为datetime对象
    birthday=datetime.strptime(birthday,"%Y-%m-%d")
    # 计算今年生日的日期
    this_year_birthday=datetime(now.year,birthday.month,birthday.day)
    # 如果今年生日已经过了,则计算明年生日的日期
    if this_year_birthday<now:
        this_year_birthday=datetime(now.year+1,birthday.month,birthday.day)
    # 计算距离今年生日还有多久时间
    time_to_birthday=this_year_birthday-now
    # 输出结果
    birthday=(time_to_birthday.days+1)
    return birthday


#今日热搜
def get_hotpoint(headers):
    urlx='https://apis.tianapi.com/toutiaohot/index?key={}'.format(key)
    a=get(urlx,headers)
    a=json.loads(a.text)
    hotpoint1=a['result']['list'][0]['word']
    hotpoint2=a['result']['list'][1]['word']
    hotpoint3=a['result']['list'][2]['word']
    return hotpoint1,hotpoint2,hotpoint3


#今日星座运势
def get_xingzuo(headers,key):
    urly='https://apis.tianapi.com/star/index?key={}&astro=sagittarius'.format(key)
    health=get(urly,headers)
    health=json.loads(health.text)
    zonghe=str(health['result']['list'][0]['content']).replace('%','')
    aiqing=str(health['result']['list'][1]['content']).replace('%','')
    caiyun=str(health['result']['list'][3]['content']).replace('%','')
    jiankang=str(health['result']['list'][4]['content']).replace('%','')
    gshu=str(health['result']['list'][8]['content'])
    return zonghe,aiqing,caiyun,jiankang,gshu

#获取语句
def get_content(headers,key):
    url = "http://open.iciba.com/dsapi/"
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    url='https://apis.tianapi.com/wanan/index?key={}'.format(key)
    r = get(url,headers)
    note_wanan=r.json()['result']['content']
    return note_ch,note_en,note_wanan
 

def send_message(to_user,today_tips,tomorrow_tips,
                 today_date,tomorrow_date,
                 birthdaydata1,birthdaydata2,
                 access_token,region,
                 today_weather,today_temp,today_wind,
                 tomorrow_weather,tomorrow_temp,tomorrow_wind,
                 zonghe,aiqing,caiyun,jiankang,gshu,
                 hotpoint1,hotpoint2,hotpoint3,
                 note_ch,note_en,note_wanan):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    yearx = localtime().tm_year
    monthx = localtime().tm_mon
    dayx = localtime().tm_mday
    today = datetime.date(datetime(year=yearx, month=monthx, day=dayx))
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    #区分白天和晚上，推送不同模板
    timenow=datetime.now().hour
    if timenow<22:
        template=config["template_morning_id"]
    else:
        template=config["template_night_id"]
    data = {
        "touser": to_user,
        "template_id": template,
        "url": "http://weixin.qq.com/download",
        # "topcolor": "#FF0000",
        "data": {
             "today_date": {
                "value": today_date
            },
            "tomorrow_date": {
                "value": tomorrow_date
            },
            "region": {
                "value": region
            },
            "birthdaydata1": {
                "value": birthdaydata1
            },
            "birthdaydata2": {
                "value": birthdaydata2
            },
            "today_weather": {
                "value": today_weather
            },
            "tomorrow_weather": {
                "value": tomorrow_weather
            },
            "today_tips": {
                "value": today_tips
            },
            "tomorrow_tips": {
                "value": tomorrow_tips
            },
            "today_temp": {
                "value": today_temp
            },
            "tomorrow_temp": {
                "value": tomorrow_temp
            },
            "today_wind": {
                "value": today_wind
            },
            "tomorrow_wind": {
                "value": tomorrow_wind
            },
            "love_day": {
                "value": love_days
            },
            "zonghe": {
                "value": zonghe
            },
            "caiyun": {
                "value": caiyun
            },
            "jiankang": {
                "value": jiankang
            },
            "aiqing": {
                "value": aiqing
            },
            "gshu": {
                "value": gshu
            },
            "hotpoint1": {
                "value": hotpoint1
            },
            "hotpoint2": {
                "value": hotpoint2
            },
            "hotpoint3": {
                "value": hotpoint3
            },
            "note_en": {
                "value": note_en
            },
            "note_ch": {
                "value": note_ch
            },
            "note_wanan": {
                "value": note_wanan
            }
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (today_windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败,请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败,请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败,请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (today_windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        with open("git/ForChen/config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except SyntaxError:
        print("推送消息失败,请检查配置文件格式是否正确")

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入地区
    region = config["region"]
    key = config["tianxing_key"]
    today_date,today_weather,today_temp,today_wind,today_tips,\
        tomorrow_date,tomorrow_weather,tomorrow_temp,tomorrow_wind,tomorrow_tips=get_weather(headers,region,key)
    zonghe,aiqing,caiyun,jiankang,gshu=get_xingzuo(headers,key)
    hotpoint1,hotpoint2,hotpoint3=get_hotpoint(headers)
    note_ch = config["note_ch"]
    note_en = config["note_en"]
    # 获取词霸每日金句
    if note_ch == "" and note_en == "":
        note_ch,note_en,note_wanan=get_content(headers,key)
    #获取生日
    b1=bir(config["birthday1"])
    name1=config["name1"]
    if b1==0:
        birthdaydata1 = "今天是%s的生日哦,祝%s生日快乐!"%name1
    else:
        birthdaydata1 = "距离%s的生日还有%s天"%(name1,b1)
    b2=bir(config["birthday2"])
    name2=config["name2"]
    if b2==0:
        birthdaydata2 = "今天是%s的生日哦,祝自己生日快乐!"%name2
    else:
        birthdaydata2 = "距离%s的生日还有%s天"%(name2,b2)

    # 公众号推送消息
    for user in users:
        send_message(user,today_tips,tomorrow_tips,
                 today_date,tomorrow_date,
                 birthdaydata1,birthdaydata2,
                 accessToken,region,
                 today_weather,today_temp,today_wind,
                 tomorrow_weather,tomorrow_temp,tomorrow_wind,
                 zonghe,aiqing,caiyun,jiankang,gshu,
                 hotpoint1,hotpoint2,hotpoint3,
                 note_ch,note_en,note_wanan)
