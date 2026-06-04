import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_medal_get(params=params, headers=headers):
    """
    查询公益购勋章详情
    /mgmt/cms/charity/medal/get

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/charity/medal/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
