import os

from util.client import client

params = {
    "createEndTime": "",  # 创建时间(结束)
    "createStartTime": "",  # 创建时间(开始)
    "instructionsShelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
    "productSerialNo": "",  # 关联产品编号
    "updateEndTime": "",  # 修改时间(结束)
    "updateStartTime": "",  # 修改时间(开始)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_instructions_list(params=params, headers=headers):
    """
    获取产品使用说明列表
    /mgmt/acc/instructions/list

    参数说明:
    - createEndTime: 创建时间(结束)
    - createStartTime: 创建时间(开始)
    - instructionsShelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - productSerialNo: 关联产品编号
    - updateEndTime: 修改时间(结束)
    - updateStartTime: 修改时间(开始)
    """

    url = "/mgmt/acc/instructions/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
