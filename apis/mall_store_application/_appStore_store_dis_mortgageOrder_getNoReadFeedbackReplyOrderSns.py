import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_getNoReadFeedbackReplyOrderSns(headers=headers):
    """
    押货单反馈回复查询(未查阅的)
    /appStore/store/dis/mortgageOrder/getNoReadFeedbackReplyOrderSns
    """

    url = "/appStore/store/dis/mortgageOrder/getNoReadFeedbackReplyOrderSns"
    with client.get(url=url, headers=headers) as r:
        return r
