import requests
from bs4 import BeautifulSoup
from main import ROOMNUMBER, BUILDINGNUMBER, ID, get_jsessionid, get_electric_bill

def charge_fee(money):
    """
    充值电费

    Args:
        money (number): 充值金额
    """
    session = requests.session()
    JSESSIONID = get_jsessionid()
    epay_url = "http://ecard.aust.edu.cn/epay/index/persontop.jsp"
    cookies = {
        'JSESSIONID': JSESSIONID,
    }
    response = session.get(epay_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    _csrf = soup.find('input', {'name': '_csrf'})['value']
    # print(_csrf)
    data = {
        'elcsysid': '1',
        'roomNo': ROOMNUMBER,
        'dumpEnergy': get_electric_bill(),
        'route':'',
        'paidMoney': money,
        '_csrf': _csrf
    }
    # 合肥校区未经测试，请自行测试
    # hefei_data = {
    #     'elcsysid': '2',
    #     'elcarea': 101,
    #     'elcbuis': BUILDINGNUMBER,
    #     'roomNo': ROOMNUMBER,
    #     'dumpEnergy': get_electric_bill(),
    #     'paidMoney': money,
    #     'route':'',
    #     '_csrf': _csrf
    # }
    bill_url = "http://ecard.aust.edu.cn/epay/electric_simple/load4paidelectricbill"
    if ID == 1:
        res = session.post(bill_url, data=data, cookies=cookies)
    # if ID == 2:
    #     res = session.post(bill_url, data=hefei_data, cookies=cookies)
    # print(res.text)
    soup1 = BeautifulSoup(res.text, 'html.parser')
    billno = soup1.find('input', {'name': 'billno'})['value']
    refno = soup1.find('input', {'name': 'refno'})['value']
    confirm_data = {
        'billno': billno,
        'refno': refno,
        'status': 0,
        '_csrf': _csrf
    }
    confirm_url = "http://ecard.aust.edu.cn/epay/electric_simple/payconfirm"
    confirm_res = session.post(confirm_url, data=confirm_data, cookies=cookies)
    print(confirm_res.text)
    print(f"充值成功了{money}元")
    balance_soup = BeautifulSoup(confirm_res.text, 'html.parser')
    balance_tags = balance_soup.find_all('span', {'class': 'c_3497ea'})
    count = 0
    for tag in balance_tags:
        if any(char.isdigit() for char in tag.text):
            count += 1
            if count == 2:
                balance = tag.text.strip()
                print(f"可支付余额: {balance} 元")
                break
    else:
        print("未找到余额信息")

if __name__ == '__main__':
    charge_fee() # 请填入充值金额