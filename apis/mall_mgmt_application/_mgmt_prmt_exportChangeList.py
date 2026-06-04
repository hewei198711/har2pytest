import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "createTimeMax": "",  # 创建时间大
    "createTimeMin": "",  # 创建时间小
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "promotionId": 0,  # 活动id
    "realName": "",  # 会员姓名
    "serialNo": "",  # 商品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_exportChangeList(params=params, headers=headers):
    """
    导出活动顾客列表变化
    /mgmt/prmt/exportChangeList

    参数说明:
    - cardNo: 会员卡号
    - createTimeMax: 创建时间大
    - createTimeMin: 创建时间小
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页条数
    - promotionId: 活动id
    - realName: 会员姓名
    - serialNo: 商品编码
    """

    url = "/mgmt/prmt/exportChangeList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
