import os

from util.client import client

data = {
    "descript": "",  # 描述
    "name": "",  # 名称
    "productList": [{"serialNo": "", "sort": 0}],  # 关联的产品列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_recommend_saveRecommend(data=data, headers=headers):
    """
    新增推荐商品
    /mgmt/cms/recommend/saveRecommend

    参数说明:
    - descript: 描述
    - name: 名称
    - productList: 关联的产品列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    """

    url = "/mgmt/cms/recommend/saveRecommend"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
