import os

from util.client import client

data = {
    "id": 0,  # TODO: 添加参数说明
    "itemFileList": [{"fileName": "", "fileSize": "", "fileUrl": "", "id": 0, "logicLabel": 0}],  # 服务项目文件列表
    "itemName": "",  # 项目名称
    "itemProductList": [{"id": 0, "logicLabel": 0, "serialNo": ""}],  # 服务项目管理产品列表
    "itemShelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
    "itemSkuList": [{"id": 0, "itemAmount": 0.0, "logicLabel": 0, "skuName": ""}],  # 服务项目规格列表
    "itemSort": 0,  # 项目排序
    "itemUnit": "",  # 服务单位
    "remarks": "",  # 服务说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_item_add(data=data, headers=headers):
    """
    新增服务项目内容
    /mgmt/acc/item/add

    参数说明:
    - itemFileList: 服务项目文件列表
    - itemFileList.fileName: 文件名称
    - itemFileList.fileSize: 文件大小 例：200kb
    - itemFileList.fileUrl: 文件地址
    - itemFileList.id: 项目文件ID
    - itemFileList.logicLabel: 逻辑删除 1：正常（默认）0：删除
    - itemName: 项目名称
    - itemProductList: 服务项目管理产品列表
    - itemProductList.id: 项目关联产品Id
    - itemProductList.logicLabel: 逻辑删除 1：正常（默认）0：删除
    - itemProductList.serialNo: 关联商品编码
    - itemShelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    - itemSkuList: 服务项目规格列表
    - itemSkuList.id: 项目规格Id
    - itemSkuList.itemAmount: 最高单价
    - itemSkuList.logicLabel: 逻辑删除 1：正常（默认）0：删除
    - itemSkuList.skuName: 项目规格名称
    - itemSort: 项目排序
    - itemUnit: 服务单位
    - remarks: 服务说明
    """

    url = "/mgmt/acc/item/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
