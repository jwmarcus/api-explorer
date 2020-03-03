#!/usr/bin/env python
# coding: utf-8

# # GitHub target account project parsing

# Import the proper libraries:

# In[ ]:


import pandas as pd
import urllib3

import json, time, os


# Setup connection pooling

# In[ ]:


http = urllib3.PoolManager()


# You must pass headers to the API (no base browsing). Also set the $GITHUB_OAUTH_KEY.

# In[ ]:


headers = {
    "Accept": "application/vnd.github.squirrel-girl-preview+json",
    "User-Agent": "jwmarcus",
    "Authorization": f"token {os.getenv('GITHUB_OAUTH_KEY')}"
}


# Define the org we want to parse, and get all the repos. Note: This works with orgs up to 100 repos. You will need to implement paging for larger orgs.

# In[ ]:


owner = "venmo"
endpoint = f"orgs/{owner}/repos?per_page=100"


# Call API and save results as JSON for later

# In[ ]:


if os.path.exists("results.json"):
    # Don't keep banging on the API if you don't need to
    print("INFO: Data exists! Delete results.json to pull fresh data")

else:
    r = http.request("GET", f"https://api.github.com/{endpoint}", headers=headers)

    if r.status == 200:
        res = json.loads(r.data.decode("utf-8"))
        print("INFO: Saving json response")

        with open("results.json", "w") as json_file:
            json.dump(res, json_file)
            print("INFO: json export complete")
    else:
        print(r.data)
        print(r.status)


# Import GitHub JSON dataset

# In[ ]:


df = pd.read_json("./results.json")


# Get just the repos that are _not_forks.

# In[ ]:


source_repos = df[df["fork"] == False]


# Get the urls of the contributors pages

# In[ ]:


# https://api.github.com/repos/{team-name}/{repo-name}/contributors

contrib_urls = source_repos["contributors_url"].tolist()


# Call each endpoint and save usernames of contributors

# In[ ]:


users = {}

for url in contrib_urls:
    # print(f"INFO: Getting {url}?per_page=100")
    r = http.request("GET", f"{url}?per_page=100", headers=headers)

    if r.status == 200:
        res = json.loads(r.data.decode("utf-8"))
        
        for user in res:
            num_contribs, repo_count = users.get(user["html_url"], (0,0)) 
            
            users[user["html_url"]] = (num_contribs + user["contributions"],
                                       repo_count + 1)
        
    else:
        print(r.status, r. headers)
    
    # Don't get rate limited
    time.sleep(0.25)

with open("contributors.json", "w") as f_contributors:
    json.dump(users, f_contributors)
    print("INFO: json export complete")


# Reload the saved JSON

# In[ ]:


df2 = pd.read_json("./contributors.json")


# Sort the data, first by key, then by contributions, then by repositories touched, grab the top 20.

# In[ ]:


df2.transpose().sort_index().sort_values([0,1], ascending=False).rename(columns={0: "Contributions", 1: "Repos"})[:20]

