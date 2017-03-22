import requests
import re
f=open('qiubai.txt','w')
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
         'Referer': 'https://www.google.com/'}

pattern=re.compile('<div.*?\"content\">[\n\r]*?<span>([\n\r]*?.*?[\n\r]*?)</span>[\n\r]*?</div>')
base_index=1
for page_num in range(50):
    url_req=requests.get('http://www.qiushibaike.com/8hr/page/{}/'.format(page_num), headers=headers)
    cont_str=url_req.content
    match_strs=pattern.findall(cont_str)
    for index, match_str in enumerate(match_strs):
        f.write('{}.  '.format(index+base_index))
        f.write(match_str)
        f.write('\n')

    base_index+=len(match_strs)-1
    print 'page {} done'.format(page_num)

f.close()




