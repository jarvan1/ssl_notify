import json
import time

import requests
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
import os


def send_msg(file_path):

    robot_url = 'https://oapi.dingtalk.com/robot/send?access_token='

    token = ''
    # dingtalk
    url = robot_url +token
    headers = {
        'Content-Type': 'application/json'
    }
    days_left, domain = get_num_days_before_expired(file_path)

    # if days_left < 30:
    #     payload = json.dumps(
    #         {
    #             "msg_type": "text",
    #             "content": {
    #                 "text": "- " + domain + "还有" + str(days_left) + " 天过期！请及时更新证书"
    #             }
    #
    #         }
    #     )
    if days_left < 30:
        # dingtalk
        payload = json.dumps(
            {
                "msgtype": "text",
                "text": {
                    "content": domain + "还有" + str(days_left) + " 天过期！请及时更新证书"
                }
            }
        )
        # feishu
        # payload = json.dumps(
        #     {
        #         "msg_type": "text",
        #         "text": {
        #             "content": domain + "还有" + str(days_left) + " 天过期！请及时更新证书"
        #         }
        #     }
        # )

        resp = requests.request('POST', url, headers=headers, data=payload)
        time.sleep(10)
        print(resp.content)
    #     if resp.status_code == 200:
    #         print(f"发送成功,域名{domain} 还有{days_left}天过期。")
    # else:
    #     print(f"域名{domain}还有{days_left}天")


def get_num_days_before_expired(base_path: str) -> tuple:
    """
    Get number of days before an TLS/SSL of a domain expired
    """
    file_paths = get_crt_file(base_path)
    for path in file_paths:
        with open(path, 'rb') as f:
            cert = x509.load_pem_x509_certificate(f.read())
            expiry_date = cert.not_valid_after
            delta = expiry_date - datetime.datetime.now()
            domain = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            # return delta.days, domain
            print(delta.days, domain)


def get_crt_file(base_path: str, target_suffix: str) -> list:
    cert_list = []
    for relpath, dirs, files in os.walk(base_path):
        if target_suffix in os.path.join(base_path, relpath, target_suffix):
            return cert_list.append(os.path.join(base_path, relpath, target_suffix))


if __name__ == '__main__':
    base_path = '/home/ec2-user/'
    send_feishu_msg(base_path)
