import os

from util.client import client

data = {
    "infoDto": {
        "businessArea": 0.0,
        "isLed": 0,
        "isSign": 0,
        "propertyType": 0,
        "rentMoney": 0.0,
        "rentTime": 0.0,
        "shopType": 0,
        "signLength": 0.0,
        "signWidth": 0.0,
        "totalArea": 0.0,
    },  # 搬迁店铺详细信息
    "movePicDto": {"noSignPic": [], "storeMeasurePic": []},  # 搬迁相关图
    "storeMoveDto": {
        "companyCode": "",
        "companyName": "",
        "currentAddr": "",
        "detailedAddr": "",
        "leaderCardNo": "",
        "leaderName": "",
        "moveReason": "",
        "newShopAddr": "",
        "port": 0,
        "storeCode": "",
        "storeName": "",
    },  # 搬迁申请信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_webAndApp_store_move_addStoreMoveApply(data=data, headers=headers):
    """
    添加搬迁申请记录(成功的话返回id)--web,app
    /appStore/webAndApp/store/move/addStoreMoveApply

    参数说明:
    - infoDto: 搬迁店铺详细信息
    - infoDto.businessArea: 营业区面积
    - infoDto.isLed: 是否安装LED灯 0否 1是
    - infoDto.isSign: 是否安装招牌 0否  1是
    - infoDto.propertyType: 房产类型 0自有 1租赁
    - infoDto.rentMoney: 租金(元)
    - infoDto.rentTime: 租期(年)
    - infoDto.shopType: 1临街店铺，2写字楼，3商城店铺
    - infoDto.signLength: 招牌长度
    - infoDto.signWidth: 招牌宽度
    - infoDto.totalArea: 总面积
    - movePicDto: 搬迁相关图
    - movePicDto.noSignPic: 不能安装招牌证明图
    - movePicDto.storeMeasurePic: 门面、周边、体验区照片与招牌、体验区测量图
    - storeMoveDto: 搬迁申请信息
    - storeMoveDto.companyCode: 所属分公司编号
    - storeMoveDto.companyName: 所属分公司名称
    - storeMoveDto.currentAddr: 当前地址
    - storeMoveDto.detailedAddr: 详细地址
    - storeMoveDto.leaderCardNo: 负责人卡号
    - storeMoveDto.leaderName: 负责人姓名
    - storeMoveDto.moveReason: 搬迁原因
    - storeMoveDto.newShopAddr: 新店地区
    - storeMoveDto.port: 请求端 0后台 1APP 2PC
    - storeMoveDto.storeCode: 服务中心编号
    - storeMoveDto.storeName: 服务中心名称
    """

    url = "/appStore/webAndApp/store/move/addStoreMoveApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
