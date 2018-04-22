import pysolr
import sys
import json

solr=pysolr.Solr("http://localhost:23456/solr/s24_top")

result = solr.search(q="*.*", fl="s24_area_s, bestN_ss")

print("Found this many:", result.hits)
print("Here they are:", result.docs)
