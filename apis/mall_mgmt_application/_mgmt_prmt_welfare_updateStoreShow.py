import os

from util.client import client

params = {
    "state": "",  # 显示状态 true-显示 false-隐藏
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_welfare_updateStoreShow(params=params, headers=headers):
    """
    更新店铺爱心守护池显示控制:true-显示 false-隐藏
    /mgmt/prmt/welfare/updateStoreShow

    参数说明:
    - state: 显示状态 true-显示 false-隐藏
    """

    url = "/mgmt/prmt/welfare/updateStoreShow"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
