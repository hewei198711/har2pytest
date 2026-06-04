import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_buttonColumn_getButtonColumnMgmt_id(params=params, headers=headers):
    """
    获取底部栏配置详情
    /mgmt/cms/buttonColumn/getButtonColumnMgmt/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/buttonColumn/getButtonColumnMgmt/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
