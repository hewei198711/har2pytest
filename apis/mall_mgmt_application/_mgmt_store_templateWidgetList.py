import os

from util.client import client

params = {
    "templateNo": "",  # 模板编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_templateWidgetList(params=params, headers=headers):
    """
    查看合同模板填充
    /mgmt/store/templateWidgetList

    参数说明:
    - templateNo: 模板编号
    """

    url = "/mgmt/store/templateWidgetList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
