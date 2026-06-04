import os

from util.client import client

params = {
    "companyCode": "",  # 公司编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getAccountList(params=params, headers=headers):
    """
    查询分公司银行账号
    /mgmt/sys/getAccountList

    参数说明:
    - companyCode: 公司编码
    """

    url = "/mgmt/sys/getAccountList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
