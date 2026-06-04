import os

from util.client import client

params = {
    "planCode": "",  # planCode
    "receiverName": "",  # receiverName
    "receiverUrl": "",  # receiverUrl
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_receiverInsert(params=params, headers=headers):
    """
    导入名单入库
    /mgmt/msgadmin/handmade/receiverInsert

    参数说明:
    - planCode: planCode
    - receiverName: receiverName
    - receiverUrl: receiverUrl
    """

    url = "/mgmt/msgadmin/handmade/receiverInsert"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
