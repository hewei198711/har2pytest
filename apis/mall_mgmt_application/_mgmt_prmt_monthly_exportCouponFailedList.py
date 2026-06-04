import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_monthly_exportCouponFailedList(params=params, headers=headers):
    """
    下载优惠券不可导入列表
    /mgmt/prmt/monthly/exportCouponFailedList

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/monthly/exportCouponFailedList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
