import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_importPromotionMemberTemplate(headers=headers):
    """
    导入活动用户模板下载
    /mgmt/prmt/importPromotionMemberTemplate
    """

    url = "/mgmt/prmt/importPromotionMemberTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
