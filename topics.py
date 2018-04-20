import pysolr
import sys

solr=pysolr.Solr("http://localhost:23456/solr/s24_top")

result2=solr.search(q="*.*", sort="date_dt desc", fl="id,best1_s")
result = solr.search(q="thread_txt_fi:koira")
result3 = solr.search(q="best1_s:lemmikki", sort="best1_f desc", fl="id,thread_txt_fi")

print("Found this many:", result3.hits)
print("Here they are:", result3.docs)




labels = open("topicnames.txt", 'r')

#for label in labels:
#    label=label.strip()
#    response=solr.search("best1_s:t_{}".format(label))
#    print("topic", label, "hits", response.hits)
