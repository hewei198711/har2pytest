import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_medal_del(data=data, headers=headers):
    """
    删除公益购勋章
    /mgmt/cms/charity/medal/del

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/charity/medal/del"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
