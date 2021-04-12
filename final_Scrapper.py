import urllib
from urllib.parse import urlparse
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re   
import pandas as pd
import re   

reviewlist =[]

def getAll(productName):
    print()
    #  = input("product name :")
    query = productName+"'amazon.in'" 
    query = urllib.parse.quote_plus(query)
    number_result = 20

    ua = UserAgent()

    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")

    result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

    links = []
    titles = []
    descriptions = []
    for r in result_div:
        try:
            link = r.find('a', href = True)
            title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
            description = r.find('div', attrs={'class':'s3v9rd'}).get_text()

            if link != '' and title != '' and description != '': 
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
        except:
            continue


    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search('\/url\?q\=(.*)\&sa',l)

        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))

    # for x in to_remove:
    #     del titles[x]
    #     del descriptions[x]
    print()
    print('link :', clean_links[0])
    print()
    productLink = clean_links[0]
    
    productReviewsLink = productLink.replace('/dp/','/product-reviews/')
    print(productReviewsLink)


    def get_soup(URL):
        
        HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
        r = requests.get(URL, headers=HEADERS)

        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    # cleanLink()

    def get_reviews(soup):
        reviews = soup.find_all('div', {'data-hook': 'review'})
        try:
            for item in reviews:
                review = {
                'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                }
                reviewlist.append(review)
        except:
            pass





    for x in range(1,10):
        if x==1:
            reviewPageLink=str(f''+productReviewsLink)+str(f'/ref=cm_cr_dp_d_show_all_btm'+f'?ie=UTF8&reviewerType=all_reviews')
   
        else:
            reviewPageLink=str(f''+productReviewsLink)+str(f'/ref=cm_cr_dp_d_show_all_btm_next_{x}'+f'?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
        print(reviewPageLink)
        soup = get_soup(reviewPageLink)
        print(f'Getting page: {x}')
        # print(soup)
        get_reviews(soup)
        print(len(reviewlist))
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
    

    df = pd.DataFrame(reviewlist)
    df.to_excel('./reviews/'+ str(productName)+'.xlsx', index=False)



getAll("Redmi 9 (Sky Blue, 4GB RAM, ")
