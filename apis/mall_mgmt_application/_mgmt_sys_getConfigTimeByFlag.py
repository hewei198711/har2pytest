import os

from util.client import client

params = {
    "flag": "",  # flag
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getConfigTimeByFlag(params=params, headers=headers):
    """
    获取订货/退货中 订单状态 配置时间 （分）
    /mgmt/sys/getConfigTimeByFlag

    参数说明:
    - flag: flag
    """

    url = "/mgmt/sys/getConfigTimeByFlag"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
