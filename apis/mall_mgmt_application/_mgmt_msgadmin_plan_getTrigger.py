import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_plan_getTrigger(headers=headers):
    """
    查询触发类型列表数据内容
    /mgmt/msgadmin/plan/getTrigger
    """

    url = "/mgmt/msgadmin/plan/getTrigger"
    with client.get(url=url, headers=headers) as r:
        return r
