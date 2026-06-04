import os

from util.client import client

params = {
    "bannerShelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_banner_list(params=params, headers=headers):
    """
    轮播图列表
    /mgmt/acc/banner/list

    参数说明:
    - bannerShelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    """

    url = "/mgmt/acc/banner/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
