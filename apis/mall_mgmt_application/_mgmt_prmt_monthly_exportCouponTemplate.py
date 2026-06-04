import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_monthly_exportCouponTemplate(headers=headers):
    """
    下载优惠券导入模板
    /mgmt/prmt/monthly/exportCouponTemplate
    """

    url = "/mgmt/prmt/monthly/exportCouponTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
