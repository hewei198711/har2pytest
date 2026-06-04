import os

from util.client import client

params = {
    "shareContentId": 0,  # shareContentId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_orderShareContent_editContent_shareContentId(params=params, headers=headers):
    """
    编辑订单分享文案
    /mgmt/cms/orderShareContent/editContent/{shareContentId}

    参数说明:
    - content: 内容文案
    - shareContentId: shareContentId
    """

    url = f"/mgmt/cms/orderShareContent/editContent/{params['shareContentId']}"
    with client.get(url=url, headers=headers) as r:
        return r
