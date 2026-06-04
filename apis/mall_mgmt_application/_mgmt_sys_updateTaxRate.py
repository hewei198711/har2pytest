import os

from util.client import client

params = {
    "id": "",  # id
    "taxRate": "",  # 税率值设置必须小于100.00
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateTaxRate(params=params, headers=headers):
    """
    查询所有税率信息
    /mgmt/sys/updateTaxRate

    参数说明:
    - id: id
    - taxRate: 税率值设置必须小于100.00
    """

    url = "/mgmt/sys/updateTaxRate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
