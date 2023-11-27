import random
import json
from time import localtime
from requests import get, post
from datetime import datetime,date




# 获取随机颜色
def get_color():
    def get_colors(n):
        return ["#" + "%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    color_list = get_colors(1000)
    return random.choice(color_list)


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
 
 
def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(region, key)
    response = get(region_url, headers=headers).json()
    if response["code"] == "404":
        print("推送消息失败,请检查地区名是否有误!")
    elif response["code"] == "401":
        print("推送消息失败,请检查和风天气key是否正确!")
    else:
        # 获取地区的location--id
        location_id = response["location"][0]["id"]
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, key)
    response = get(weather_url, headers=headers).json()
    # 天气
    weather = response["now"]["text"]
    # 当前温度
    temp = response["now"]["temp"]
    # 风向
    wind_dir = response["now"]["windDir"]
    return weather, temp, wind_dir

#生日在这里
def bir(birthday):
    # 获取当前日期
    now = datetime.now()
    # 获取用户输入的出生日期
    # 将用户输入的出生日期字符串转换为datetime对象
    birthday = datetime.strptime(birthday, "%Y-%m-%d")
    # 计算今年生日的日期
    this_year_birthday = datetime(now.year, birthday.month, birthday.day)
    # 如果今年生日已经过了,则计算明年生日的日期
    if this_year_birthday < now:
        this_year_birthday = datetime(now.year + 1, birthday.month, birthday.day)
    # 计算距离今年生日还有多久时间
    time_to_birthday = this_year_birthday - now
    # 输出结果
    birthday=(time_to_birthday.days)
    return birthday

#今日热搜
urlx='https://apis.tianapi.com/toutiaohot/index?key=0286f08d7d10479012b557d0cf9bb225'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
a=get(urlx,headers)
a=json.loads(a.text)
resou1=a['result']['list'][0]['word']
resou2=a['result']['list'][1]['word']
resou3=a['result']['list'][2]['word']


#今日星座运势
urly='https://apis.tianapi.com/star/index?key=0286f08d7d10479012b557d0cf9bb225&astro=sagittarius'
health=get(urly,headers)
health=json.loads(health.text)
zhe=str(health['result']['list'][0]['content']).replace('%','')
aqing=str(health['result']['list'][1]['content']).replace('%','')
cyun=str(health['result']['list'][3]['content']).replace('%','')
jkang=str(health['result']['list'][4]['content']).replace('%','')
gshu=str(health['result']['list'][8]['content'])


  
def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en
 
 
def send_message(to_user,notex,birthdaydata1,birthdaydata2,access_token,region_name,weather,temp,wind_dir,zhe,aqing,cyun,jkang,gshu,resou1,resou2,resou3,note_ch,note_en):
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
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{}".format(today),
                "color": get_color()
            },
            "region": {
                "value": region_name,
                "color": get_color()
            },
            "birthdaydata1": {
                "value": birthdaydata1,
                "color": get_color()
            },
            "birthdaydata2": {
                "value": birthdaydata2,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "notex": {
                "value": notex,
                "color": get_color()
            },
            "temp": {
                "value": temp,
                "color": get_color()
            },
            "wind_dir": {
                "value": wind_dir,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },
            "zhe": {
                "value": zhe,
                "color": get_color()
            },
            "cyun": {
                "value": cyun,
                "color": get_color()
            },
            "jkang": {
                "value": jkang,
                "color": get_color()
            },
            "aqing": {
                "value": aqing,
                "color": get_color()
            },
            "gshu": {
                "value": gshu,
                "color": get_color()
            },
            "resou1": {
                "value": resou1,
                "color": get_color()
            },
            "resou2": {
                "value": resou2,
                "color": get_color()
            },
            "resou3": {
                "value": resou3,
                "color": get_color()
            },
            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch": {
                "value": note_ch,
                "color": get_color()
            }
        }
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
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败,请检查config.txt文件是否与程序位于同一路径")
    except SyntaxError:
        print("推送消息失败,请检查配置文件格式是否正确")

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入地区获取天气信息
    region = config["region"]
    weather, temp, wind_dir = get_weather(region)
    note_ch = config["note_ch"]
    note_en = config["note_en"]
    # 获取词霸每日金句
    if note_ch == "" and note_en == "":
        note_ch, note_en = get_ciba()
    #获取生日
    b1=bir(config["birthday1"])
    if b1==0:
        birthdaydata1 = "今天是欣怡宝宝的生日哦,祝欣怡宝宝生日快乐!"
    else:
        birthdaydata1 = "距离欣怡的生日还有%s天"%b1
    b2=bir(config["birthday2"])
    if b2==0:
        birthdaydata2 = "今天是夕超的生日哦,祝自己生日快乐!"
    else:
        birthdaydata2 = "距离夕超的生日还有%s天"%b2
    #获取提醒
    if(weather=="阴" and int(temp)<=15):
        notex="今天天气比较冷,记得多穿件衣服"
    elif(weather=="晴" and int(temp)>=25):
        notex="今天会很热,可以带把伞遮太阳"
    elif(weather=="小雨" or weather=="中雨" or weather=="大雨"):
        notex="今天会下雨哦,记得带伞"
    elif((weather=="小雪" or weather=="中雪" or weather=="大雪")and int(temp)<=5):
        notex="今天会下雪哦,多穿衣服也可以打打雪仗"
    elif(int(temp)<=5):
        notex="今天会很冷,得多穿几件衣服"
    elif(int(temp)>=30):
        notex="今天特别热,注意不要中暑了,记得多喝水"
    elif(18<=int(temp)<=20):
        notex="今天天气应该会很舒服喔"
    else:
        notex="好像没有需要特别注意的,那就祝你开心啦"
    
    # ########更改推送时间⬇️
    # week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    # yearx = localtime().tm_year
    # monthx = localtime().tm_mon
    # dayx = localtime().tm_mday
    # today = datetime.date(datetime(year=yearx, month=monthx, day=dayx))
    # week = week_list[today.isoweekday() % 7]
    # with open('.github\\workflows\\weixin.yml', 'r',encoding='utf-8') as f:
    #     lines = f.readlines()

    # if week in ["星期日","星期一","星期二"]:
    #     lines[5] = "    - cron: '30 23 * * *'\n"  # 修改第6行的内容为七点半推送
    # elif week in ["星期三","星期四","星期五","星期六"]:
    #     lines[5] = "    - cron: '30 1 * * *'\n"  # 修改第6行的内容为九点半推送

    # with open('.github\\workflows\\weixin.yml', 'w',encoding='utf-8') as f:
    #     f.writelines(lines)
    # ########更改推送时间⬆️


    # 公众号推送消息
    for user in users:
        send_message(user,notex,
                     birthdaydata1,birthdaydata2,
                     accessToken,region,
                     weather,temp,wind_dir,
                     zhe,aqing,cyun,jkang,gshu,
                     resou1,resou2,resou3,
                     note_ch,note_en)
