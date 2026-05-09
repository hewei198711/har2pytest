import os

from util.client import client

params = {
    "orderSn": "",  # orderSn
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_store_dis_mortgageOrder_readFeedbackReply_orderSn(params=params, headers=headers):
    """
    押货单反馈回复阅读(修改状态为已读)
    /appStore/store/dis/mortgageOrder/readFeedbackReply/{orderSn}

    参数说明:
    - orderSn: orderSn
    """

    url = f"/appStore/store/dis/mortgageOrder/readFeedbackReply/{params['orderSn']}"
    with client.get(url=url, headers=headers) as r:
        return r
