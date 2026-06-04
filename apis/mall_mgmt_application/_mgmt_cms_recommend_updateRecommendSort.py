import os

from util.client import client

data = {
    "serialNo": "",  # 产品编码
    "sort": 0,  # sort
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_recommend_updateRecommendSort(data=data, headers=headers):
    """
    按商品编号修改推荐商品排序
    /mgmt/cms/recommend/updateRecommendSort

    参数说明:
    - serialNo: 产品编码
    - sort: sort
    """

    url = "/mgmt/cms/recommend/updateRecommendSort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
