import os

from util.client import client

params = {
    "bannerId": 0,  # bannerId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_banner_fullRemoveBanner_bannerId(params=params, headers=headers):
    """
    彻底删除Banner
    /mgmt/cms/banner/fullRemoveBanner/{bannerId}

    参数说明:
    - bannerId: bannerId
    """

    url = f"/mgmt/cms/banner/fullRemoveBanner/{params['bannerId']}"
    with client.get(url=url, headers=headers) as r:
        return r
