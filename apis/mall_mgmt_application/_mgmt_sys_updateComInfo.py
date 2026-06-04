import os

from util.client import client

data = {
    "change": False,  # TODO: 添加参数说明
    "comAccounts": [
        {
            "account": "",
            "accountCode": "",
            "accountName": "",
            "accountUse": 0,
            "bankCity": "",
            "bankCityCode": "",
            "bankName": "",
            "bankProvince": "",
            "bankProvinceCode": "",
            "bankType": "",
            "companyId": 0,
            "id": 0,
            "isDel": 0,
        }
    ],  # 公司账号集合
    "comInvoice": {
        "addressUrl": "",
        "bankName": "",
        "cashier": "",
        "checker": "",
        "companyAccount": "",
        "companyAddress": "",
        "companyBank": "",
        "companyId": 0,
        "companyPhone": "",
        "drawee": "",
        "drawer": "",
        "excludingTaxMaximumAmount": 0.0,
        "id": 0,
        "postAddress": "",
        "postCityCode": "",
        "postCityName": "",
        "postDistrictCode": "",
        "postDistrictName": "",
        "postPostcode": "",
        "postProvinceCode": "",
        "postProvinceName": "",
        "postStreetCode": "",
        "postStreetName": "",
        "taxNo": "",
    },  # 公司账号信息
    "comRegion": {"companyId": 0, "regionCodes": []},  # 公司地区关联信息
    "company": {
        "code": "",
        "contactAddress": "",
        "contactCityCode": "",
        "contactCityName": "",
        "contactDistrictCode": "",
        "contactDistrictName": "",
        "contactPostcode": "",
        "contactProvinceCode": "",
        "contactProvinceName": "",
        "contactProvinceNum": "",
        "contactStreetCode": "",
        "contactStreetName": "",
        "deliveryAddress": "",
        "deliveryCityCode": "",
        "deliveryCityName": "",
        "deliveryDistrictCode": "",
        "deliveryDistrictName": "",
        "deliveryPostcode": "",
        "deliveryProvinceCode": "",
        "deliveryProvinceName": "",
        "deliveryStreetCode": "",
        "deliveryStreetName": "",
        "emailOne": "",
        "emailTwo": "",
        "faxPhone": "",
        "fixedPhoneOne": "",
        "fixedPhoneTwo": "",
        "fullName": "",
        "geographyCode": 0,
        "grade": 0,
        "gradestr": "",
        "id": 0,
        "name": "",
        "openTime": "",
        "principal": "",
        "principalPhone": "",
        "returnAddress": "",
        "returnCityCode": "",
        "returnCityName": "",
        "returnDistrictCode": "",
        "returnDistrictName": "",
        "returnInfo": "",
        "returnMobile": "",
        "returnPeople": "",
        "returnPostcode": "",
        "returnProvinceCode": "",
        "returnProvinceName": "",
        "returnStreetCode": "",
        "returnStreetName": "",
        "shopAddress": "",
        "shopCityCode": "",
        "shopCityName": "",
        "shopDistrictCode": "",
        "shopDistrictName": "",
        "shopPostcode": "",
        "shopProvinceCode": "",
        "shopProvinceName": "",
        "shopStreetCode": "",
        "shopStreetName": "",
        "type": 0,
    },  # 公司信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateComInfo(data=data, headers=headers):
    """
    更改公司信息
    /mgmt/sys/updateComInfo

    参数说明:
    - comAccounts: 公司账号集合
    - comAccounts.account: 账号
    - comAccounts.accountCode: 账号编号
    - comAccounts.accountName: 账号名称
    - comAccounts.accountUse: 账号用途:1->押货款专用;2->商城报单；3->保证金;4->订货款专用;5->备用金
    - comAccounts.bankCity: 银行城市
    - comAccounts.bankCityCode: 银行城市编码
    - comAccounts.bankName: 开户行名称
    - comAccounts.bankProvince: 银行省份
    - comAccounts.bankProvinceCode: 银行省份编码
    - comAccounts.bankType: 开户银行
    - comAccounts.companyId: 公司id
    - comAccounts.id: 主键
    - comAccounts.isDel: 是否删除:0->否；1->是
    - comInvoice: 公司账号信息
    - comInvoice.addressUrl: 发票地址url
    - comInvoice.bankName: 支行名称
    - comInvoice.cashier: 收款员
    - comInvoice.checker: 复核员
    - comInvoice.companyAccount: 账号
    - comInvoice.companyAddress: 公司注册地址
    - comInvoice.companyBank: 公司开户行
    - comInvoice.companyId: 公司id
    - comInvoice.companyPhone: 公司电话
    - comInvoice.drawee: 收票人
    - comInvoice.drawer: 开票员
    - comInvoice.excludingTaxMaximumAmount: 不含税金额上限
    - comInvoice.id: id
    - comInvoice.postAddress: 发票邮寄详细地址
    - comInvoice.postCityCode: 发票邮寄城市编码
    - comInvoice.postCityName: 发票邮寄城市
    - comInvoice.postDistrictCode: 发票邮寄地区编码
    - comInvoice.postDistrictName: 发票邮寄地区
    - comInvoice.postPostcode: 发票邮寄地址邮编
    - comInvoice.postProvinceCode: 发票邮寄省份编码
    - comInvoice.postProvinceName: 发票邮寄省份
    - comInvoice.postStreetCode: 发票邮寄街道编码
    - comInvoice.postStreetName: 发票邮寄街道
    - comInvoice.taxNo: 公司税号
    - comRegion: 公司地区关联信息
    - comRegion.companyId: 公司id
    - comRegion.regionCodes: 区域编码集
    - company: 公司信息
    - company.code: 公司编号
    - company.contactAddress: 联系详细地址
    - company.contactCityCode: 联系地址所属城市编码
    - company.contactCityName: 联系地址所属城市
    - company.contactDistrictCode: 联系地址所属区县编码
    - company.contactDistrictName: 联系地址所属区县
    - company.contactPostcode: 联系地址邮编
    - company.contactProvinceCode: 联系地址所属省份编码
    - company.contactProvinceName: 联系地址所属省份
    - company.contactProvinceNum: 联系地址所属省份编号
    - company.contactStreetCode: 联系地址所属街道编码
    - company.contactStreetName: 联系地址所属街道
    - company.deliveryAddress: 发货详细地址
    - company.deliveryCityCode: 发货地址所属城市编码
    - company.deliveryCityName: 发货地址所属城市
    - company.deliveryDistrictCode: 发货地址所属区县编码
    - company.deliveryDistrictName: 发货地址所属区县
    - company.deliveryPostcode: 发货地址邮编
    - company.deliveryProvinceCode: 发货地址所属省份编码
    - company.deliveryProvinceName: 发货地址所属省份
    - company.deliveryStreetCode: 发货地址所属街道编码
    - company.deliveryStreetName: 发货地址所属街道
    - company.emailOne: 电子邮箱1
    - company.emailTwo: 电子邮箱2
    - company.faxPhone: 传真
    - company.fixedPhoneOne: 固定电话1
    - company.fixedPhoneTwo: 固定电话2
    - company.fullName: 全称
    - company.geographyCode: 所属地区：1.华北 2.东北 3.华东 4.东中 5.东南 6.西南 7.西北
    - company.grade: 公司等级：公司类型为;分公司时：下拉选项有：1级，2级，3级
    - company.gradestr: 公司等级：公司类型为;分公司时：下拉选项有：A级，B级，C级,D级
    - company.id: 公司id
    - company.name: 公司名称
    - company.openTime: 开设时间
    - company.principal: 负责人
    - company.principalPhone: 负责人电话
    - company.returnAddress: 退货详细地址
    - company.returnCityCode: 退货地址所在市编码
    - company.returnCityName: 退货地址所在市
    - company.returnDistrictCode: 退货地址所在区县编码
    - company.returnDistrictName: 退货地址所在区县
    - company.returnInfo: 退回信息
    - company.returnMobile: 退货电话
    - company.returnPeople: 退货人
    - company.returnPostcode: 退货地址邮编
    - company.returnProvinceCode: 退货地址所在省编码
    - company.returnProvinceName: 退货地址所在省
    - company.returnStreetCode: 退货地址所在街道编码
    - company.returnStreetName: 退货地址所在街道
    - company.shopAddress: 店铺详细地址
    - company.shopCityCode: 店铺所在城市编码
    - company.shopCityName: 店铺所在城市
    - company.shopDistrictCode: 店铺所在区县编码
    - company.shopDistrictName: 店铺所在区县
    - company.shopPostcode: 店铺所在地邮编
    - company.shopProvinceCode: 店铺所在省份编码
    - company.shopProvinceName: 店铺所在省份
    - company.shopStreetCode: 店铺所在街道编码
    - company.shopStreetName: 店铺所在街道
    - company.type: 类型 公司类型1->总公司；2->分公司；3->上海商业；4->扬州公司；5->吉林公司;6->广东公司
    """

    url = "/mgmt/sys/updateComInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
