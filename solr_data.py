import requests, json, gzip, pickle, os
import logging
logging.basicConfig(level=logging.INFO)

class DataGrabber:
	
	''' grab threads or comments from Solr based on query words (lemmas) '''
	
	
	def __init__(self, query_info, output_folder,address, core):
		self.query_field, self.query_words = query_info
		self.output_folder = output_folder
		self.user, self.passwd = "solr", "comhis"
		self.core = core
		self.address=address
		self.threads_per_query = 20 ## defaults
		self.threads_per_file = 10000
		self.comments_per_query = 100
		self.comments_per_file = 10000 ##

	def grab_threads(self):
		ids = self.find_thread_ids()
		self.download_threads(ids)
		
	def grab_comments(self):
		logging.info("Grabbing comments...")
		logging.info("Finding the amount of comments first...")
		query = self.make_id_query()
		params = {"q": query, "rows": 1, "wt":"json"}
		response=requests.get("{}/{}/select".format(self.address, self.core),data=params,auth=(self.user, self.passwd))
		count = int(json.loads(response.text)["response"]["numFound"])
		logging.info("Found {} comments in total...".format(count))
		self.download_comments(count)
		
	def download_comments(self, count):
		logging.info("Downloading all comments...")
		comments = {}
		file_c = 0
		for i in range(0, 500, self.comments_per_query):
			logging.info("Loading comments {} to {}".format(i, i+self.comments_per_query))
			query = self.make_id_query()
			print(query)
			params = {"q": query, "rows": self.comments_per_query, "start": i, "wt": "json"}
			response=requests.get("{}/{}/select".format(self.address, self.core),data=params,auth=(self.user, self.passwd))
			for doc_i, document in enumerate(json.loads(response.text)["response"]["docs"]):
				comments[i + doc_i] = document
			if len(comments) >= self.comments_per_file:
				logging.info("Saving to file, first {} comments found...".format(self.comments_per_file))
				self.save_data(comments, file_c, "comments")
				file_c += 1
				comments.clear()
		self.save_data(comments, file_c, "comments")
		
		
	def make_id_query(self):
#		q = []
#		for word in self.query_words:
#			q.append("{}:{}".format(self.query_field, word))
#		return " OR ".join(q)
		return "-lemma:turkulainen"# *:*"#"-lemma:köyhä -lemma:rutiköyhä -lemma:ruti#köyhä -lemma:rahaton -lemma:persaukinen -lemma:pers#aukinen -lemma:vähävarainen -lemma:vähä#varainen -lemma:perseaukinen -lemma:perse#aukinen -lemma:tyhjätasku -lemma:tyhjä#tasku -lemma:pienituloinen -lemma:pieni#tuloinen  -lemma:sossupummi -lemma:sossu#pummi -lemma:saita -lemma:sosiaalipummi -lemma:sosiaali#pummi -lemma:varaton -lemma:eläkeläinen -lemma:pienipalkkainen -lemma:pieni#palkkainen"
        
	def process_id_response(self, response):
		threads = set()
		response = json.loads(response.text)
		logging.info("Found comments in total: {}".format(response["response"]["numFound"]))
		for doc in response["response"]["docs"]:
			threads.add(doc["thread"])
		return threads
		
	def find_thread_ids(self):
		query = self.make_id_query()
		params = {"fl":"thread", "q":query, "rows":1000000, "wt":"json"}
		response=requests.get("{}/{}/select".format(self.address, self.core),data=params,auth=(self.user, self.passwd))
		ids = self.process_id_response(response)
		return ids
		
		
	def download_threads(self, ids):
		threads = {}
		file_c = 0
		counts = [0]
		max = 33716
		for thread_c, thread_id in enumerate(ids):
			logging.info("Thread: {} / {}  max: {}".format(thread_c, len(ids), max(counts)))
			params = {"q": "thread:{}".format(thread_id), "wt":"json", "rows": 10000}
			response = requests.get("{}/{}/select".format(self.address, self.core), data=params, auth=(self.user, self.passwd))
			threads[thread_id] = json.loads(response.text)["response"]
			found = int(threads[thread_id]["numFound"])
			counts.append(found)
			if len(threads) == self.threads_per_file:
				self.save_data(threads, file_c, "threads")
				threads.clear()
				file_c += 1
		self.save_data(threads, file_c, "threads")

	
	def save_data(self, threads, file_c, name):
		if not os.path.exists(self.output_folder):
			os.makedirs(self.output_folder)
		with gzip.open("{}/{}_{}.gz".format(self.output_folder, name, file_c), "wt") as gzip_file:
			gzip_file.write(json.dumps(threads))
		
			
	

if __name__ == "__main__":
	''' q_info = what data to load. list, where [0] = what field, [1] = list of words to have (OR) '''
	q_info = ["lemma", ["turkulainen"]]#["lemma", ["köyhä", "rutiköyhä", "ruti#köyhä", "rahaton", "persaukinen", "pers#aukinen", "vähävarainen", "vähä#varainen", "perseaukinen", "perse#aukinen", "tyhjätasku", "tyhjä#tasku", "pienituloinen", "pieni#tuloinen",  "sossupummi", "sossu#pummi", "saita", "sosiaalipummi", "sosiaali#pummi", "varaton", "eläkeläinen", "pienipalkkainen", "pieni#palkkainen"]]
	address = "http://evex.utu.fi/solr"
	core = "suomi24POS"
	grabber = DataGrabber(query_info=q_info, output_folder="comments_datapaja_verrokki", address=address, core=core)
	grabber.grab_comments()
		
			
