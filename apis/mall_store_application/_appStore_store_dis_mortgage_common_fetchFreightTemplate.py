import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_fetchFreightTemplate(headers=headers):
    """
    获取最新的运费计算模板
    /appStore/store/dis/mortgage/common/fetchFreightTemplate
    """

    url = "/appStore/store/dis/mortgage/common/fetchFreightTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
