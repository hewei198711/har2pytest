import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_sys_city_level_importBatchCityLevelEdit(headers=headers):
    """
    城市等级批量编辑导入
    /mgmt/sys/city-level/importBatchCityLevelEdit
    """

    url = "/mgmt/sys/city-level/importBatchCityLevelEdit"
    with client.post(url=url, headers=headers) as r:
        return r
