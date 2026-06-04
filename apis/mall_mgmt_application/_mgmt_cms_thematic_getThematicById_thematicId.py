import os

from util.client import client

params = {
    "thematicId": 0,  # thematicId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_thematic_getThematicById_thematicId(params=params, headers=headers):
    """
    根据ID查询专题
    /mgmt/cms/thematic/getThematicById/{thematicId}

    参数说明:
    - thematicId: thematicId
    """

    url = f"/mgmt/cms/thematic/getThematicById/{params['thematicId']}"
    with client.get(url=url, headers=headers) as r:
        return r
