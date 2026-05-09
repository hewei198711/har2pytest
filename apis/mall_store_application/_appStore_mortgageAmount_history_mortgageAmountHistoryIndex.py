import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mortgageAmount_history_mortgageAmountHistoryIndex(headers=headers):
    """
    押货额度个人首页
    /appStore/mortgageAmount/history/mortgageAmountHistoryIndex
    """

    url = "/appStore/mortgageAmount/history/mortgageAmountHistoryIndex"
    with client.get(url=url, headers=headers) as r:
        return r
