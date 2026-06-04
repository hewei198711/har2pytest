import os

from util.client import client

data = {
    "comment": "",  # 留言内容
    "id": 0,  # 留言id
    "serviceNo": "",  # 退货/换货单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_saveComment(data=data, headers=headers):
    """
    新增/修改留言
    /mgmt/order/return/saveComment

    参数说明:
    - comment: 留言内容
    - id: 留言id
    - serviceNo: 退货/换货单号
    """

    url = "/mgmt/order/return/saveComment"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
