import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_exportMemberTemplate(headers=headers):
    """
    登录有礼活动导入顾客模板下载
    /mgmt/prmt/loginGift/exportMemberTemplate
    """

    url = "/mgmt/prmt/loginGift/exportMemberTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
