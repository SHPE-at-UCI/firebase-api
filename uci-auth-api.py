# uci-auth-api.py
from urllib import urlencode
from sheets_api_client import SheetsApiClient
import requests


class UciAuthApi:
    def __init(self):
        self.sheetsApi = SheetsApiClient()

    def uci_signin(self):
        param = urlencode({"return_url": "http://shpe.uci.edu:5000/login"})
        webauth = "http://login.uci.edu/ucinetid/webauth?" + param

        login_status = self.refresh_login_status()
        if not login_status:
            return "UCI login failed"
        elif login_status["valid"]:
            print(login_status)
            return self.sheetsApi.signin_user(login_status["ucinetid"])
        else:
            return webauth

    def logout(self):
        param = urlencode({"return_url": "http://shpe.uci.edu:5000/logout"})
        webauth = "http://login.uci.edu/ucinetid/webauth_logout?" + param

        login_status = self.refresh_login_status()

        # TODO: Fix Login status so users can sign-in with UCI account
        return "UCI logout failed"

        if login_status["valid"]:
            return webauth
        else:
            # go to homepage
            return "/"

    def refresh_login_status(self):
        login_status = None
        uci_cookie = "ucinetid_auth"

        if uci_cookie in requests.cookies:
            login_status = {}
            param = urlencode({uci_cookie: requests.cookies.get(uci_cookie)})
            webauth_check = "http://login.uci.edu/ucinetid/webauth_check"
            resp = requests.get(webauth_check + "?" + param)
            resp = resp.content.decode("utf-8")

            for line in resp.split("\n"):
                key_val = line.split("=")
                if len(key_val) != 2 or key_val[1] == "":
                    continue
                elif len(key_val) == 2 and key_val[0] == "uci_affiliations":
                    login_status[key_val[0]] = set(key_val[1].split(","))
                else:
                    login_status[key_val[0]] = key_val[1]

            login_status["valid"] = False

            theres_err_code = "error_code" in login_status
            theres_auth_fail = "auth_fail" in login_status
            theres_ucinetid = "ucinetid" in login_status
            theres_timestamp = "time_created" in login_status
            valid_auth_host = (
                login_status["auth_host"] == login_status["x_forwarded_for"]
            )

            if theres_err_code or theres_auth_fail:
                print("Error Code:", login_status.get("error_codes"))
                print("Authentication Failure:", login_status.get("auth_fail"))

            elif theres_ucinetid and theres_timestamp and valid_auth_host:
                login_status["valid"] = True

        return login_status
