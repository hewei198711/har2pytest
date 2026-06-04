import os

from util.client import client

data = {
    "addressInfo": "",  # 详细地址／联系地址
    "companyCode": "",  # 所属分公司编号
    "decorationInfo": "",  # 装修信息
    "deliveryInfo": "",  # 收货地址／收货人／收货电话／收讫章
    "email": "",  # 邮箱
    "extraInfo": "",  # 额外信息
    "fax": "",  # 传真
    "id": 0,  # TODO: 添加参数说明
    "isMainShop": 0,  # 是否总店 1总店 2分店
    "isServiceShop": 0,  # 是否服务网店
    "isSignContract": 0,  # 是否签订合同
    "leaderId": 0,  # 总店负责人id
    "level": 0,  # 星级
    "name": "",  # 服务中心名称
    "openDate": "",  # 开业时间
    "permission": "",  # 权限
    "phone": "",  # 店铺联系电话
    "province": "",  # 省份
    "ratifyDate": "",  # 批准时间
    "remarks": "",  # 备注
    "shopStatus": 0,  # 服务中心状态
    "shopType": 0,  # 网点类型
    "shopkeeperId": 0,  # 分店管理员id（店长id）
    "zipCode": "",  # 邮编
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_updateStore(data=data, headers=headers):
    """
    更新服务中心
    /mgmt/store/updateStore

    参数说明:
    - addressInfo: 详细地址／联系地址
    - companyCode: 所属分公司编号
    - decorationInfo: 装修信息
    - deliveryInfo: 收货地址／收货人／收货电话／收讫章
    - email: 邮箱
    - extraInfo: 额外信息
    - fax: 传真
    - isMainShop: 是否总店 1总店 2分店
    - isServiceShop: 是否服务网店
    - isSignContract: 是否签订合同
    - leaderId: 总店负责人id
    - level: 星级
    - name: 服务中心名称
    - openDate: 开业时间
    - permission: 权限
    - phone: 店铺联系电话
    - province: 省份
    - ratifyDate: 批准时间
    - remarks: 备注
    - shopStatus: 服务中心状态
    - shopType: 网点类型
    - shopkeeperId: 分店管理员id（店长id）
    - zipCode: 邮编
    """

    url = "/mgmt/store/updateStore"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
