import os

from util.client import client

data = {
    "credentialList": [
        {
            "certificateDate": "",
            "credentialType": 0,
            "expiryDate": "",
            "imageBackUrl": "",
            "imageFrontUrl": "",
            "info": "",
            "picUrls": "",
            "remark": "",
            "storeCode": "",
        }
    ],  # 证件资料变更信息
    "editLeaderAo": {
        "cardNo": "",
        "certificatesEndDate": "",
        "certificatesNo": "",
        "certificatesPositiveUrl": "",
        "certificatesReverseUrl": "",
        "certificatesStartDate": "",
        "certificatesType": 0,
        "createTime": "",
        "eatingHabbits": "",
        "education": "",
        "gender": 0,
        "homePhone": "",
        "id": 0,
        "leaderAge": 0,
        "leaderBirthday": "",
        "lecturerLevel": "",
        "livePlace": "",
        "mobile": "",
        "nation": "",
        "profession": "",
        "realname": "",
        "resourceCommitteeIdentity": "",
        "spouseAge": 0,
        "spouseBirthday": "",
        "spouseCardNo": "",
        "spouseCertificatesEndDate": "",
        "spouseCertificatesNo": "",
        "spouseCertificatesPositiveUrl": "",
        "spouseCertificatesReverseUrl": "",
        "spouseCertificatesStartDate": "",
        "spouseCertificatesType": 0,
        "spouseEatingHabbits": "",
        "spouseEducation": "",
        "spouseGender": 0,
        "spouseLecturerLevel": "",
        "spouseLivePlace": "",
        "spouseMobile": "",
        "spouseNation": "",
        "spouseProfession": "",
        "spouseRealname": "",
        "spouseResourceCommitteeIdentity": "",
        "spouseTrainingTimes": 0,
        "storeCode": "",
        "trainingTimes": 0,
        "updateTime": "",
    },  # 负责人资料信息
    "editTypes": [],  # 变更类型  1.负责人资料 2.服务中心资料  3.证件资料   4.店铺装修
    "storeCode": "",  # 服务中心code
    "storeDataDto": {
        "areaCode": "",
        "areaName": "",
        "cityCode": "",
        "cityName": "",
        "code": "",
        "companyCode": "",
        "deliveryInfo": "",
        "discountPermission": "",
        "email": "",
        "extraInfo": "",
        "fax": "",
        "isBadAssetStore": 0,
        "isHighPriority": 0,
        "isInterprovincial": 0,
        "isMainShop": 0,
        "isServiceShop": 0,
        "isSignContract": 0,
        "lat": "",
        "leaderId": 0,
        "leaderNo": "",
        "level": 0,
        "lng": "",
        "name": "",
        "openDate": "",
        "permission": "",
        "phone": "",
        "provinceCode": "",
        "provinceName": "",
        "ratifyDate": "",
        "remarks": "",
        "shopStatus": 0,
        "shopType": 0,
        "shopkeeperId": 0,
        "shopkeeperNo": "",
        "streetCode": "",
        "streetName": "",
        "transferFinishDate": "",
        "ucongNo": "",
        "wechat": "",
        "zipCode": "",
    },  # 服务中心资料信息
    "storeDecorationDto": {
        "businessArea": "",
        "businessFloorHeight": "",
        "createTime": "",
        "del": 0,
        "id": 0,
        "isLed": 0,
        "isSign": 0,
        "leaseTerm": "",
        "monthlyRent": "",
        "propertyType": 0,
        "shopLength": "",
        "shopType": 0,
        "shopWidth": "",
        "signLength": "",
        "signWidth": "",
        "storeCode": "",
        "storePic": "",
        "totalArea": "",
        "updateTime": "",
    },  # 装修信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_editStore(data=data, headers=headers):
    """
    更新服务中心资料信息
    /mgmt/store/editStore

    参数说明:
    - credentialList: 证件资料变更信息
    - credentialList.certificateDate: 办证日期
    - credentialList.credentialType: 证件类型 1营业执照 2食品经营许可证 3税务登记证
    - credentialList.expiryDate: 到期时间
    - credentialList.imageBackUrl: 证件副本照
    - credentialList.imageFrontUrl: 证件正本照
    - credentialList.info: 证件详细信息
    - credentialList.picUrls: 图片--废弃
    - credentialList.remark: remark
    - credentialList.storeCode: 服务中心编号
    - editLeaderAo: 负责人资料信息
    - editLeaderAo.cardNo: 会员卡号
    - editLeaderAo.certificatesEndDate: 证件有效期结束时间
    - editLeaderAo.certificatesNo: 证件号码
    - editLeaderAo.certificatesPositiveUrl: 身份证正面图片url
    - editLeaderAo.certificatesReverseUrl: 身份证反面图片url
    - editLeaderAo.certificatesStartDate: 证件有效期开始时间
    - editLeaderAo.certificatesType: 证件类型：1->身份证；2->其他
    - editLeaderAo.createTime: 创建时间
    - editLeaderAo.eatingHabbits: 饮食习惯
    - editLeaderAo.education: 学历
    - editLeaderAo.gender: 性别：1->男；2->女
    - editLeaderAo.homePhone: 住宅电话
    - editLeaderAo.id: id
    - editLeaderAo.leaderAge: 负责人年龄
    - editLeaderAo.leaderBirthday: 负责人生日
    - editLeaderAo.lecturerLevel: 讲师级别
    - editLeaderAo.livePlace: 居住地
    - editLeaderAo.mobile: 负责人手机号码
    - editLeaderAo.nation: 民族
    - editLeaderAo.profession: 职业
    - editLeaderAo.realname: 真实姓名
    - editLeaderAo.resourceCommitteeIdentity: 资委等级
    - editLeaderAo.spouseAge: 配偶年龄
    - editLeaderAo.spouseBirthday: 配偶生日
    - editLeaderAo.spouseCardNo: 配偶卡号
    - editLeaderAo.spouseCertificatesEndDate: 配偶证件有效期结束时间
    - editLeaderAo.spouseCertificatesNo: 配偶证件号码
    - editLeaderAo.spouseCertificatesPositiveUrl: 配偶身份证正面地址
    - editLeaderAo.spouseCertificatesReverseUrl: 配偶身份证反面地址
    - editLeaderAo.spouseCertificatesStartDate: 配偶证件有效期开始时间
    - editLeaderAo.spouseCertificatesType: 配偶证件类型：1->身份证；2->其他
    - editLeaderAo.spouseEatingHabbits: 配偶饮食习惯
    - editLeaderAo.spouseEducation: 配偶学历
    - editLeaderAo.spouseGender: 配偶性别：1->男；2->女
    - editLeaderAo.spouseLecturerLevel: 配偶讲师级别
    - editLeaderAo.spouseLivePlace: 配偶居住地
    - editLeaderAo.spouseMobile: 配偶手机号码
    - editLeaderAo.spouseNation: 配偶民族
    - editLeaderAo.spouseProfession: 配偶职业
    - editLeaderAo.spouseRealname: 配偶真实姓名
    - editLeaderAo.spouseResourceCommitteeIdentity: 配偶资委等级
    - editLeaderAo.spouseTrainingTimes: 配偶培训次数
    - editLeaderAo.storeCode: 店铺编号
    - editLeaderAo.trainingTimes: 培训次数
    - editLeaderAo.updateTime: 更新时间
    - editTypes: 变更类型  1.负责人资料 2.服务中心资料  3.证件资料   4.店铺装修
    - storeCode: 服务中心code
    - storeDataDto: 服务中心资料信息
    - storeDataDto.areaCode: 区/县code
    - storeDataDto.areaName: 区/县名称
    - storeDataDto.cityCode: 城市编码
    - storeDataDto.cityName: 城市名称
    - storeDataDto.code: 服务中心编号
    - storeDataDto.companyCode: 所属分公司编号
    - storeDataDto.deliveryInfo: 收货地址／收货人／收货电话／收讫章
    - storeDataDto.discountPermission: 85%权限，1/可押货，2/可押货退货，3/可代客下单（店交付），4/可代客下单（公司交付），5/可转店交付库存，6/禁止登录，7/取消资格，8/可自购（店交付），9/可自购（公司交付），10/电子礼券清单，11/购物礼券清单，12/可代签约，13/可自签约，14/可交付，多个用逗号隔开
    - storeDataDto.email: 邮箱
    - storeDataDto.extraInfo: 额外信息
    - storeDataDto.fax: 传真
    - storeDataDto.isBadAssetStore: 是否不良资产门店 0->否 1->是
    - storeDataDto.isHighPriority: 是否优先处理，1/是，2/否
    - storeDataDto.isInterprovincial: 是否跨省云+，0/否，1/是
    - storeDataDto.isMainShop: 是否总店 1总店 2分店
    - storeDataDto.isServiceShop: 是否服务网店
    - storeDataDto.isSignContract: 是否签订合同
    - storeDataDto.lat: 纬度
    - storeDataDto.leaderId: 总店负责人id
    - storeDataDto.leaderNo: 总店负责人卡号
    - storeDataDto.level: 星级
    - storeDataDto.lng: 经度
    - storeDataDto.name: 服务中心名称
    - storeDataDto.openDate: 开业时间
    - storeDataDto.permission: 权限
    - storeDataDto.phone: 店铺联系电话
    - storeDataDto.provinceCode: 省份编码
    - storeDataDto.provinceName: 省份名称
    - storeDataDto.ratifyDate: 批准时间
    - storeDataDto.remarks: 备注
    - storeDataDto.shopStatus: 服务中心状态 0正常 1 结业
    - storeDataDto.shopType: 网点类型
    - storeDataDto.shopkeeperId: 分店管理员id（店长id）
    - storeDataDto.shopkeeperNo: 分店管理员卡号
    - storeDataDto.streetCode: 街道code
    - storeDataDto.streetName: 街道名
    - storeDataDto.transferFinishDate: 完成转让日期
    - storeDataDto.wechat: 微信号
    - storeDataDto.zipCode: 邮编
    - storeDecorationDto: 装修信息
    - storeDecorationDto.businessArea: 营业区面积
    - storeDecorationDto.businessFloorHeight: 营业区层高
    - storeDecorationDto.del: 删除标识，0：未删除；1：已删除
    - storeDecorationDto.isLed: 是否安装LED灯 0否 1是
    - storeDecorationDto.isSign: 是否安装招牌 0 否 1 是
    - storeDecorationDto.leaseTerm: 租赁年限
    - storeDecorationDto.monthlyRent: 月租金
    - storeDecorationDto.propertyType: 房产类型  0 自有 1 租赁
    - storeDecorationDto.shopLength: 店铺长度
    - storeDecorationDto.shopType: 店铺类型，1/临街店铺, 2/写字楼, 3/商场店铺
    - storeDecorationDto.shopWidth: 店铺宽度
    - storeDecorationDto.signLength: 招牌长度
    - storeDecorationDto.signWidth: 招牌宽度
    - storeDecorationDto.storeCode: 服务中心编号
    - storeDecorationDto.storePic: 店铺装修图
    - storeDecorationDto.totalArea: 总面积
    """

    url = "/mgmt/store/editStore"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
