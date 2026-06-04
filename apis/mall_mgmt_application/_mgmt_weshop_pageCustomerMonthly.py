import os

from util.client import client

data = {
    "customerCard": "",  # 顾客卡号
    "customerIdCard": "",  # 顾客身份证号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "from": 0,  # TODO: 添加参数说明
    "id": 0,  # TODO: 添加参数说明
    "month": "",  # 月份，yyyy-MM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "serialNo": "",  # 商品编码
    "title": "",  # 商品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_pageCustomerMonthly(data=data, headers=headers):
    """
    分页查询微信小店月结报表-卡号维度
    /mgmt/weshop/pageCustomerMonthly

    参数说明:
    - customerCard: 顾客卡号
    - customerIdCard: 顾客身份证号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - month: 月份，yyyy-MM
    - pageNum: 页数
    - pageSize: 每页显示数
    - serialNo: 商品编码
    - title: 商品名称
    """

    url = "/mgmt/weshop/pageCustomerMonthly"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
