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
    "queryType": 0,  # 查询月结报表类型：1-产品维度，2-卡号维度
    "serialNo": "",  # 商品编码
    "title": "",  # 商品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_pageMonthlyDetail(data=data, headers=headers):
    """
    分页查询微信小店月结报表详细
    /mgmt/weshop/pageMonthlyDetail

    参数说明:
    - customerCard: 顾客卡号
    - customerIdCard: 顾客身份证号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - month: 月份，yyyy-MM
    - pageNum: 页数
    - pageSize: 每页显示数
    - queryType: 查询月结报表类型：1-产品维度，2-卡号维度
    - serialNo: 商品编码
    - title: 商品名称
    """

    url = "/mgmt/weshop/pageMonthlyDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
