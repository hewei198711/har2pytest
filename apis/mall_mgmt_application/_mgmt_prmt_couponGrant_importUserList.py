import os
from urllib.parse import urlencode

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "file": "",  # 顾客文件
    "grantId": 0,  # 派发记录id
    "type": 0,  # 派发方式1等量2按需
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_couponGrant_importUserList(data=data, headers=headers):
    """
    导入优惠券派发用户
    /mgmt/prmt/couponGrant/importUserList

    参数说明:
    - couponId: 优惠券id
    - file: 顾客文件
    - grantId: 派发记录id
    - type: 派发方式1等量2按需
    """

    url = "/mgmt/prmt/couponGrant/importUserList"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
