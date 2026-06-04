import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_exportProductTemplate(headers=headers):
    """
    优惠券关联产品导入模板下载
    /mgmt/prmt/coupon/exportProductTemplate
    """

    url = "/mgmt/prmt/coupon/exportProductTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
