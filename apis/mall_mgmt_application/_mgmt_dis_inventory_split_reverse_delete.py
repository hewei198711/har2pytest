import os
from urllib.parse import urlencode

from util.client import client

data = {
    "reserveId": 0,  # reserveId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_dis_inventory_split_reverse_delete(data=data, headers=headers):
    """
    删除保留套装
    /mgmt/dis-inventory/split/reverse/delete

    参数说明:
    - reserveId: reserveId
    """

    url = "/mgmt/dis-inventory/split/reverse/delete"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
