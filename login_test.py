import requests
import pytest
import hashlib

# 修改为你自己的后端地址和端口！！
BASE_URL = "http://localhost:21090"

def get_md5(pwd):
    """计算密码md5，和前端保持一致"""
    res = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
    print("当前生成md5：", res) #新增打印
    return res


def login_req(account, password_md5):
    url = BASE_URL + "/api/online-travel-sys/v1.0/user/login"
    json_body = {
        "userAccount": account,
        "userPwd": password_md5
    }
    resp = requests.post(url=url, json=json_body)
    return resp


class TestLogin:
    # 正向：正确账号密码登录
    def test_login_ok(self):
        resp = login_req("legal_gree01", "367d4417edbc5fa8b4e17dfe53539191")
        print("\n登录返回数据：", resp.json())
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        assert "token" in resp.json()["data"]

    # 反向：密码错误
    def test_login_wrong_pwd(self):
        resp = login_req("legal_gree01", "666666")
        print("\n密码错误返回：", resp.json())
        assert "密码错误" in resp.json()["msg"]

    # 反向：账号不存在
    def test_login_no_user(self):
        resp = login_req("abc9999", "123456")
        print("\n不存在账号返回：", resp.json())
        assert "账号不存在" in resp.json()["msg"]
