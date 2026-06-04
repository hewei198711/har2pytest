import os

from util.client import client

params = {
    "beginDate": "",  # 开始时间
    "customerCard": "",  # 顾客卡号/姓名
    "customerCards": [],  # 顾客卡号/姓名列表
    "endDate": "",  # 结束时间
    "financeCompanyCode": "",  # 订单财务分公司编码
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_exportOrderSelfStoreDiffSumList(params=params, headers=headers):
    """
    顾客自购门店自提订单分公司不一致（汇总表）
    /mgmt/order/exportOrderSelfStoreDiffSumList

    参数说明:
    - beginDate: 开始时间
    - customerCard: 顾客卡号/姓名
    - customerCards: 顾客卡号/姓名列表
    - endDate: 结束时间
    - financeCompanyCode: 订单财务分公司编码
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/order/exportOrderSelfStoreDiffSumList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
