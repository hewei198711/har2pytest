import os

from util.client import client

params = {
    "bannerId": 0,  # bannerId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_banner_restoreBanner_bannerId(params=params, headers=headers):
    """
    恢复Banner
    /mgmt/cms/banner/restoreBanner/{bannerId}

    参数说明:
    - bannerId: bannerId
    """

    url = f"/mgmt/cms/banner/restoreBanner/{params['bannerId']}"
    with client.get(url=url, headers=headers) as r:
        return r
