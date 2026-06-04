import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_exportPromotionTemplate(headers=headers):
    """
    优惠券关联活动导入模板下载
    /mgmt/prmt/coupon/exportPromotionTemplate
    """

    url = "/mgmt/prmt/coupon/exportPromotionTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
