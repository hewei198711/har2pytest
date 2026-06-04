import os

from util.client import client

params = {
    "floorPageId": 0,  # floorPageId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_floor_getFloorPageById_floorPageId(params=params, headers=headers):
    """
    根据ID查询楼层
    /mgmt/cms/floor/getFloorPageById/{floorPageId}

    参数说明:
    - floorPageId: floorPageId
    """

    url = f"/mgmt/cms/floor/getFloorPageById/{params['floorPageId']}"
    with client.get(url=url, headers=headers) as r:
        return r
