import pysolr
import sys

solr=pysolr.Solr("http://localhost:8983/solr/s24_top")

result=solr.search(q="*.*", fl="best1_s")
#result2=solr.serach(q="thread_txt_fi:Turku", fl="best1_s")

print("Found this many:", result.hits)
print("Here they are:", result.docs)


