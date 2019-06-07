from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
import os
import datetime
import twitter
import json
import csv
import re
api = twitter.Api(consumer_key='7WpfZGdrvuhsBf8n2Sa27xb7g',
                  consumer_secret='a5YE6A0DXwNEByvSkxA9WzT8IyoYjPX5xSBmZK9DlSP2mCspua',
                  access_token_key='1086125916051464192-LkOrybTgdCO6GYL0JW2ZAscv5q79H2',
                  access_token_secret='JNEfKGiDifQElw1YUMuvKPqkXCKI7IEyTnS7RaswQGW6u')

# Create your views here.
def refresh(request):
    archive_del()
    now = datetime.datetime.now()
    dumpFile = "true_post_dump_"+str(now)+".json"
    print dumpFile
    f = open('myapp/current.txt','w')
    f.write(dumpFile)
    f.close()
    searchRespArr = []
    searchTermSet = getSearchKeywords()
    searchRespArr = triggerSearches(searchTermSet,searchRespArr)
    writeAllSearchRespOnDisk(dumpFile,searchRespArr)
    return  HttpResponse('Disk write done')
    #json_reader()
    
    
    
def csvfile(request) :
    json_reader()
    return  HttpResponse('csv write done')
    
def getcsv(request):
    f = open('myapp/current.txt')
    d = f.readline()
    f.close()
    with open('myapp/'+d[0:len(d)-5]+'.csv') as send_file:
       response = HttpResponse(send_file, content_type='text/csv')
       response['Content-Disposition'] = 'attachment; filename=\"'+d[0:len(d)-5]+'.csv\"'
       return response
        
def json_reader():
    tweet_django_array = [];
    f = open('myapp/current.txt')
    d = f.readline()
    f.close()
    print d
    with open('myapp/'+d, "r") as read_file:
        tweet_array = json.load(read_file)
    print len(tweet_array)
    for tweet_sub_array in tweet_array:
        print len(tweet_sub_array)
        for tweet in tweet_sub_array:
            tweet_django_array.append([tweet['text'],tweet['lang']])
        

    with open('myapp/'+d[0:len(d)-5]+'.csv', 'w') as csvfile:
        fieldnames = ['news', 'fakeness']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ob in tweet_django_array :
            print tweet_django_array.index(ob)
            ___handle__error(ob[0],ob[1],writer)
    print  d[0:len(d)-5]+'.csv'
        
def ___handle__error(text,lang,writer):
    if((lang == 'en')|(lang == 'in')|(lang == 'ro')|(lang == 'sv')|(lang == 'da')|(lang == 'et')|(lang == 'tl')):
        try:
            writer.writerow({'news': text,'fakeness':'1'})
        except UnicodeEncodeError as e :
            out_of_bound_char = text[e.start]
            ___handle__error(re.sub(out_of_bound_char,'?',text),lang,writer)
        
        
def archive_del():
    f = open('myapp/current.txt','r')
    d = f.readline()
    os.remove('myapp/'+d)
    print 'ARCHIVED'
    
    
def getSearchKeywords():
    keywordSet = ["@narendramodi","@INCIndia","@BJP4India","@BJP4Gujrat","@timesofindia","@TimesNow","@ndtv","@SpokespersonECI","@arunjaitley","@ArvindKejriwal","@SheilaDikshit","@nsitharaman","@DefenceMinIndia","@PMOIndia", "@nitin_gadkari","@OfficeOfNG","@SushmaSwaraj","@MEAIndia","@Mayawati","@MamataOfficial","@nstomar","@rajnathsingh","@PIB_India","@IAF_MCC","@IndianDiplomacy","@crpfindia","@airnewsalerts","@airnewsalerts","@DDNewsLive","@mygovindia","@rashtrapatibhvn","@MIB_India","@PiyushGoyal","@DG_PIB","@IndianExpress", "@kgahlot" , "@htTweets" ,"@the_hindu" , "@htdelhi" , "@AamAadmiParty" ,"@aajtak" ,"@IndiaToday", "@FinMinIndia", "@rajeevkumr", "@RBI", "@FollowCII","@cbic_india", "@arivalayam","@ShivSena","@AUThackeray"]
    return keywordSet
    
def triggerSearches(searchTermSet,searchRespArr):
     for term in searchTermSet:
        searchRespArr = tweetSearch(term,searchRespArr)
     return searchRespArr
     
     
def tweetSearch(searchTerm,searchRespArr):
    if searchTerm:
        data=api.GetUserTimeline(screen_name=searchTerm, count=200)
        data_array = []
        for tweet in data:
            data_array.append(tweet._json)
        searchRespArr.append(data_array);
        print "Done fetching search results for ",searchTerm," keyword."
    else:
        print "_tweetSearch_ Search term is null or undefined."  
    return searchRespArr
    
def writeAllSearchRespOnDisk(dumpFile,searchRespArr):
    with open("myapp/"+dumpFile, "w") as write_file:
        json.dump(searchRespArr, write_file)