import urllib3

import json

owner = "venmo"
endpoint = f"orgs/{owner}/repos?per_page=100"


def main():
    headers = {
        "Accept": "application/vnd.github.squirrel-girl-preview+json",
        "User-Agent": "jwmarcus",
    }

    http = urllib3.PoolManager()
    r = http.request("GET", f"https://api.github.com/{endpoint}", headers=headers)

    if r.status == 200:
        res = json.loads(r.data.decode("utf-8"))
        print("INFO: Saving json response")

        with open("results.json", "w") as json_file:
            json.dump(res, json_file)
            print("INFO: json export complete")
    else:
        print(r.status)
        print(r.data)


if __name__ == "__main__":
    main()
