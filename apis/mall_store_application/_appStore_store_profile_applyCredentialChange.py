import os

from util.client import client

data = {
    "businessInfo": {
        "certificateDate": "",
        "expiryDate": "",
        "imageBackUrl": "",
        "imageFrontUrl": "",
        "info": {
            "businessAreaCode": "",
            "businessAreaName": "",
            "businessCityCode": "",
            "businessCityName": "",
            "businessPlace": "",
            "businessProvinceCode": "",
            "businessProvinceName": "",
            "businessScope": "",
            "businessStreetCode": "",
            "businessStreetName": "",
            "certificateCode": "",
            "certificateName": "",
            "certificatePerson": "",
            "certificationAuthority": "",
            "composition": "",
            "identificationCode": "",
            "isFive": "",
            "isSale": "",
            "operatorName": "",
            "operatorType": "",
            "socialCreditCode": "",
        },
        "isHaveEffectTime": 0,
        "remark": "",
    },  # 营业执照信息
    "foodInfo": {
        "certificateDate": "",
        "expiryDate": "",
        "imageBackUrl": "",
        "imageFrontUrl": "",
        "info": {"businessScope": "", "certificationAuthority": "", "isFoodBusinessLicense": "", "licenseKey": ""},
        "isHaveEffectTime": 0,
        "remark": "",
    },  # 食品经营许可证信息
    "taxInfo": {
        "certificateDate": "",
        "expiryDate": "",
        "imageBackUrl": "",
        "imageFrontUrl": "",
        "info": {"businessScope": "", "certificationAuthority": "", "code": ""},
        "isHaveEffectTime": 0,
        "remark": "",
    },  # 税务登记证信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyCredentialChange(data=data, headers=headers):
    """
    申请服务中心证件信息变更
    /appStore/store/profile/applyCredentialChange

    参数说明:
    - businessInfo: 营业执照信息
    - businessInfo.certificateDate: 办证日期
    - businessInfo.expiryDate: 到期时间，格式：yyyy-MM-dd,yyyy-MM-dd
    - businessInfo.imageBackUrl: 证件副本照
    - businessInfo.imageFrontUrl: 证件正本照
    - businessInfo.info: 证件详细信息
    - businessInfo.info.businessAreaCode: 经营场所区/县code
    - businessInfo.info.businessAreaName: 经营场所区/县名称
    - businessInfo.info.businessCityCode: 经营场所城市编码
    - businessInfo.info.businessCityName: 经营场所城市名称
    - businessInfo.info.businessPlace: 经营场所，（详细地址）
    - businessInfo.info.businessProvinceCode: 经营场所省份编码
    - businessInfo.info.businessProvinceName: 经营场所省份名称
    - businessInfo.info.businessScope: 经营范围
    - businessInfo.info.businessStreetCode: 经营场所街道code
    - businessInfo.info.businessStreetName: 经营场所街道名称
    - businessInfo.info.certificateCode: 营业执照号码
    - businessInfo.info.certificateName: 营业执照名称
    - businessInfo.info.certificatePerson: 营业执照人
    - businessInfo.info.certificationAuthority: 办证机关
    - businessInfo.info.composition: 组成形式, 1、个人经营 2、家庭经营
    - businessInfo.info.identificationCode: 纳税人识别号
    - businessInfo.info.isFive: 五证合一， 1：是，0：否
    - businessInfo.info.isSale: 是否包含销售， 1：是，0：否
    - businessInfo.info.operatorName: 经营者
    - businessInfo.info.operatorType: 经营类型，文本类型
    - businessInfo.info.socialCreditCode: 社会信用代码
    - businessInfo.isHaveEffectTime: 否有有限期(0->无有效期,1->有有效期)
    - businessInfo.remark: 备注
    - foodInfo: 食品经营许可证信息
    - foodInfo.certificateDate: 办证日期
    - foodInfo.expiryDate: 到期时间，格式：yyyy-MM-dd,yyyy-MM-dd
    - foodInfo.imageBackUrl: 证件副本照
    - foodInfo.imageFrontUrl: 证件正本照
    - foodInfo.info: 证件详细信息
    - foodInfo.info.businessScope: 经营范围
    - foodInfo.info.certificationAuthority: 办证机关
    - foodInfo.info.isFoodBusinessLicense: 食品经营许可证, 1是，0否
    - foodInfo.info.licenseKey: 许可证号
    - foodInfo.isHaveEffectTime: 否有有限期(0->无有效期,1->有有效期)
    - foodInfo.remark: 备注
    - taxInfo: 税务登记证信息
    - taxInfo.certificateDate: 办证日期
    - taxInfo.expiryDate: 到期时间，格式：yyyy-MM-dd,yyyy-MM-dd
    - taxInfo.imageBackUrl: 证件副本照
    - taxInfo.imageFrontUrl: 证件正本照
    - taxInfo.info: 证件详细信息
    - taxInfo.info.businessScope: 经营范围
    - taxInfo.info.certificationAuthority: 办证机关
    - taxInfo.info.code: 税务登记证税字号
    - taxInfo.isHaveEffectTime: 否有有限期(0->无有效期,1->有有效期)
    - taxInfo.remark: 备注
    """

    url = "/appStore/store/profile/applyCredentialChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
