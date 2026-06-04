import os

from util.client import client

data = {
    "bannerId": 0,  # BannerID
    "shelfStatus": 0,  # 上下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_banner_shelfOff(data=data, headers=headers):
    """
    Banner下架
    /mgmt/cms/banner/shelfOff

    参数说明:
    - bannerId: BannerID
    - shelfStatus: 上下架
    """

    url = "/mgmt/cms/banner/shelfOff"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
