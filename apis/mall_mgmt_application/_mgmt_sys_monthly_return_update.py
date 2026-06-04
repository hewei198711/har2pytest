import os

from util.client import client

data = {
    "effectDate": "",  # 生效日期
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_monthly_return_update(data=data, headers=headers):
    """
    修改月结日期
    /mgmt/sys/monthly/return/update

    参数说明:
    - effectDate: 生效日期
    - id: id
    """

    url = "/mgmt/sys/monthly/return/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
