import os

from util.client import client

data = {
    "addMemberLeaderAo": {
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
    },  # 负责人信息
    "credentialVO1": {
        "certificateDate": "",
        "credentialType": 0,
        "expiryDate": "",
        "imageBackUrl": "",
        "imageFrontUrl": "",
        "info": "",
        "picUrls": "",
        "remark": "",
        "storeCode": "",
    },  # 营业执照证件
    "credentialVO2": {
        "certificateDate": "",
        "credentialType": 0,
        "expiryDate": "",
        "imageBackUrl": "",
        "imageFrontUrl": "",
        "info": "",
        "picUrls": "",
        "remark": "",
        "storeCode": "",
    },  # 税务登记证
    "credentialVO3": {
        "certificateDate": "",
        "credentialType": 0,
        "expiryDate": "",
        "imageBackUrl": "",
        "imageFrontUrl": "",
        "info": "",
        "picUrls": "",
        "remark": "",
        "storeCode": "",
    },  # 食品经营许可证
    "storeVO": {
        "agentOrder": False,
        "areaCode": "",
        "areaName": "",
        "businessMode": 0,
        "cityCode": "",
        "cityName": "",
        "code": "",
        "companyCode": "",
        "companyName": "",
        "decorationInfo": "",
        "del": 0,
        "deliveryInfo": "",
        "detailAddress": "",
        "disableLogin": False,
        "discountLevel": "",
        "discountPermission": "",
        "disqualified": False,
        "email": "",
        "extraInfo": "",
        "fax": "",
        "hierarchy": "",
        "id": 0,
        "isBadAssetStore": 0,
        "isHighPriority": 0,
        "isInterprovincial": 0,
        "isMainShop": 0,
        "isServiceShop": 0,
        "isSettledAccount": 0,
        "isSignContract": 0,
        "lat": "",
        "leaderId": 0,
        "leaderMobilePhone": "",
        "leaderName": "",
        "leaderNo": "",
        "level": 0,
        "lng": "",
        "name": "",
        "normalStore": False,
        "openDate": "",
        "permission": "",
        "phone": "",
        "postCode": "",
        "provinceCode": "",
        "provinceName": "",
        "ratifyDate": "",
        "remarks": "",
        "selfOrder": False,
        "shopStatus": 0,
        "shopType": 0,
        "shopkeeperId": 0,
        "shopkeeperNo": "",
        "streetCode": "",
        "streetName": "",
        "transferFinishDate": "",
        "ucongNo": "",
        "wechat": "",
        "zipCode": 0,
    },  # 服务中心信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_addStore(data=data, headers=headers):
    """
    添加服务中心
    /mgmt/store/addStore

    参数说明:
    - addMemberLeaderAo: 负责人信息
    - addMemberLeaderAo.cardNo: 会员卡号
    - addMemberLeaderAo.certificatesEndDate: 证件有效期结束时间
    - addMemberLeaderAo.certificatesNo: 证件号码
    - addMemberLeaderAo.certificatesPositiveUrl: 身份证正面图片url
    - addMemberLeaderAo.certificatesReverseUrl: 身份证反面图片url
    - addMemberLeaderAo.certificatesStartDate: 证件有效期开始时间
    - addMemberLeaderAo.certificatesType: 证件类型：1->身份证；2->其他
    - addMemberLeaderAo.createTime: 创建时间
    - addMemberLeaderAo.eatingHabbits: 饮食习惯
    - addMemberLeaderAo.education: 学历，01高中或以下、02中专、03大专、04大学本科、05研究生及以上
    - addMemberLeaderAo.gender: 性别：1->男；2->女
    - addMemberLeaderAo.homePhone: 住宅电话
    - addMemberLeaderAo.leaderAge: 负责人年龄
    - addMemberLeaderAo.leaderBirthday: 负责人生日
    - addMemberLeaderAo.lecturerLevel: 讲师级别
    - addMemberLeaderAo.livePlace: 居住地
    - addMemberLeaderAo.mobile: 负责人手机号码
    - addMemberLeaderAo.nation: 民族
    - addMemberLeaderAo.profession: 职业
    - addMemberLeaderAo.realname: 真实姓名
    - addMemberLeaderAo.resourceCommitteeIdentity: 资委等级
    - addMemberLeaderAo.spouseAge: 配偶年龄
    - addMemberLeaderAo.spouseBirthday: 配偶生日
    - addMemberLeaderAo.spouseCardNo: 配偶卡号
    - addMemberLeaderAo.spouseCertificatesEndDate: 配偶证件有效期结束时间
    - addMemberLeaderAo.spouseCertificatesNo: 配偶证件号码
    - addMemberLeaderAo.spouseCertificatesPositiveUrl: 配偶身份证正面图片地址
    - addMemberLeaderAo.spouseCertificatesReverseUrl: 配偶身份证反面图片地址
    - addMemberLeaderAo.spouseCertificatesStartDate: 配偶证件有效期开始时间
    - addMemberLeaderAo.spouseCertificatesType: 配偶证件类型：1->身份证；2->其他
    - addMemberLeaderAo.spouseEatingHabbits: 配偶饮食习惯
    - addMemberLeaderAo.spouseEducation: 配偶学历
    - addMemberLeaderAo.spouseGender: 配偶性别：1->男；2->女
    - addMemberLeaderAo.spouseLecturerLevel: 配偶讲师级别
    - addMemberLeaderAo.spouseLivePlace: 配偶居住地
    - addMemberLeaderAo.spouseMobile: 配偶手机号码
    - addMemberLeaderAo.spouseNation: 配偶民族
    - addMemberLeaderAo.spouseProfession: 配偶职业
    - addMemberLeaderAo.spouseRealname: 配偶真实姓名
    - addMemberLeaderAo.spouseResourceCommitteeIdentity: 配偶资委等级
    - addMemberLeaderAo.spouseTrainingTimes: 配偶培训次数
    - addMemberLeaderAo.storeCode: 店铺编号
    - addMemberLeaderAo.trainingTimes: 培训次数
    - addMemberLeaderAo.updateTime: 更新时间
    - credentialVO1: 营业执照证件
    - credentialVO1.certificateDate: 办证日期
    - credentialVO1.credentialType: 证件类型 1营业执照 2食品经营许可证 3税务登记证
    - credentialVO1.expiryDate: 到期时间
    - credentialVO1.imageBackUrl: 证件副本照
    - credentialVO1.imageFrontUrl: 证件正本照
    - credentialVO1.info: 证件详细信息
    - credentialVO1.picUrls: 图片--废弃
    - credentialVO1.remark: remark
    - credentialVO1.storeCode: 服务中心编号
    - credentialVO2: 税务登记证
    - credentialVO2.certificateDate: 办证日期
    - credentialVO2.credentialType: 证件类型 1营业执照 2食品经营许可证 3税务登记证
    - credentialVO2.expiryDate: 到期时间
    - credentialVO2.imageBackUrl: 证件副本照
    - credentialVO2.imageFrontUrl: 证件正本照
    - credentialVO2.info: 证件详细信息
    - credentialVO2.picUrls: 图片--废弃
    - credentialVO2.remark: remark
    - credentialVO2.storeCode: 服务中心编号
    - credentialVO3: 食品经营许可证
    - credentialVO3.certificateDate: 办证日期
    - credentialVO3.credentialType: 证件类型 1营业执照 2食品经营许可证 3税务登记证
    - credentialVO3.expiryDate: 到期时间
    - credentialVO3.imageBackUrl: 证件副本照
    - credentialVO3.imageFrontUrl: 证件正本照
    - credentialVO3.info: 证件详细信息
    - credentialVO3.picUrls: 图片--废弃
    - credentialVO3.remark: remark
    - credentialVO3.storeCode: 服务中心编号
    - storeVO: 服务中心信息
    - storeVO.agentOrder: 代客下单 true: 有权限，false: 无权限（85折不适用）
    - storeVO.areaCode: 区/县code
    - storeVO.areaName: 区/县名称
    - storeVO.businessMode: 保证金类型，1/1:3，2/85%
    - storeVO.cityCode: 城市编码
    - storeVO.cityName: 城市名称
    - storeVO.code: 服务中心编号
    - storeVO.companyCode: 所属分公司编号
    - storeVO.companyName: 所属分公司名称
    - storeVO.decorationInfo: 装修信息
    - storeVO.del: 取消资格，0：正常；1：取消资格
    - storeVO.deliveryInfo: 收货地址／收货人／收货电话／收讫章
    - storeVO.detailAddress: 服务中心详细地址(门牌号)
    - storeVO.disableLogin: 禁止登陆 true: 禁止登陆，false: 正常
    - storeVO.discountLevel: 折扣系数等级  A->65%; B->70%; C->75%; D->85%
    - storeVO.discountPermission: 85%权限，1/可押货，2/可押货退货，3/可代客下单（店交付），4/可代客下单（公司交付），5/可转店交付库存，6/禁止登录，7/取消资格，8/可自购（店交付），9/可自购（公司交付），10/电子礼券清单，11/购物礼券清单，12/可代签约，13/可自签约，14/可交付，多个用逗号隔开
    - storeVO.disqualified: 取消资格标志 true: 取消资格，false: 非取消资格
    - storeVO.email: 邮箱
    - storeVO.extraInfo: 额外信息
    - storeVO.fax: 传真
    - storeVO.hierarchy: 服务中心层级
    - storeVO.isBadAssetStore: 是否不良资产门店 0->否 1->是
    - storeVO.isHighPriority: 是否优先处理，1/是，2/否
    - storeVO.isInterprovincial: 是否跨省云+，0/否，1/是
    - storeVO.isMainShop: 是否总店 1总店 2分店
    - storeVO.isServiceShop: 是否服务网店
    - storeVO.isSettledAccount: 是否已结清财务，1/已结清,2/未结清
    - storeVO.isSignContract: 是否签订合同
    - storeVO.lat: 纬度
    - storeVO.leaderId: 总店负责人id
    - storeVO.leaderMobilePhone: 负责人手机号码
    - storeVO.leaderName: 总店负责人姓名
    - storeVO.leaderNo: 总店负责人卡号
    - storeVO.level: 星级
    - storeVO.lng: 经度
    - storeVO.name: 服务中心名称
    - storeVO.normalStore: 是否是正常运营的服务中心，true：是，false：否
    - storeVO.openDate: 开业时间
    - storeVO.permission: 服务中心权限 1:可押货, 2:可交付,3:自购下单,4:可退货,5:代客下单,6:禁止登陆,7:取消资格,8:电子礼券清单,9:购物礼券清单,10:可代签约,11:可自签约  多个逗号隔开
    - storeVO.phone: 店铺联系电话
    - storeVO.postCode: 邮编，废弃
    - storeVO.provinceCode: 省份编码
    - storeVO.provinceName: 省份名称
    - storeVO.ratifyDate: 批准时间
    - storeVO.remarks: 备注
    - storeVO.selfOrder: 自购下单 true: 有权限，false: 无权限（85折不适用）
    - storeVO.shopStatus: 服务中心状态 0正常 1 结业 2 冻结中
    - storeVO.shopType: 网点类型
    - storeVO.shopkeeperId: 分店管理员id（店长id）
    - storeVO.shopkeeperNo: 分店管理员卡号
    - storeVO.streetCode: 街道code
    - storeVO.streetName: 街道名
    - storeVO.transferFinishDate: 完成转让日期
    - storeVO.wechat: 微信号
    - storeVO.zipCode: 邮编，使用中
    """

    url = "/mgmt/store/addStore"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
