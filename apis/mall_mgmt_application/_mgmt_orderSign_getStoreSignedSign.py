import os

from util.client import client

params = {
    "businessMode": 0,  # 保证金类型，1=1:3，2=85%,不传=全部
    "leaderId": 0,  # 管理员id, 85%才需要
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_getStoreSignedSign(params=params, headers=headers):
    """
    根据服务中心编号查询已经签约单情况
    /mgmt/orderSign/getStoreSignedSign

    参数说明:
    - businessMode: 保证金类型，1=1:3，2=85%,不传=全部
    - leaderId: 管理员id, 85%才需要
    - storeCode: 服务中心编号
    """

    url = "/mgmt/orderSign/getStoreSignedSign"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
