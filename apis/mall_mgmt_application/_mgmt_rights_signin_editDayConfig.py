import os

from util.client import client

data = {
    "addQuantity": 0,  # 逐日增加金豆数量
    "id": 0,  # 配置id
    "initQuantity": 0,  # 开始金豆数量
    "limitQuantity": 0,  # 上限金豆数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_rights_signin_editDayConfig(data=data, headers=headers):
    """
    编辑每日签到奖励配置
    /mgmt/rights/signin/editDayConfig

    参数说明:
    - addQuantity: 逐日增加金豆数量
    - id: 配置id
    - initQuantity: 开始金豆数量
    - limitQuantity: 上限金豆数量
    """

    url = "/mgmt/rights/signin/editDayConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
