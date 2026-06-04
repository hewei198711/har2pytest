import os

from util.client import client

params = {
    "promotionId": "",  # 3S活动主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_getOperateLogs(params=params, headers=headers):
    """
    获取3S活动阶梯编辑记录
    /mgmt/prmt/combine/getOperateLogs

    参数说明:
    - promotionId: 3S活动主键id
    """

    url = "/mgmt/prmt/combine/getOperateLogs"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
