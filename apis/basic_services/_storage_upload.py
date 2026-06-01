import os

from requests_toolbelt import MultipartEncoder

from util.client import client

files = {
    "storageType": "PublicCloud",  # TODO: 添加参数说明
    "clientKey": "mall-center-product",  # TODO: 添加参数说明
    "file": "(binary)",  # TODO: 添加参数说明
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundarySpxP9y98G84LF6p7",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _storage_upload(files=files, headers=headers):
    """
    TODO: 添加接口描述
    /storage/upload
    """

    url = "/storage/upload"
    with open(files["file"], "rb") as f:
        filename = os.path.basename(files["file"])
        m = MultipartEncoder(
            fields={
                "storageType": files["storageType"],
                "clientKey": files["clientKey"],
                "file": (filename, f, "text/plain"),
            }
        )
    headers["content-type"] = m.content_type
    with client.post(url=url, headers=headers, data=m) as r:
        return r
