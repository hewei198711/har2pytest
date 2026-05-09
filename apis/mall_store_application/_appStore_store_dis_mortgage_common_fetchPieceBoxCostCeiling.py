import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_fetchPieceBoxCostCeiling(headers=headers):
    """
    获取启用中的拼箱费上限
    /appStore/store/dis/mortgage/common/fetchPieceBoxCostCeiling
    """

    url = "/appStore/store/dis/mortgage/common/fetchPieceBoxCostCeiling"
    with client.get(url=url, headers=headers) as r:
        return r
