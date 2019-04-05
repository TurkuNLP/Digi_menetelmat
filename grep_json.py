import json, gzip, sys, os


#input_folder = "/home/avjves/s24/comments_new"
#input_folder= "no_koyha_words"
input_folder= "comments_datapaja_turkulainen"

files = os.listdir(input_folder)

def json2clean(data):
	Counter = 0
	for file in files:
		with gzip.open(input_folder + "/" + file, "rt") as data_file:
			data=json.loads(data_file.read())
			for comment_id, comment in data.items():
				try:
					lemma=comment["lemma"]
					id = comment["id"]
					text = comment["text"]
					pos = comment["pos"]
					date = comment["date"]
					sect= comment["sect"]
				except: continue
				try:
					subsect = comment["subsect"]
				except: subsect = "SUBSECT"
				try:
					user = comment["user"]
				except:
					user = "USER"
#				lemma,text,pos=clean_data(lemma,text,pos)
#				print(comment_id, "\t", id, "\t", lemma.lower())
				if date.startswith("2014"):
					Counter += 1
					if Counter <  50000:
#					print(date)
#					lemma,text,pos=clean_data(lemma,text,pos)
						print("#", "id:", id)
						print("#", "date:", date)
						print("#", "sect:", sect)
						print("#", "subsect:", subsect)
						print("#", "user:", user)
						for word, lemma, postag in zip(text.split(" "), lemma.split(" "), pos.split(" ")):
							# print(id, "\t", date, "\t", sect, "\t", subsect,  "\t", user, "\t",  word, "\t", lemma, "\t", postag)
							print(word, "\t", lemma, "\t", postag)
						print()
def clean_data(lemma,text,pos):
	to_keep = ["VERB", "NOUN", "PROPN", "ADJ", "ADV"]
	lemma = lemma.split(" ")
#	print("TT", text)
#	print("POS", pos)
	pos = pos.split(" ")
	text = text.split(" ")
	to_remove = []
	for i, tag in enumerate(pos):
#		print("TAG", tag)
		if tag not in to_keep: # and lemma[i] not in stop:
#			print("1", lemma[i])
			to_remove.append(i)
	for i, tag in enumerate(lemma):
		if tag.lower() in set(stop):
			if i not in to_remove:
				to_remove.append(i)
#	print("TO REMOVE", to_remove)
	for index in reversed(sorted(to_remove)):
#		print("index to remove", index)
#		print(lemma[index])
#		print(pos)
		del pos[index]
		del lemma[index]
		del text[index]
#	print("T", text)
	return(" ".join(lemma), " ".join(text), " ".join(pos))

json2clean(input_folder)
#			sys.stdout.write(id + "\t" + " ".join(lemma) + "\n")


#	for i in data.items():
#		print("i", i)

