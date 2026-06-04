import os

from util.client import client

data = {
    "answerResult": 0,  # 回答结果(0:错误；1：正确)
    "customerCard": "",  # 会员卡号
    "memberType": 0,  # 顾客身份
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_passwordActivity_exportUserAnswerRecords(data=data, headers=headers):
    """
    导出口令活动用户回答记录
    /mgmt/prmt/passwordActivity/exportUserAnswerRecords

    参数说明:
    - answerResult: 回答结果(0:错误；1：正确)
    - customerCard: 会员卡号
    - memberType: 顾客身份
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页数量
    - promotionId: 活动id
    """

    url = "/mgmt/prmt/passwordActivity/exportUserAnswerRecords"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
