import os

from util.client import client

params = {
    "location": 0,  # 显示位置，1：PC商城首页，2：APP，3：小程序
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "shelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_banner_getBannerList(params=params, headers=headers):
    """
    获取Banner列表
    /mgmt/cms/banner/getBannerList

    参数说明:
    - location: 显示位置，1：PC商城首页，2：APP，3：小程序
    - pageNum: 页码
    - pageSize: 每页页数
    - shelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    """

    url = "/mgmt/cms/banner/getBannerList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
