import os

from util.client import client

data = {
    "commitTimeBegin": "",  # 下单开始时间 #格式yyyy-MM-dd
    "commitTimeEnd": "",  # 下单结束时间 #格式yyyy-MM-dd
    "customerCard": "",  # 会员卡号
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "receiverPhone": "",  # 收货人手机号
    "registerNo": "",  # 登记人工号
    "registerTimeBegin": "",  # 登记开始时间 #格式yyyy-MM-dd
    "registerTimeEnd": "",  # 登记结束时间 #格式yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_return_register_returnRegisterExport(data=data, headers=headers):
    """
    手工登记退货信息导出
    /mgmt/return/register/returnRegisterExport

    参数说明:
    - commitTimeBegin: 下单开始时间 #格式yyyy-MM-dd
    - commitTimeEnd: 下单结束时间 #格式yyyy-MM-dd
    - customerCard: 会员卡号
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - receiverPhone: 收货人手机号
    - registerNo: 登记人工号
    - registerTimeBegin: 登记开始时间 #格式yyyy-MM-dd
    - registerTimeEnd: 登记结束时间 #格式yyyy-MM-dd
    """

    url = "/mgmt/return/register/returnRegisterExport"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
