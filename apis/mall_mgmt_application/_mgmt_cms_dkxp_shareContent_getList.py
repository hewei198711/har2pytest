import os

from util.client import client

params = {
    "category": 0,  # 内容分类 1：分享好友内容配置，2：保存图像内容配置
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_dkxp_shareContent_getList(params=params, headers=headers):
    """
    按分类获取代客选品分享内容配置列表
    /mgmt/cms/dkxp/shareContent/getList

    参数说明:
    - category: 内容分类 1：分享好友内容配置，2：保存图像内容配置
    """

    url = "/mgmt/cms/dkxp/shareContent/getList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
