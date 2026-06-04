import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "certificatesEndDate": "",  # 证件有效期结束时间
    "certificatesNo": "",  # 证件号码
    "certificatesPositiveUrl": "",  # 身份证正面图片url
    "certificatesReverseUrl": "",  # 身份证反面图片url
    "certificatesStartDate": "",  # 证件有效期开始时间
    "certificatesType": 0,  # 证件类型：1->身份证；2->其他
    "createTime": "",  # 创建时间
    "eatingHabbits": "",  # 饮食习惯
    "education": "",  # 学历
    "gender": 0,  # 性别：1->男；2->女
    "homePhone": "",  # 住宅电话
    "id": 0,  # id
    "lecturerLevel": "",  # 讲师级别
    "livePlace": "",  # 居住地
    "mobile": "",  # 负责人手机号码
    "nation": "",  # 民族
    "profession": "",  # 职业
    "realname": "",  # 真实姓名
    "resourceCommitteeIdentity": "",  # 资委等级
    "spouseCardNo": "",  # 配偶卡号
    "spouseCertificatesEndDate": "",  # 配偶证件有效期结束时间
    "spouseCertificatesNo": "",  # 配偶证件号码
    "spouseCertificatesPositiveUrl": "",  # 配偶身份证正面地址
    "spouseCertificatesReverseUrl": "",  # 配偶身份证反面地址
    "spouseCertificatesStartDate": "",  # 配偶证件有效期开始时间
    "spouseCertificatesType": 0,  # 配偶证件类型：1->身份证；2->其他
    "spouseEatingHabbits": "",  # 配偶饮食习惯
    "spouseEducation": "",  # 配偶学历
    "spouseGender": 0,  # 配偶性别：1->男；2->女
    "spouseLecturerLevel": "",  # 配偶讲师级别
    "spouseLivePlace": "",  # 配偶居住地
    "spouseMobile": "",  # 配偶手机号码
    "spouseNation": "",  # 配偶民族
    "spouseProfession": "",  # 配偶职业
    "spouseRealname": "",  # 配偶真实姓名
    "spouseResourceCommitteeIdentity": "",  # 配偶资委等级
    "spouseTrainingTimes": 0,  # 配偶培训次数
    "storeCode": "",  # 店铺编号
    "trainingTimes": 0,  # 培训次数
    "updateTime": "",  # 更新时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_leader_leaderTransfer(data=data, headers=headers):
    """
    负责人转移
    /mgmt/store/leader/leaderTransfer

    参数说明:
    - cardNo: 会员卡号
    - certificatesEndDate: 证件有效期结束时间
    - certificatesNo: 证件号码
    - certificatesPositiveUrl: 身份证正面图片url
    - certificatesReverseUrl: 身份证反面图片url
    - certificatesStartDate: 证件有效期开始时间
    - certificatesType: 证件类型：1->身份证；2->其他
    - createTime: 创建时间
    - eatingHabbits: 饮食习惯
    - education: 学历
    - gender: 性别：1->男；2->女
    - homePhone: 住宅电话
    - id: id
    - lecturerLevel: 讲师级别
    - livePlace: 居住地
    - mobile: 负责人手机号码
    - nation: 民族
    - profession: 职业
    - realname: 真实姓名
    - resourceCommitteeIdentity: 资委等级
    - spouseCardNo: 配偶卡号
    - spouseCertificatesEndDate: 配偶证件有效期结束时间
    - spouseCertificatesNo: 配偶证件号码
    - spouseCertificatesPositiveUrl: 配偶身份证正面地址
    - spouseCertificatesReverseUrl: 配偶身份证反面地址
    - spouseCertificatesStartDate: 配偶证件有效期开始时间
    - spouseCertificatesType: 配偶证件类型：1->身份证；2->其他
    - spouseEatingHabbits: 配偶饮食习惯
    - spouseEducation: 配偶学历
    - spouseGender: 配偶性别：1->男；2->女
    - spouseLecturerLevel: 配偶讲师级别
    - spouseLivePlace: 配偶居住地
    - spouseMobile: 配偶手机号码
    - spouseNation: 配偶民族
    - spouseProfession: 配偶职业
    - spouseRealname: 配偶真实姓名
    - spouseResourceCommitteeIdentity: 配偶资委等级
    - spouseTrainingTimes: 配偶培训次数
    - storeCode: 店铺编号
    - trainingTimes: 培训次数
    - updateTime: 更新时间
    """

    url = "/mgmt/store/leader/leaderTransfer"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
