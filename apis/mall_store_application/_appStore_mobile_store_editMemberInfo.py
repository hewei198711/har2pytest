import os

from util.client import client

data = {
    "address": "",  # 详细地址
    "birthday": "",  # 生日
    "certificatesEndDate": "",  # 证件有效期结束时间
    "certificatesPositiveUrl": "",  # 身份证正面地址
    "certificatesReverseUrl": "",  # 身份证反面地址
    "certificatesStartDate": "",  # 证件有效期开始时间
    "city": "",  # 地址市
    "consumeFollow": "",  # 消费关注
    "district": "",  # 地址区
    "education": "",  # 学历
    "email": "",  # 电子邮箱
    "emerContactEmail": "",  # 紧急联系人邮箱
    "emerContactHomePhone": "",  # 紧急联系人家庭电话
    "emerContactMobile": "",  # 紧急联系人手机号
    "emerContactName": "",  # 紧急联系人姓名
    "gender": 0,  # 性别：1->男；2->女
    "handledCardNo": "",  # 新经办人卡号
    "homePhone": "",  # 住宅电话
    "id": 0,  # id
    "livePlace": "",  # 居住地
    "marital": 0,  # 婚姻状况：1->未婚；2->已婚；3->离异
    "nation": "",  # 民族
    "opencardPositiveUrl": "",  # 开卡资料正面地址
    "opencardReverseUrl": "",  # 开卡资料反面地址
    "postcode": "",  # 邮政编码
    "profession": "",  # 职业
    "province": "",  # 地址省份
    "spouseAddress": "",  # 配偶详细地址
    "spouseBirthday": "",  # 配偶生日
    "spouseCardEmail": "",  # 配偶预留电子邮箱
    "spouseCertificatesEndDate": "",  # 配偶证件有效期结束时间
    "spouseCertificatesPositiveUrl": "",  # 配偶身份证正面地址
    "spouseCertificatesReverseUrl": "",  # 配偶身份证反面地址
    "spouseCertificatesStartDate": "",  # 配偶证件有效期开始时间
    "spouseCity": "",  # 配偶地址市
    "spouseConsumeFollow": "",  # 配偶消费关注
    "spouseDistrict": "",  # 配偶地址区
    "spouseEducation": "",  # 配偶学历
    "spouseGender": 0,  # 配偶性别：1->男；2->女
    "spouseHomePhone": "",  # 配偶住宅电话
    "spouseLivePlace": "",  # 配偶居住地
    "spouseMarital": 0,  # 配偶婚姻状况：1->未婚；2->已婚；3->离异
    "spouseNation": "",  # 配偶民族
    "spouseOrNot": 0,  # 是否有配偶，1 是 ，0 否
    "spousePostcode": "",  # 配偶邮政编码
    "spouseProfession": "",  # 配偶职业
    "spouseProvince": "",  # 配偶地址省份
    "type": 0,  # 变更类型：1->修改线下办卡资料；2->修改会员资料；3->修改经办人
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_store_editMemberInfo(data=data, headers=headers):
    """
    app服务中心业务大厅修改会员资料
    /appStore/mobile/store/editMemberInfo

    参数说明:
    - address: 详细地址
    - birthday: 生日
    - certificatesEndDate: 证件有效期结束时间
    - certificatesPositiveUrl: 身份证正面地址
    - certificatesReverseUrl: 身份证反面地址
    - certificatesStartDate: 证件有效期开始时间
    - city: 地址市
    - consumeFollow: 消费关注
    - district: 地址区
    - education: 学历
    - email: 电子邮箱
    - emerContactEmail: 紧急联系人邮箱
    - emerContactHomePhone: 紧急联系人家庭电话
    - emerContactMobile: 紧急联系人手机号
    - emerContactName: 紧急联系人姓名
    - gender: 性别：1->男；2->女
    - handledCardNo: 新经办人卡号
    - homePhone: 住宅电话
    - id: id
    - livePlace: 居住地
    - marital: 婚姻状况：1->未婚；2->已婚；3->离异
    - nation: 民族
    - opencardPositiveUrl: 开卡资料正面地址
    - opencardReverseUrl: 开卡资料反面地址
    - postcode: 邮政编码
    - profession: 职业
    - province: 地址省份
    - spouseAddress: 配偶详细地址
    - spouseBirthday: 配偶生日
    - spouseCardEmail: 配偶预留电子邮箱
    - spouseCertificatesEndDate: 配偶证件有效期结束时间
    - spouseCertificatesPositiveUrl: 配偶身份证正面地址
    - spouseCertificatesReverseUrl: 配偶身份证反面地址
    - spouseCertificatesStartDate: 配偶证件有效期开始时间
    - spouseCity: 配偶地址市
    - spouseConsumeFollow: 配偶消费关注
    - spouseDistrict: 配偶地址区
    - spouseEducation: 配偶学历
    - spouseGender: 配偶性别：1->男；2->女
    - spouseHomePhone: 配偶住宅电话
    - spouseLivePlace: 配偶居住地
    - spouseMarital: 配偶婚姻状况：1->未婚；2->已婚；3->离异
    - spouseNation: 配偶民族
    - spouseOrNot: 是否有配偶，1 是 ，0 否
    - spousePostcode: 配偶邮政编码
    - spouseProfession: 配偶职业
    - spouseProvince: 配偶地址省份
    - type: 变更类型：1->修改线下办卡资料；2->修改会员资料；3->修改经办人
    """

    url = "/appStore/mobile/store/editMemberInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
