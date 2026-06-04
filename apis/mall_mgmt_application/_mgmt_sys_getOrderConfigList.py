import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getOrderConfigList(headers=headers):
    """
    获取展示订货或退货设置列表
    /mgmt/sys/getOrderConfigList
    """

    url = "/mgmt/sys/getOrderConfigList"
    with client.get(url=url, headers=headers) as r:
        return r
