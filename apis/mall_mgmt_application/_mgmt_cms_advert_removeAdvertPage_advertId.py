import os

from util.client import client

params = {
    "advertId": 0,  # advertId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_advert_removeAdvertPage_advertId(params=params, headers=headers):
    """
    删除广告页
    /mgmt/cms/advert/removeAdvertPage/{advertId}

    参数说明:
    - advertId: advertId
    """

    url = f"/mgmt/cms/advert/removeAdvertPage/{params['advertId']}"
    with client.get(url=url, headers=headers) as r:
        return r
