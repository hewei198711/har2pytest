import os

from util.client import client

params = {
    "instructionsId": 0,  # instructionsId
    "serialNo": "",  # serialNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_instructions_checkDuplicate(params=params, headers=headers):
    """
    查看商品是否已添加过使用说明
    /mgmt/acc/instructions/checkDuplicate

    参数说明:
    - instructionsId: instructionsId
    - serialNo: serialNo
    """

    url = "/mgmt/acc/instructions/checkDuplicate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
