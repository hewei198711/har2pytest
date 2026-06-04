import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_getRemark(headers=headers):
    """
    后台获取活动说明配置
    /mgmt/prmt/shelvesCoupon/getRemark
    """

    url = "/mgmt/prmt/shelvesCoupon/getRemark"
    with client.get(url=url, headers=headers) as r:
        return r
