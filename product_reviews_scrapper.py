# import neccessary libraries or packages
import lxml
import csv
import re
from urllib.request import Request,urlopen
import urllib.request
import bs4 as bs
import time
# the open function create the file in this case it is csv file
file = open('negative_and_neutra_reviews.csv','w+',encoding='utf-8',newline='')
file1 = csv.writer(file)
file1.writerow(["Review_title","Review_text","Review_rating","Review_data","Review_link"])
pages = []
# the following is used to save all the links in pages list and then we will use it below to go through all the webpages
for i in range(1,10):
    # the link of the webpages0
    url = 'https://www.amazon.com/BLU-Studio-6-0-HD-Smartphone/product-reviews/B00PYWQ7R4/ref=cm_cr_getr_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&filterByStar=critical&pageNumber=' + str(
        i)
    pages.append(url)
j = 0
date_l = []
rating = []
title = []
review = []
# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
# in the following loop we will actually start making request and then pull some data
for item in pages:
    # here we will send a request to a webpage
    p = urllib.request.Request(item,data=None,headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'})
    page = urllib.request.urlopen(p).read()
    # make it a little clean with beautifulsoup package
    soup = bs.BeautifulSoup(page, 'lxml')

    # find the div tag whose class is equal to the given below
    user_reviews = soup.find(class_='a-section a-spacing-none review-views celwidget')
    # find all those span tag whose class is equal to a-size-base review-text
    user_reviews_in_p = user_reviews.find_all('span', class_='a-size-base review-text')
    # find all those span tag whose class is equal to a-icon-alt
    user_reviews_star_in_div = user_reviews.find_all('span', class_='a-icon-alt')
    user_reviews_title_in_a = user_reviews.find_all('a',
                                                    class_='a-size-base a-link-normal review-title a-color-base a-text-bold')
    # find all dates of the reviews inside span tag whose class is a-size-base a-color-secondary review-date
    user_reviews_date_in_span = user_reviews.find_all('span', class_='a-size-base a-color-secondary review-date')
    # for finding all the links of the reviews in a tag whos class is a-link-normal
    user_reviews_link_in_a = user_reviews.find_all('a',class_='a-size-base a-link-normal review-title a-color-base a-text-bold',
                                                   attrs={'href': re.compile("^/gp/customer-reviews")})
    # for putting all the links in review_link list
    for review_link in user_reviews_link_in_a:
        review.append("https://www.amazon.com" + review_link['href'])
    # for putting review date in date list
    for date_text in user_reviews_date_in_span:
        date_l.append(date_text.text)
    # for putting the text of title in title list
    for title_text in user_reviews_title_in_a:
        title.append(title_text.text)
    # in the following loop we will get the rating of the reviews
    for star in user_reviews_star_in_div:
        if (star.text == '|'):
            continue
        else:
            # we will get only the 1st integer out of the string which is 5.0 out of 5 and append it to a list rating
            rating.append(re.findall('\d+', star.text)[0])
    print(len(review))
    print(len(rating))
    print(len(title))
    print(len(date_l))

    for comments in user_reviews_in_p:
        print(comments.text)
        file1.writerow([title[j],comments.text,rating[j],date_l[i],review[i]])
        j = j + 1


