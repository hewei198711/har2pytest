import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_exportBatchCityLevelEditTemplate(headers=headers):
    """
    城市等级批量编辑导入模板下载
    /mgmt/sys/city-level/exportBatchCityLevelEditTemplate
    """

    url = "/mgmt/sys/city-level/exportBatchCityLevelEditTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
