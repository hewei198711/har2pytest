import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_libertySale_delete(data=data, headers=headers):
    """
    删除活动
    /mgmt/prmt/libertySale/delete

    参数说明:
    - id: 活动id
    """

    url = "/mgmt/prmt/libertySale/delete"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
