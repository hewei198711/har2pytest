import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_sys_company_enable_batchEnableOrDisable(headers=headers):
    """
    批量 启动 / 禁用
    /mgmt/sys/company/enable/batchEnableOrDisable
    """

    url = "/mgmt/sys/company/enable/batchEnableOrDisable"
    with client.post(url=url, headers=headers) as r:
        return r
