import os

from util.client import client

params = {
    "companyCode": "",  # 所属分公司编号
    "leaderCardNo": "",  # 总店负责人卡号
    "level": 0,  # 星级
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "provinceCode": "",  # 省份编码
    "provinceName": "",  # 省份名称
    "shopType": 0,  # 1、微店 2、微店(账务未清)3、微店(办理结店中)4、微店(结店)5、冻结资格6、办理结点中7、取消（账务未结清）8、新批未运作9、正式网点10、结店（保店二年1、结店12、结店（保店一年13、结店（保店三年）
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_listStoreLevel(params=params, headers=headers):
    """
    获取服务中心等级列表
    /mgmt/store/listStoreLevel

    参数说明:
    - companyCode: 所属分公司编号
    - leaderCardNo: 总店负责人卡号
    - level: 星级
    - pageNum: pageNum
    - pageSize: pageSize
    - provinceCode: 省份编码
    - provinceName: 省份名称
    - shopType: 1、微店 2、微店(账务未清)3、微店(办理结店中)4、微店(结店)5、冻结资格6、办理结点中7、取消（账务未结清）8、新批未运作9、正式网点10、结店（保店二年1、结店12、结店（保店一年13、结店（保店三年）
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/listStoreLevel"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
