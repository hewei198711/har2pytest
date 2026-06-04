import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_current_user_company_list(headers=headers):
    """
    根据当前用户获取分公司集合
    /mgmt/sys/current/user/company/list
    """

    url = "/mgmt/sys/current/user/company/list"
    with client.get(url=url, headers=headers) as r:
        return r
