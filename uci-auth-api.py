# uci-auth-api.py


def uci_signin():
    resp = None
    param = urlencode({"return_url": "http://shpe.uci.edu:5000/login"})
    webauth = "http://login.uci.edu/ucinetid/webauth?" + param

    login_status = refresh_login_status()
    if not login_status:
        return "UCI login failed"
    elif login_status["valid"]:
        print(login_status)
        return signin_user(login_status["ucinetid"])
    else:
        return redirect(webauth)


def logout():
    resp = None
    param = urlencode({"return_url": "http://shpe.uci.edu:5000/logout"})
    webauth = "http://login.uci.edu/ucinetid/webauth_logout?" + param

    login_status = refresh_login_status()

    # TODO: Fix Login status so users can sign-in with UCI account
    return "UCI logout failed"

    if login_status["valid"]:
        return redirect(webauth)
    else:
        return redirect("/")


def refresh_login_status():
    login_status = None
    uci_cookie = "ucinetid_auth"

    if uci_cookie in request.cookies:
        login_status = {}
        param = urlencode({uci_cookie: request.cookies.get(uci_cookie)})
        webauth_check = "http://login.uci.edu/ucinetid/webauth_check"
        resp = requests.get(webauth_check + "?" + param).content.decode("utf-8")

        for line in resp.split("\n"):
            key_val = line.split("=")
            if len(key_val) != 2 or key_val[1] == "":
                continue
            elif len(key_val) == 2 and key_val[0] == "uci_affiliations":
                login_status[key_val[0]] = set(key_val[1].split(","))
            else:
                login_status[key_val[0]] = key_val[1]

        login_status["valid"] = False
        if "error_code" in login_status or "auth_fail" in login_status:
            print("Error Code:", login_status.get("error_codes"))
            print("Authentication Failure:", login_status.get("auth_fail"))
        elif (
            "ucinetid" in login_status
            and "time_created" in login_status
            and login_status["auth_host"] == login_status["x_forwarded_for"]
        ):
            login_status["valid"] = True

    return login_status
