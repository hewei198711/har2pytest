import os

from util.client import client

params = {
    "thematicId": 0,  # thematicId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_thematic_removeThematicBar_thematicId(params=params, headers=headers):
    """
    删除专题页
    /mgmt/cms/thematic/removeThematicBar/{thematicId}

    参数说明:
    - thematicId: thematicId
    """

    url = f"/mgmt/cms/thematic/removeThematicBar/{params['thematicId']}"
    with client.get(url=url, headers=headers) as r:
        return r
