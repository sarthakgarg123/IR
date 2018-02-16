import os	
import re
import json
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
location = os.getcwd() + "/" + "20_newsgroups" 
pattern=re.compile('[a-zA-Z1-9]+')
print (location)

choiceString = """
1)x or y
2)x and y
3)x and not y
4)x or not y
5)x and y (with skips)
"""

counter = 0
dictionary = {}
fileList = []
for folder in os.listdir(location):
	folderPath = location + "/" + folder
	print(folderPath)
	if os.path.isdir(folderPath):
		for file in os.listdir(folderPath):
			"""filePath = folderPath+ "/" + file
			counter = counter + 1
			f = open(filePath,"r",encoding='utf-8',errors='ignore')
			words = []	
			for line in f:
				try:
					encodedLine = line.encode("utf-8")
					decodedLine = encodedLine.decode()
					#print(decodedLine)
					temp = pattern.findall(decodedLine)
					words +=temp 
					#print(decodedLine,end='')
				except Exception as e:
					print("Non Ascii")
					raise e
			#print(file)
			
			mainWords = []
			stop_words = set(stopwords.words('english'))
			for r in words:
				if not r in stop_words:
					mainWords.append(r)
					#print(mainWords)
			ps = PorterStemmer()
			stemmedList = [ps.stem(word) for word in mainWords]
			#print (len(stemmedList))
			stemmedList = set(stemmedList)
			#print(len(stemmedList))"""
			fileNo=str(file)
			fileList.append(int(fileNo))
			"""for index in stemmedList:
				if index in dictionary:
					dictionary[index].append(int(fileNo))
				else:
					dictionary[index] = []
					dictionary[index].append(int(fileNo))
			"""
dictionary = json.load(open("pretty.json"))
# key_list = dictionary.keys()
# dlist = []
# def printWordCloud():
# 	text = open("data.txt").read()
# 	wordcloud = WordCloud().generate(text)
# 	#plt.imshow(wordcloud, interpolation='bilinear')
# 	#plt.axis("off")
# 	wordcloud = WordCloud(max_font_size=40).generate(text)
# 	plt.figure()
# 	plt.imshow(wordcloud, interpolation="bilinear")
# 	plt.axis("off")
# 	plt.show()
# for key in key_list:
# 	l=len(dictionary[key])
# 	for i in range(0,l):
# 		dlist.append(key)
# temp_file = open("data.txt","w")
# for item in dlist:
# 	temp_file.write("%s\n"%item)

# printWordCloud()
print(len(fileList))
print("Indexing completed.......")
for k in dictionary:
	dictionary[k].sort()  
fileList.sort()
#fileList = set(fileList)
#print(fileList)
#print("\n \n")
print(len(dictionary))
print("\n \n \n")
"""print(len(words))
print(words)
print("\n \n \n")
print(len(mainWords))
print(mainWords)
print("\n \n \n")
print(len(stemmedList))
print(stemmedList)
print("\n \n \n")
print(counter)
f2 = open("dictionary",'w')
json.dump(dictionary,f2)"""

while(1):
	print(choiceString)
	ps2 = PorterStemmer()
	choice = int(input("Enter your choice..\t"))
	word1 = input("Enter first name to search..\t")
	word2 = input("Enter second name to search..\t")
	list1 = dictionary.get(ps2.stem(word1))
	list2 = dictionary.get(ps2.stem(word2))
	#print(list1)
	#print("\n \n")
	#print(list2)
	i=j=0
	result = []
	if(choice==1):
		if not list1:
			result = list2
		elif not list2:
			result = list1
		else:
			while(i<len(list1) and j<len(list2)):
				if(int(list1[i])==int(list2[j])):
					result.append(list1[i])
					i+=1
					j+=1
				elif(int(list1[i])<int(list2[j])):
					result.append(list1[i])
					i+=1
				else:
					result.append(list2[j])
					j+=1
			while(i<len(list1)):
				result.append(list1[i])
				i+=1
			while(j<len(list2)):
				result.append(list2[j])
				j+=1
	elif(choice==2):
		if not list1 or not list2:
			result=[]
		else:
			countNormal=0
			print("Executing and... and lists not empty")
			while(i<len(list1) and j<len(list2)):
				#print(list1[i])
				#print(list2[j])
				if(int(list1[i])==int(list2[j])):
					result.append(list1[i])
					i+=1
					j+=1
				elif(int(list1[i])<int(list2[j])):
					i+=1
				else:
					j+=1
				countNormal+=1
			print("Running normally..." + str(countNormal))
	elif(choice==3):
		if not list1:
			result=[]
		if not list2:
			result=list1
		else:
			while(i<len(list1) and j<len(list2)):
				if(int(list1[i])==int(list2[j])):
					i+=1
					j+=1
				elif(int(list1[i])<int(list2[j])):
					result.append(list1[i])
					i+=1
				else:
					j+=1
			while (i<len(list1)):
				result.append(list1[i])
				i+=1
	elif(choice==4):
		temp = []
		if not list1:
			list1=[]
		elif not list2:
			list2=[]
		while(i<len(list1) and j<len(list2)):
				if(int(list1[i])==int(list2[j])):
					temp.append(list1[i])
					i+=1
					j+=1
				elif(int(list1[i])<int(list2[j])):
					i+=1
				else:
					j+=1
		result = [x for x in fileList if x not in list2]
		list1=result
		list2=temp
		result2 = []
		i=0
		j=0
		while(i<len(list1) and j<len(list2)):
				if(int(list1[i])==int(list2[j])):
					result2.append(list1[i])
					i+=1
					j+=1
				elif(int(list1[i])<int(list2[j])):
					result2.append(list1[i])
					i+=1
				else:
					result2.append(list2[j])
					j+=1
		while(i<len(list1)):
			result2.append(list1[i])
			i+=1
		while(j<len(list2)):
			result2.append(list2[j])
			j+=1

	elif(choice==5):
		listx = []
		listy = []	
		if not list1 or not list2:
			print("No Result Found")
			result=[]
		else:
			dict = {}
			print("\nExecuting and... and lists not empty\n")
			#numberOfSkips = int(input("\nEnter no. of skips\t"))
			numberOfSkips=1
			while(numberOfSkips<len(list1) and numberOfSkips<len(list2)):
				countSkip=0
				result=[]
				i=0
				j=0
				skipList1 = [0 for x in range(0,len(list1))]
				skipList2 = [0 for x in range(0,len(list2))]
				for x in range(0,len(list1),len(list1)//numberOfSkips):
					skipList1[x] = 1;
				for x in range(0,len(list2),len(list2)//numberOfSkips):
					skipList2[x] = 1;
				while(i<len(list1) and j<len(list2)):
					if(int(list1[i])==int(list2[j])):
						result.append(list1[i])
						i+=1
						j+=1
					elif(int(list1[i])<int(list2[j])):
						if(skipList1[i]==1 and i+numberOfSkips<len(list1) and (int(list1[i+numberOfSkips])<int(list2[j]))):
							i+=numberOfSkips
						else:
							i+=1
					else:
						if(j<len(list2)  and skipList2[j]==1 and j+numberOfSkips<len(list2) and (int(list2[j+numberOfSkips])<int(list1[i]))):
							j+=numberOfSkips
						else:
							j+=1
					countSkip+=1
					dict[numberOfSkips] = countSkip
				listx.append(numberOfSkips)
				listy.append(countSkip)
				numberOfSkips+=1
				print("No. of skips " + str(numberOfSkips) +"\t \t" +"No. of iterations " + str(countSkip))
			plt.plot(listx,listy)
			plt.xlabel('No. of skips')
			plt.ylabel('No. of iterations')
			plt.title('graph')
			plt.show()
	print("\n \n",result)

