import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getPopUpTypeList(headers=headers):
    """
    获取弹窗类型列表
    /mgmt/cms/getPopUpTypeList
    """

    url = "/mgmt/cms/getPopUpTypeList"
    with client.get(url=url, headers=headers) as r:
        return r
