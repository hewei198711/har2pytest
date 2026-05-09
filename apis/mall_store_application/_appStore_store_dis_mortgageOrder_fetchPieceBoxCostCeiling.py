import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_fetchPieceBoxCostCeiling(headers=headers):
    """
    获取启用中的拼箱费上限
    /appStore/store/dis/mortgageOrder/fetchPieceBoxCostCeiling
    """

    url = "/appStore/store/dis/mortgageOrder/fetchPieceBoxCostCeiling"
    with client.get(url=url, headers=headers) as r:
        return r
