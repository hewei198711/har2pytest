import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_buttonColumn_getButtonColumnMgmtList(headers=headers):
    """
    查询底部栏配置列表
    /mgmt/cms/buttonColumn/getButtonColumnMgmtList
    """

    url = "/mgmt/cms/buttonColumn/getButtonColumnMgmtList"
    with client.get(url=url, headers=headers) as r:
        return r
