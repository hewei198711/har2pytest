import os
from urllib.parse import urlencode

from util.client import client

data = {
    "commentId": 0,  # commentId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_return_delComment(data=data, headers=headers):
    """
    删除留言
    /mgmt/order/return/delComment

    参数说明:
    - commentId: commentId
    """

    url = "/mgmt/order/return/delComment"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
