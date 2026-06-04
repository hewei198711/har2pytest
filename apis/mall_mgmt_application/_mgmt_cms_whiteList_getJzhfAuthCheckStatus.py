import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_whiteList_getJzhfAuthCheckStatus(headers=headers):
    """
    获取精准护肤白名单检测开关状态
    /mgmt/cms/whiteList/getJzhfAuthCheckStatus
    """

    url = "/mgmt/cms/whiteList/getJzhfAuthCheckStatus"
    with client.post(url=url, headers=headers) as r:
        return r
