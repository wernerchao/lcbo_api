import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import json
import pandas as pd
from pandas.io.json import json_normalize

if __name__ == '__main__':
    http = urllib3.PoolManager()
    all_prod = []
    # Replace the access_key with your own key.
    access_key = 'MDpjOTNmYTljNi04ZTUwLTExZTctYTc1OC0wYmE0YTU2Yzc3NTk6M1N3WmNFeTdtdXFSMjVlYnJyZmNnWEx6UUxURm5DWkxNV2tD'

    # Get the max total page
    con = http.request('GET', 'https://lcboapi.com/products?access_key={}'.format(access_key))
    con = json.loads(con.data.decode('utf-8'))
    max_page = con['pager']['total_pages']

    # Loops through 586 pages. Currently, there are 586 pages. This number changes everyday.
    for i in range(1, max_page+1):
        req = http.request('GET', 'https://lcboapi.com/products?access_key={}&page={}'.format(access_key, i))
        req = json.loads(req.data.decode('utf-8'))
        print('Iteration ', i)
        if i == 1:
            all_prod = req['result']
        else:
            all_prod = all_prod + req['result']

    df = json_normalize(all_prod)
    print(df.shape)
    df.to_csv('lcbo_api_products.csv', index=False, encoding = 'utf8')
