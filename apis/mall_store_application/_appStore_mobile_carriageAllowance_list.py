import os

from util.client import client

data = {
    "beginTime": "",  # TODO: 添加参数说明
    "endTime": "",  # TODO: 添加参数说明
    "subsidyReason": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_carriageAllowance_list(data=data, headers=headers):
    """
    运费补贴
    /appStore/mobile/carriageAllowance/list
    """

    url = "/appStore/mobile/carriageAllowance/list"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
