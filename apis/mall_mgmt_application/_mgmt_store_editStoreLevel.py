import os

from util.client import client

data = {
    "cancelTime": "",  # 取消日期
    "cancelType": 0,  # 取消类型: 1、结点取消，2、转让取消，3、违规取消，4、不达标取消，5、冻结取消，6、转云取消
    "id": 0,  # 主键ID
    "level": 0,  # 网点等级 1服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_editStoreLevel(data=data, headers=headers):
    """
    编辑网点等级
    /mgmt/store/editStoreLevel

    参数说明:
    - cancelTime: 取消日期
    - cancelType: 取消类型: 1、结点取消，2、转让取消，3、违规取消，4、不达标取消，5、冻结取消，6、转云取消
    - id: 主键ID
    - level: 网点等级 1服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店
    """

    url = "/mgmt/store/editStoreLevel"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
