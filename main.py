import urllib3

import json

owner = "venmo"
endpoint = f"/orgs/{owner}/repos"

def main():
    headers = {
        "Accept": "application/vnd.github.squirrel-girl-preview+json",
        "User-Agent": "jwmarcus",
    }

    http = urllib3.PoolManager()
    r = http.request("GET", f"https://api.github.com{endpoint}", headers=headers)

    if r.status == 200:
        res_json = json.loads(r.data.decode("utf-8"))
        # res_source = [x for x in res_json if not x["fork"]]
        # print(json.dumps(res_json, indent=2, sort_keys=True))
        print(r.headers)
    else:
        print(r.status)
        print(r.data)


if __name__ == "__main__":
    main()
