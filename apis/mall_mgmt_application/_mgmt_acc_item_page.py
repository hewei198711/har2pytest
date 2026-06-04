import os

from util.client import client

params = {
    "createEndTime": "",  # 创建时间(结束)
    "createStartTime": "",  # 创建时间(开始)
    "itemName": "",  # 服务名称
    "itemShelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
    "itemSort": 0,  # 项目排序
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "updateEndTime": "",  # 修改时间(结束)
    "updateStartTime": "",  # 修改时间(开始)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_item_page(params=params, headers=headers):
    """
    分页获取服务项目列表
    /mgmt/acc/item/page

    参数说明:
    - createEndTime: 创建时间(结束)
    - createStartTime: 创建时间(开始)
    - itemName: 服务名称
    - itemShelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - itemSort: 项目排序
    - pageNum: 页数
    - pageSize: 页大小
    - updateEndTime: 修改时间(结束)
    - updateStartTime: 修改时间(开始)
    """

    url = "/mgmt/acc/item/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
