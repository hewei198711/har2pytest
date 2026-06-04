import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_freightTemplate_list(headers=headers):
    """
    查询运费模板列表
    /mgmt/sys/freightTemplate/list
    """

    url = "/mgmt/sys/freightTemplate/list"
    with client.get(url=url, headers=headers) as r:
        return r
