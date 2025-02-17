import requests
import json
from bs4 import BeautifulSoup
from encrypt import encrypt_password

def get_jsessionid(username,ivpassword):
    """
    获取JSESSIONID

    Args:
        username (number): 学号
        ivpassword (string): 密码

    Returns:
        string : JSESSIONID
    """
    session = requests.session()

    # CAS登录页面的URL
    login_url = "https://authserver.aust.edu.cn/authserver/login?service=http%3A%2F%2Fecard.aust.edu.cn%2Fepay%2Fj_spring_cas_security_check"

    username = username
    ivpassword = ivpassword

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

def get_electric_bill(id, roomNumber, username, ivpassword):
    """
    获取剩余度数信息

    Args:
        id (number): 固定值1
        roomNumber (number): 宿舍房间号
        username (number): 学号
        ivpassword (string): 密码

    """
    JSESSIONID = get_jsessionid(username, ivpassword)
    url = f"http://ecard.aust.edu.cn/epay/electric_simple/queryelectricbill?sysid={id}&roomNo={roomNumber}"
    cookies = {
        'JSESSIONID': JSESSIONID,
        'LOGIN': f'{username}',
        'SCREEN_NAME': 'ZCpfHbVMV7cxjUxle56IkQ==',
        'GUEST_LANGUAGE_ID': 'zh_CN'
    }
    response = requests.get(url, cookies=cookies)
    response_text = response.text.lstrip('\ufeff')
    result = json.loads(response_text)
    rest_elec_degree = result.get('restElecDegree')
    if rest_elec_degree <10 :
        print("电量不足10度,请及时充值")
    print(rest_elec_degree)


if __name__ == '__main__':
    get_electric_bill(1, 1, 1, '密码') # 填写正确的房间号(num)，学号(num)和密码(str)