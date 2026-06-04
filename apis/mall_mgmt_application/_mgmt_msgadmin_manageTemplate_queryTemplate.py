import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_manageTemplate_queryTemplate(params=params, headers=headers):
    """
    查询系统模板接口
    /mgmt/msgadmin/manageTemplate/queryTemplate

    参数说明:
    - key: key
    """

    url = "/mgmt/msgadmin/manageTemplate/queryTemplate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
