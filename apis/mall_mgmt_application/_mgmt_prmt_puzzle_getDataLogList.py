import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "createTimeMax": "",  # 创建时间末
    "createTimeMin": "",  # 创建时间始
    "memberType": 0,  # 顾客身份 1->会员；2->VIP会员；3->云商；4->微店（云+）
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "puzzleId": 0,  # 拼图活动id
    "result": 0,  # 拼图结果是否正确 0-错误 1-正确
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_puzzle_getDataLogList(data=data, headers=headers):
    """
    用户参与记录
    /mgmt/prmt/puzzle/getDataLogList

    参数说明:
    - cardNo: 会员卡号
    - createTimeMax: 创建时间末
    - createTimeMin: 创建时间始
    - memberType: 顾客身份 1->会员；2->VIP会员；3->云商；4->微店（云+）
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - puzzleId: 拼图活动id
    - result: 拼图结果是否正确 0-错误 1-正确
    """

    url = "/mgmt/prmt/puzzle/getDataLogList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
