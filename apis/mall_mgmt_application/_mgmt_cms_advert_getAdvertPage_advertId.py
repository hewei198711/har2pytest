import os

from util.client import client

params = {
    "advertId": 0,  # advertId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_advert_getAdvertPage_advertId(params=params, headers=headers):
    """
    获取广告页
    /mgmt/cms/advert/getAdvertPage/{advertId}

    参数说明:
    - advertId: advertId
    """

    url = f"/mgmt/cms/advert/getAdvertPage/{params['advertId']}"
    with client.get(url=url, headers=headers) as r:
        return r
