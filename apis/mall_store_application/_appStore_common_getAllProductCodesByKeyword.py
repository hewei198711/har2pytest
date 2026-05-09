import os

from util.client import client

params = {
    "keyword": "",  # 编号或名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getAllProductCodesByKeyword(params=params, headers=headers):
    """
    获取所有匹配的商品编码列表(编号或名称)
    /appStore/common/getAllProductCodesByKeyword

    参数说明:
    - keyword: 编号或名称
    """

    url = "/appStore/common/getAllProductCodesByKeyword"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
