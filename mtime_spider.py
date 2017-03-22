import requests
import lxml
import time
import datetime
import re
import cPickle
import os
from io import BytesIO
from PIL import Image
import uuid
import random

def grab_movie_id(page_start,page_end):
    pattern = re.compile('<a target=\\\\"_blank\\\\" href=\\\\"http://movie.mtime.com/(.*?)/\\\\">')
    all_movie_indices=[]
    for page_num in range(page_start,page_end):
        time_str=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        page_index=page_num if page_num!=0 else 1
        request_num=page_num+1
        para={"Ajax_CallBack":"true",
        'Ajax_CallBackType':'Mtime.Channel.Pages.SearchService',
        'Ajax_CallBackMethod':'SearchMovieByCategory',
        'Ajax_CrossDomain':'1',
        'Ajax_RequestUrl':'http://movie.mtime.com/movie/search/section/?nation=138#pageIndex={}&nation=138'.format(page_index),
        't':time_str+'0437',
        'Ajax_CallBackArgument0':'',
        'Ajax_CallBackArgument1':'0',
        'Ajax_CallBackArgument2':'138',
        'Ajax_CallBackArgument3':'0',
        'Ajax_CallBackArgument4':'0',
        'Ajax_CallBackArgument5':'0',
        'Ajax_CallBackArgument6':'0',
        'Ajax_CallBackArgument7':'0',
        'Ajax_CallBackArgument8':'',
        'Ajax_CallBackArgument9':'0',
        'Ajax_CallBackArgument10':'0',
        'Ajax_CallBackArgument11':'0',
        'Ajax_CallBackArgument12':'0',
        'Ajax_CallBackArgument13':'0',
        'Ajax_CallBackArgument14':'1',
        'Ajax_CallBackArgument15':'0',
        'Ajax_CallBackArgument16':'1',
        'Ajax_CallBackArgument17':'4',
        'Ajax_CallBackArgument18':'{}'.format(request_num),
        'Ajax_CallBackArgument19':'0'}
        url_str='http://service.channel.mtime.com/service/search.mcs?'
        headers={'Referer':'http://movie.mtime.com/movie/search/section/?nation=138',
                 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        try:
            r = requests.get(url=url_str,params=para,headers=headers)
            cont_str=r.content
            movie_indices=pattern.findall(cont_str)
            all_movie_indices+=movie_indices
            print 'page {} done {} movies detected'.format(page_num,len(movie_indices))
        except:
            print 'page {} missing'.format(page_num)
        time.sleep(1)

    return all_movie_indices

def grab_img_url(movie_ids):
    list_pattern = re.compile('var imageList =(.*?)\n')
    img_url_pattern = re.compile('\\"img_1000\\":\\"(.*?jpg)\\"')
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    all_img_urls=[]
    for movie_id in movie_ids:
        url_str = 'http://movie.mtime.com/{}/posters_and_images/stills/hot.html'.format(movie_id)
        try:
            r = requests.get(url=url_str,headers=headers)
            cont_str=r.content
            cont_list = list_pattern.findall(cont_str)
            assert len(cont_list) == 1, 'pattern length >1'
            img_urls = img_url_pattern.findall(cont_list[0])
            all_img_urls+=img_urls
            print 'movie {} search done {} pictures detected'.format(movie_id,len(img_urls))
        except:
            print 'movie {} missing'.format(movie_id)

        time.sleep(0.5)

    return all_img_urls

def grab_img(img_urls):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    for url in img_urls:
        try:
            r = requests.get(url=url,headers=headers)
            img=Image.open(BytesIO(r.content))
            img_path='movie_img/{}.jpg'.format(uuid.uuid1())
            img.save(img_path)
            print 'image {} saved sucess'.format(img_path)

            time.sleep(random.uniform(0.5,1))

        except:
            print 'image {} failed'.format(url)




# all_indices=grab_movie_id(0,21)
# with open('movie_indices.pkl','w') as f:
#     cPickle.dump(all_indices,f)
#
# print 'total {} movies detected'.format(len(all_indices))

# with open('movie_indices.pkl') as f:
#     movie_ids=cPickle.load(f)
#
# movie_ids=set(movie_ids)
# movie_ids=list(movie_ids)
# img_urls=grab_img_url(movie_ids[:10])
# print 'total {} pictures detected'.format(len(img_urls))
#
# with open('img_urls.pkl','w') as f:
#     cPickle.dump(img_urls,f)

# get existed urls
if os.path.exists('img_urls.pkl'):
    with open('img_urls.pkl') as f:
        img_urls=cPickle.load(f)
# grab urls
else:
    # get existed movie indices
    if os.path.exists('movie_indices.pkl'):
        with open('movie_indices.pkl') as f:
            movie_ids=cPickle.load(f)
    # grab movie indices
    else:
        movie_ids=grab_movie_id(0,21)
        with open('movie_indices.pkl','w') as f:
            cPickle.dump(movie_ids,f)
        print 'total {} movies detected'.format(len(movie_ids))

    movie_ids=set(movie_ids)
    movie_ids=list(movie_ids)
    img_urls=grab_img_url(movie_ids[:10])
    print 'total {} pictures detected'.format(len(img_urls))

    with open('img_urls.pkl','w') as f:
        cPickle.dump(img_urls,f)

grab_img(img_urls)