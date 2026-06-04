import os

from util.client import client

data = {
    "sendDay": 0,  # 推送日
    "sendMonth": 0,  # 推送月
    "sendType": 0,  # 推送类型：1/每年，2/每季，3/每月
    "signType": 0,  # 对账单签署类型，1/1:3对账单，2/85%对账单，3/85%账款对账单，4/钱包对账单
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_updateBillJob(data=data, headers=headers):
    """
    修改对账单定时推送记录
    /mgmt/store/updateBillJob

    参数说明:
    - sendDay: 推送日
    - sendMonth: 推送月
    - sendType: 推送类型：1/每年，2/每季，3/每月
    - signType: 对账单签署类型，1/1:3对账单，2/85%对账单，3/85%账款对账单，4/钱包对账单
    """

    url = "/mgmt/store/updateBillJob"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
