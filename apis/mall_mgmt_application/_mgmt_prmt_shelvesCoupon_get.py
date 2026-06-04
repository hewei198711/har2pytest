import os

from util.client import client

params = {
    "getLogs": False,  # 是否获取操作日志，默认值:false
    "id": "",  # 优惠券上架id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_get(params=params, headers=headers):
    """
    查询优惠券上架信息
    /mgmt/prmt/shelvesCoupon/get

    参数说明:
    - getLogs: 是否获取操作日志，默认值:false
    - id: 优惠券上架id
    """

    url = "/mgmt/prmt/shelvesCoupon/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
