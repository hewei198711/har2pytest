import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_sys_store_certificate_upload_apply_pending(headers=headers):
    """
    上传待导入证件的服务中心集合
    /mgmt/sys/store/certificate/upload/apply/pending
    """

    url = "/mgmt/sys/store/certificate/upload/apply/pending"
    with client.post(url=url, headers=headers) as r:
        return r
