import os
import re
import sys
import json
import math
import inflect
import operator
import csv
from word2number import w2n
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from autocorrect import spell
dictionary = {}
doc_freq_dictionary = {}
pattern = re.compile('[a-zA-Z0-9~]+')
count = 0
dictionary_final = {}
dictionary_idf = {}
def loadFiles():
	global dictionary
	global doc_freq_dictionary
	global pattern
	global count
	p = inflect.engine()
	data_path = os.path.join(os.getcwd(),"stories")
	for root_path,subdir,files in os.walk(data_path):
		print(root_path,subdir)
		for file in files:
			file_path = os.path.join(root_path,file)
			word_list = []
			with open(file_path,"r",errors='ignore') as f:
				for line in f:
					temp = pattern.findall(line)
					word_list+=temp
				count+=1
				print(file)

				word_list = stop_words_removal(word_list)
				for i in range(len(word_list)):
					if(word_list[i].isdigit()):
						try:
							word_list[i] = p.number_to_words(int(word_list[i]))
							temp = word_list[i].replace(",","")
							temp = temp.replace(" ","~")
							word_list[i] = temp
						except Exception as e:
							print("Number too large")
						
				# print(word_list)
				word_list = porter_stemmer(word_list)
				# print(word_list)

				for word in word_list:
					if not word in doc_freq_dictionary:
						doc_freq_dictionary[word] = []
						doc_freq_dictionary[word].append(file)
					else:
						doc_freq_dictionary[word].append(file)
			
	with open("doc_freq.json","w") as f:
		json.dump(doc_freq_dictionary,f,indent=4)

def stop_words_removal(word_list):
	main_words = []
	stop_words = set(stopwords.words('english'))
	for word in word_list:
		if not word in stop_words:
			main_words.append(word)
	return main_words

def porter_stemmer(word_list):
	ps = PorterStemmer()
	stemmed_list = [ps.stem(word) for word in word_list]
	return stemmed_list

def tf_idf():
	global dictionary
	global dictionary_final
	global dictionary_idf
	for key in dictionary:
		temp_list = dictionary[key]
		dict_temp = {}
		dictionary_idf[key] = math.log10(477/len(set(temp_list)))
		for files in temp_list:
			if files in dict_temp:
				dict_temp[files]+=1
			else:
				dict_temp[files]=1
		dictionary_final[key] = dict_temp
	with open("tf.json","w") as f:
		json.dump(dictionary_final,f,indent=4)
	with open("idf.json","w") as f:
		json.dump(dictionary_idf,f,indent=4)

def document_scores(query_tokens):
	global dictionary_idf
	global dictionary_final
	dictionary_score = {}
	for word in query_tokens:
		if(word in dictionary_final.keys()):
			temp_dict = dictionary_final[word]
			idf = dictionary_idf[word]
			for key in temp_dict:
				tf = 1+math.log10(temp_dict[key])
				score = tf*idf
				if key in dictionary_score:
					dictionary_score[key] +=score
				else:
					dictionary_score[key] = score
		else:
			print("Not found:\t",word)
	return dictionary_score

def title_score():
	global dictionary_final
	with open("index.csv",'rt') as f:
		data = csv.reader(f)
		for row in data:
			file = row[0]
			title = row[1]
			title_tokens = pattern.findall(title)
			title_tokens = stop_words_removal(title_tokens)
			title_tokens = porter_stemmer(title_tokens)
			word_list = title_tokens
			for i in range(len(word_list)):
				if(word_list[i].isdigit()):
					try:
						word_list[i] = p.number_to_words(int(word_list[i]))
						temp = word_list[i].replace(",","")
						temp = temp.replace(" ","~")
						word_list[i] = temp
					except Exception as e:
						print("Number too large")
			title_tokens = word_list
			for word in title_tokens:
				if word in dictionary_final:
					# print(dictionary_final[word])
					if file in dictionary_final[word]: 
						dictionary_final[word][file] +=10
					else:
						dictionary_final[word] = {file:10}
					# print(dictionary_final[word])
				else:
					dictionary_final[word] = {file:10}

def check_cache(query_tokens):
	# print(query_tokens)
	temp_dict = json.load(open("cache.json"))
	if query_tokens in temp_dict:
		print("Detected in cache:")
		print("Using Tf-Idf\n",temp_dict[query_tokens][0])
		print("Using cos sim:\n",temp_dict[query_tokens][1])
		sys.exit()


query = input("Enter your query:\n")
check_cache(query)
query_tokens = pattern.findall(query)
corrected_word_list = []
p = inflect.engine()
for word in query_tokens:
	if word.isdigit():
		temp = p.number_to_words(int(word))
		temp = temp.replace(",","")
		temp = temp.replace(" ","~")
		corrected_word_list.append(temp)
	else:	
		corrected_word_list.append(spell(word))

query_tokens = corrected_word_list
print("Corrected_word_list:\t",query_tokens)
query_tokens = stop_words_removal(query_tokens)
query_tokens = porter_stemmer(query_tokens)
print("Stemmed word \t",query_tokens)



# loadFiles()
dictionary = json.load(open("doc_freq.json"))
# tf_idf()
dictionary_idf = json.load(open("idf.json"))
dictionary_final = json.load(open("tf.json"))
title_score()
#print(dictionary_final)
# print(dictionary_idf)
print(count)


dictionary_score = document_scores(query_tokens)
result1 = sorted(dictionary_score.items(), key=operator.itemgetter(1),reverse=True)
result1 = result1[:5]
print(result1)

dictionary_tfidf_word = {}
size = len(query_tokens)
for word in query_tokens:
	if word in dictionary_tfidf_word:
		dictionary_tfidf_word[word]+=1
	else:
		dictionary_tfidf_word[word]=1

query_norm = 0
for key in dictionary_tfidf_word:
	dictionary_tfidf_word[key]/=size
	dictionary_tfidf_word[key]*=dictionary_idf[key]
	query_norm+= (dictionary_tfidf_word[key])**2

query_norm = query_norm**0.5 

print(dictionary_tfidf_word) 
dictionary_cosine = {}
dictionary_norm = {}
for word in query_tokens:
	temp_dict = dictionary_final[word]
	for file in temp_dict:
		norm = (temp_dict[file] * dictionary_idf[word])**2
		dot_product = temp_dict[file] * dictionary_idf[word] * dictionary_tfidf_word[word]
		if not file in dictionary_cosine:
			dictionary_cosine[file] = dot_product
			dictionary_norm[file] = norm
		else:
			dictionary_cosine[file]+=dot_product
			dictionary_norm[file]+=norm

for key in dictionary_norm:
	dictionary_norm[key] = dictionary_norm[key]**0.5

for key in dictionary_cosine:
	dictionary_cosine[key] = dictionary_cosine[key]/(dictionary_norm[key]*query_norm)

result2 = sorted(dictionary_cosine.items(), key=operator.itemgetter(1),reverse=True)
result2 = result2[:5]
print(result2)
dictionary_cache = {}
dictionary_cache = json.load(open("cache.json"))
if not query in dictionary_cache:
	dictionary_cache[query] = [result1,result2]
	# print(dictionary_cache)
	with open("cache.json","w") as f:
		json.dump(dictionary_cache,f,indent=4)



	