import requests
import json
from bs4 import BeautifulSoup
from encrypt import encrypt_password
import time  # 新增导入time模块
import schedule  # 新增导入schedule


PUSHPLUS_TOKEN = "" # 你的Token
ID = 1 #校区 淮南1 合肥2
ROOMNUMBER = 0 # 房间号
USERNAME = 0 # 学号
IVPASSWORD = "password" # 密码


def pushplus_notification(token, title, content):
    """
    Pushplus消息推送

    Args:
        token (string): Pushplus Token
        title (string): 消息标题
        content (string): 消息内容
    """
    payload = {
        "token": token,
        "title": title,
        "content": content
    }
    try:
        r = requests.post("http://www.pushplus.plus/send", json=payload)
        # print(r.text)
    except Exception as e:
        print("Pushplus推送失败:", e)
def get_jsessionid():
    """
    获取JSESSIONID

    Returns:
        string : JSESSIONID
    """
    session = requests.session()

    # CAS登录页面的URL
    login_url = "https://authserver.aust.edu.cn/authserver/login?service=http%3A%2F%2Fecard.aust.edu.cn%2Fepay%2Fj_spring_cas_security_check"

    username = USERNAME
    ivpassword = IVPASSWORD

    response = session.get(login_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取隐藏的表单字段
    lt = soup.find('input', {'name': 'lt'})['value']
    execution = soup.find('input', {'name': 'execution'})['value']
    pwdEncryptSalt = soup.find('input', {'id': 'pwdEncryptSalt'})['value']
    _eventId = soup.find('input', {'name': '_eventId'})['value']

    password = encrypt_password(ivpassword, pwdEncryptSalt)

    # 构建登录表单数据
    login_data = {
        'username': username,
        'password': password,
        'lt': lt,
        'execution': execution,
        '_eventId': _eventId,
        'rmShown': '1'
    }
    response = session.post(login_url, data=login_data, allow_redirects=False)

    # 获取重定向URL
    if 'Location' in response.headers:
        redirect_url = response.headers['Location']
        # print("Redirect URL:", redirect_url)

    response = session.get(redirect_url)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    # print("cookie:", cookies)
    return cookies.get('JSESSIONID')

def get_electric_bill():
    """
    获取电费余额

    Returns:
        float : rest_elec_degree
    """
    JSESSIONID = get_jsessionid()
    url = f"http://ecard.aust.edu.cn/epay/electric_simple/queryelectricbill?sysid={ID}&roomNo={ROOMNUMBER}"
    cookies = {
        'JSESSIONID': JSESSIONID,
        'LOGIN': f'{USERNAME}',
        'SCREEN_NAME': 'ZCpfHbVMV7cxjUxle56IkQ==',
        'GUEST_LANGUAGE_ID': 'zh_CN'
    }
    response = requests.get(url, cookies=cookies)
    response_text = response.text.lstrip('\ufeff')
    result = json.loads(response_text)
    rest_elec_degree = result.get('restElecDegree')
    # print(rest_elec_degree)
    return rest_elec_degree


def main():
    rest_elec_degree = get_electric_bill()
    if rest_elec_degree < 10:
        print("电量不足 10 度")
        if PUSHPLUS_TOKEN:
            pushplus_notification(PUSHPLUS_TOKEN, "电量不足通知", f"剩余电量: {rest_elec_degree} 度, 即将为您充值。")
        # from charge import charge_fee
        # charge_fee(0) # 充值金额
    else:
        print(f"电量大于 10 度,剩余电量: {rest_elec_degree} 度")
        # if PUSHPLUS_TOKEN:
        #     pushplus_notification(PUSHPLUS_TOKEN, "电量充足通知", f"剩余电量: {rest_elec_degree} 度。")

if __name__ == '__main__':
    # 定时任务，每2小时执行一次
    schedule.every(2).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

    # 手动执行一次
    # main()