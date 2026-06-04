import os

from util.client import client

params = {
    "address": "",  # 地址关键字，模糊查询
    "areaCode": "",  # 区/县Code
    "businessMode": 0,  # 保证金类型，1/1:3，2/85%
    "cityCode": "",  # 城市Code
    "companyCode": "",  # 所属分公司编号 全部则不传
    "hierarchy": "",  # 服务中心层级
    "isBadAssetStore": 0,  # 是否不良资产门店, 0->否 1->是';
    "isHighPriority": 0,  # 是否优先处理，1/是，2/否
    "isMainShop": 0,  # 是否总店 1总店 2分店 全部则不传
    "isServiceShop": 0,  # 是否服务网店
    "isSettledAccount": 0,  # 是否已结清财务，1/已结清,2/未结清
    "isSignContract": 0,  # 是否签订合同
    "leaderCardNo": "",  # 总店负责人卡号
    "leaderName": "",  # 负责人姓名
    "level": 0,  # 星级 1普通服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店 全部则不传
    "name": "",  # 服务中心名称
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "provinceCode": "",  # 省份Code
    "ratifyEndTime": "",  # 批准最晚时间点
    "ratifyStartTime": "",  # 批准最早时间点
    "searchKey": "",  # 服务中心编码或服务中心名称
    "shopType": 0,  # 全部则不传  网点类型
    "shopkeeperName": "",  # 分店管理员名称
    "shopkeeperNo": "",  # 分店管理员卡号
    "storeCode": "",  # 服务中心编号
    "storeCodes": [],  # 服务中心编号集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_listStore(params=params, headers=headers):
    """
    获取服务中心列表
    /mgmt/store/listStore

    参数说明:
    - address: 地址关键字，模糊查询
    - areaCode: 区/县Code
    - businessMode: 保证金类型，1/1:3，2/85%
    - cityCode: 城市Code
    - companyCode: 所属分公司编号 全部则不传
    - hierarchy: 服务中心层级
    - isBadAssetStore: 是否不良资产门店, 0->否 1->是';
    - isHighPriority: 是否优先处理，1/是，2/否
    - isMainShop: 是否总店 1总店 2分店 全部则不传
    - isServiceShop: 是否服务网店
    - isSettledAccount: 是否已结清财务，1/已结清,2/未结清
    - isSignContract: 是否签订合同
    - leaderCardNo: 总店负责人卡号
    - leaderName: 负责人姓名
    - level: 星级 1普通服务中心 2五星服务中心 3五星旗舰服务中心 4无实体店 全部则不传
    - name: 服务中心名称
    - pageNum: pageNum
    - pageSize: pageSize
    - provinceCode: 省份Code
    - ratifyEndTime: 批准最晚时间点
    - ratifyStartTime: 批准最早时间点
    - searchKey: 服务中心编码或服务中心名称
    - shopType: 全部则不传  网点类型
    - shopkeeperName: 分店管理员名称
    - shopkeeperNo: 分店管理员卡号
    - storeCode: 服务中心编号
    - storeCodes: 服务中心编号集合
    """

    url = "/mgmt/store/listStore"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
