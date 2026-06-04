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


def _mgmt_sys_monthly_return_save(data=data, headers=headers):
    """
    新增月结日期
    /mgmt/sys/monthly/return/save

    参数说明:
    - effectDate: 生效日期
    - id: id
    """

    url = "/mgmt/sys/monthly/return/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
