import os
from urllib.parse import urlencode

from util.client import client

data = {
    "file": "",  # 导入文件
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_monthly_importCoupon(data=data, headers=headers):
    """
    导入优惠券
    /mgmt/prmt/monthly/importCoupon

    参数说明:
    - file: 导入文件
    """

    url = "/mgmt/prmt/monthly/importCoupon"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
