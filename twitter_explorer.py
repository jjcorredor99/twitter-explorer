

import pandas as pd
import altair as alt
from datetime import datetime, timedelta,date
from collections import Counter
from operator import itemgetter
import tldextract
from wordcloud import WordCloud
from stop_words import get_stop_words
import matplotlib.pyplot as plt

def timeline (list_of_tweets, identifier):
	creation_dates=[tweet["created_at"] for tweet in list_of_tweets]
	df = pd.DataFrame({'dates':creation_dates})
	df.dates = df.dates.astype("datetime64")+ timedelta(hours=-5)
	df['just_date'] = df['dates'].dt.date

	counts= df.groupby(["just_date"]).size()
	counts=counts.to_frame(name = 'count').reset_index()
	counts.just_date=pd.to_datetime(counts.just_date)
	counts.sort_values(by=['just_date'])
	counts['just_date'] = pd.to_datetime(counts['just_date'])

	chart=alt.Chart(counts).mark_line(point=True).encode(
		x='just_date',
		y='count'
	).properties(
		title='Número de tuits en el tiempo'
	)
	chart.save("timeline_"+identifier+"_"+str(date.today())+".html")
	return (chart)

def most_used_hashtags(list_of_tweets,n):
	#Most used hashtags:
	hashtags=[]
	w_o_ht=[]
	for tweet in list_of_tweets:
		ht=[tweet["entities"]["hashtags"][i]["text"].lower()for i in range(0,len(tweet["entities"]["hashtags"]))]
		
		if len(ht)==0:
			w_o_ht.append(tweet) 
		else:
			hashtags=hashtags+ht

	c = Counter(hashtags)
	print(c.most_common(n))
	
	return(c)

def most_mentioned_users(list_of_tweets,n):
	#Most mentioned users:
	mentions=[]
	w_o_mt=[]
	for tweet in list_of_tweets:
		mt=[tweet["entities"]["user_mentions"][i]["screen_name"]for i in range(0,len(tweet["entities"]["user_mentions"]))]
		
		if len(mt)==0:
			w_o_mt.append(tweet) 
		else:
			mentions=mentions+mt

	c = Counter(mentions)
	print(c.most_common(n))

	return(c)

def most_used_urls(list_of_tweets,n):
	urls=[]
	sin_url=[]
	n_rts=[]
	for tweet in list_of_tweets:
		if "retweeted_status"in tweet.keys():
			url=[tweet["retweeted_status"]["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["retweeted_status"]["entities"]["urls"]))]
		elif "quoted_status"in tweet.keys():
			url=[tweet["quoted_status"]["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["quoted_status"]["entities"]["urls"]))]
			url=url.extend([tweet["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["entities"]["urls"]))])
		else:
			url=[tweet["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["entities"]["urls"]))]
		if url is not None:

			urls=urls+url

	c = Counter(urls)
	print(c.most_common(n))

	return(c)
	
def most_used_domains(list_of_tweets,n):
	urls=most_used_urls(list_of_tweets,0)
	dominios={}
	for url in urls.keys():
		ext = tldextract.extract(url)
		if ext.domain in dominios.keys():
			dominios[ext.domain]+=urls[url]
		else:
			dominios[ext.domain]=urls[url]
	dominios_sorted=dict(sorted(dominios.items(), key = itemgetter(1), reverse = True)[:n])
			
	print(dominios_sorted)
	return(dominios)



def most_retweeted_urls(list_of_tweets,n):
	#Most mentioned urls:
	urls={}
	sin_url=[]
	n_rts=[]
	for tweet in list_of_tweets:
		url=[tweet["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["entities"]["urls"]))]
		
		if len(url)==0:
			sin_url.append(tweet) 
		else:
			for u in url:
				if u in urls.keys():
					urls[u]=max(tweet['retweet_count'],urls[u])
				else:
					urls[u]=tweet['retweet_count']
		try:
			url=[tweet["retweeted_status"]["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["retweeted_status"]["entities"]["urls"]))]
			
			for u in url:
				if u in urls.keys():
					urls[u]=max(tweet['retweet_count']+tweet["retweeted_status"]['retweet_count'],urls[u])
				else:
					urls[u]=tweet['retweet_count']+tweet["retweeted_status"]['retweet_count']
			url=[tweet["quoted_status"]["entities"]["urls"][i]["expanded_url"]for i in range(0,len(tweet["quoted_status"]["entities"]["urls"]))]
			for u in url:
				if u in urls.keys():
					urls[u]=max(tweet['retweet_count']+tweet["quoted_status"]['retweet_count'],urls[u])
				else:
					urls[u]=tweet['retweet_count']+tweet["quoted_status"]['retweet_count']
					
		except:
			next

	urls_sorted=dict(sorted(urls.items(), key = itemgetter(1), reverse = True)[:n])
	print(urls_sorted)
	return(urls)

def most_retweeted_domains(urls,n):
	dominios={}
	for url in urls.keys():
		ext = tldextract.extract(url)
		if ext.domain in dominios.keys():
			dominios[ext.domain]+=urls[url]
		else:
			dominios[ext.domain]=urls[url]
	dominios_sorted=dict(sorted(dominios.items(), key = itemgetter(1), reverse = True)[:n])
			
	print(dominios_sorted)
	return(dominios)

def unify_text(list_of_tweets):
	for tweet in list_of_tweets:
		if "extended_tweet" in tweet.keys():
			tweet["unified_text"]=tweet["extended_tweet"]["full_text"]
		if "full_text" in tweet.keys():
			tweet["unified_text"]=tweet["full_text"]
		if "retweeted_status" in tweet.keys() and "extended_tweet" in tweet["retweeted_status"].keys():
			tweet["unified_text"]=tweet["retweeted_status"]["extended_tweet"]["full_text"]
		if "retweeted_status" in tweet.keys()and "full_text" in tweet["retweeted_status"].keys():
			tweet["unified_text"]=tweet["retweeted_status"]["full_text"]
		
		if "quoted_status" in tweet.keys() and "extended_tweet" in tweet["quoted_status"].keys():
			tweet["unified_text"]=tweet["text"]+tweet["quoted_status"]["extended_tweet"]["full_text"]
		
		if "quoted_status" in tweet.keys()and "full_text" in tweet["quoted_status"].keys():
			tweet["unified_text"]=tweet["text"]+tweet["quoted_status"]["full_text"]
		
		if  "quoted_status" in tweet.keys():
			tweet["unified_text"]=tweet["text"]+tweet["quoted_status"]["text"]
		

		if "unified_text" not in tweet.keys():
			tweet["unified_text"]=tweet["text"]
	
	return(list_of_tweets)

def sum_of_rts(list_of_tweets):
	for tweet in list_of_tweets:
		tweet["rts_global_count"]=tweet["retweet_count"]
		if "quoted_status" in tweet.keys():
			tweet["rts_global_count"]+=tweet["quoted_status"]['retweet_count']
		if "retweeted_status" in tweet.keys():
			tweet["rts_global_count"]+=tweet["retweeted_status"]['retweet_count']
	return(list_of_tweets)



def most_retweeted_tweets(list_of_tweets,n):
	tweets_procesados=unify_text(list_of_tweets)
	tweets_procesados=sum_of_rts(tweets_procesados)

	sorted_byRts=sorted(tweets_procesados, key = lambda i: i["rts_global_count"],reverse=True)

	#Most retwited twits:

	
	pd.set_option("max_colwidth",300)
	df = pd.DataFrame.from_dict(sorted_byRts)
	df['user'] = [list_of_tweets[i]["user"]["screen_name"] for i in range(0,len(list_of_tweets))]

	df=df[["id",'created_at','unified_text',"rts_global_count","user"]]

	return(df.head(n))

def find_tweets_by_id(list_of_tweets, id):
	trinos=[]
	for tweet in list_of_tweets:
		if tweet["id"]==id:
			trinos.append(tweet)
			print(tweet["text"])
	return(trinos)


#def most_used_emojies(list_of_tweets,n):
#	emojies=[]




def wordcloud_bios(list_of_tweets, name):
	
	bios=[tweet["user"]["description"] for tweet in list_of_tweets]
	bios=list(filter(None, bios))
	unique_bios=list(set(bios))
	bios_str=' '.join(unique_bios)
	bios_str=bios_str.lower()

	stopwords_es= get_stop_words('es')
	stopwords_es.append("rt")
	stopwords_es.extend(["https","co"])
	stopwords_es.extend( get_stop_words('en'))


	wordcloud = WordCloud(background_color ='white',stopwords=stopwords_es,width=800, height=400,collocations=True, normalize_plurals=False).generate(bios_str) 
	  
	# plot the WordCloud image                        
	plt.figure( figsize=(20,10) )
	plt.imshow(wordcloud) 
	plt.axis("off") 
	plt.savefig("./"+name+"png")
	plt.show() 


def wordcloud_tweets(list_of_tweets, name):
	tweets_procesados=unify_text(list_of_tweets)
	text=[tweet["unified_text"] for tweet in tweets_procesados]
	texto_str=' '.join(text)
	texto_str=texto_str.lower()
	stopwords_es= get_stop_words('es')
	stopwords_es.append("rt")
	stopwords_es.extend(["https","co"])
	stopwords_es.extend( get_stop_words('en'))

	wordcloud = WordCloud(background_color ='white',stopwords=stopwords_es,width=1000, height=500,collocations=True, normalize_plurals=False).generate(texto_str)

	# plot the WordCloud image                        
	plt.figure( figsize=(20,10) )
	plt.imshow(wordcloud) 
	plt.axis("off") 
	plt.savefig("./"+name+"png")
	plt.show() 

def find_tweets_by_text (list_of_tweets, list_of_terms):
	list_of_tweets=unify_text(list_of_tweets)
	filtered_tweets=[ x for x in list_of_tweets if any(word in x["unified_text"].lower() for word in list_of_terms)]
	return(filtered_tweets)

def wordcloud_filtered_tweets(list_of_tweets, list_of_terms,name):
	filtered_tweets=find_tweets_by_text (list_of_tweets, list_of_terms)
	wordcloud=wordcloud_tweets(filtered_tweets, name)




