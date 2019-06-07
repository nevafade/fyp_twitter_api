import twitter
import json
api = twitter.Api(consumer_key='7WpfZGdrvuhsBf8n2Sa27xb7g',
                  consumer_secret='a5YE6A0DXwNEByvSkxA9WzT8IyoYjPX5xSBmZK9DlSP2mCspua',
                  access_token_key='1086125916051464192-LkOrybTgdCO6GYL0JW2ZAscv5q79H2',
                  access_token_secret='JNEfKGiDifQElw1YUMuvKPqkXCKI7IEyTnS7RaswQGW6u')


searchKeywordsFile = "certified_accounts.txt"
dumpFile = "true_post_dump.json"

searchRespArr = []

def getSearchKeywords():
    keywordSet = ["@narendramodi","@INCIndia","@BJP4India","@BJP4Gujrat","@timesofindia","@TimesNow","@ndtv","@SpokespersonECI","@arunjaitley","@ArvindKejriwal","@SheilaDikshit","@nsitharaman","@DefenceMinIndia","@PMOIndia", "@nitin_gadkari","@OfficeOfNG","@SushmaSwaraj","@MEAIndia","@Mayawati","@MamataOfficial","@nstomar","@rajnathsingh","@PIB_India","@IAF_MCC","@IndianDiplomacy","@crpfindia","@airnewsalerts","@airnewsalerts","@DDNewsLive","@mygovindia","@rashtrapatibhvn","@MIB_India","@PiyushGoyal","@DG_PIB","@IndianExpress", "@kgahlot" , "@htTweets" ,"@the_hindu" , "@htdelhi" , "@AamAadmiParty" ,"@aajtak" ,"@IndiaToday", "@FinMinIndia", "@rajeevkumr", "@RBI", "@FollowCII","@cbic_india", "@arivalayam","@ShivSena","@AUThackeray"]
    return keywordSet
    
def triggerSearches(searchTermSet):
     for term in searchTermSet:
        tweetSearch(term)
                
def tweetSearch(searchTerm):
    if searchTerm:
        data=api.GetUserTimeline(screen_name=searchTerm, count=200)
        data_array = []
        for tweet in data:
            data_array.append(tweet._json)
        searchRespArr.append(data_array);
        print "Done fetching search results for ",searchTerm," keyword."
    else:
        print "_tweetSearch_ Search term is null or undefined."      
    
def writeAllSearchRespOnDisk():
    with open(dumpFile, "w") as write_file:
        json.dump(searchRespArr, write_file)

dataKey = open(searchKeywordsFile)
searchTermSet = getSearchKeywords();
triggerSearches(searchTermSet);
writeAllSearchRespOnDisk();
  