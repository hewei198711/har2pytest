import os

from util.client import client

params = {
    "floorPageId": 0,  # floorPageId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_floor_removeFloorPage_floorPageId(params=params, headers=headers):
    """
    删除楼层页
    /mgmt/cms/floor/removeFloorPage/{floorPageId}

    参数说明:
    - floorPageId: floorPageId
    """

    url = f"/mgmt/cms/floor/removeFloorPage/{params['floorPageId']}"
    with client.get(url=url, headers=headers) as r:
        return r
