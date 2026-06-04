import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_city_level_exportImportBatchCityLevelEditFailList(headers=headers):
    """
    导出导入城市等级批量编辑失败列表
    /mgmt/sys/city-level/exportImportBatchCityLevelEditFailList
    """

    url = "/mgmt/sys/city-level/exportImportBatchCityLevelEditFailList"
    with client.get(url=url, headers=headers) as r:
        return r
