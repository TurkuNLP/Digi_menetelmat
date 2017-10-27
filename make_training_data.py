import glob
import random
import gzip


doc_dirs=glob.glob("/home/mavela/cl2017/nodalida_check/data/doc_ngrams/*")

#doc_dirs=glob.glob("/home/mavela/cl2017/cluster/data/doc_ngrams/*")


wanted = ["NOUN", "PROPN", "VERB", "ADV"]

random.shuffle(doc_dirs)

for doc_dir in doc_dirs:
    doc_num=doc_dir.split("/")[-1]
#    print(doc_dir)
    with gzip.open(doc_dir+"/full_text.txt.gz","rt",encoding="utf-8") as barcs:
        for line in barcs:
#            print("1", line)
            try:
                if not line.startswith("#"):
                    if not line.startswith("doc"):
#                        print(line)
                        cols=line.split("\t")
#                        if cols[3] in wanted:
##                            print(line)
                        print(int(doc_num),cols[2].lower(),sep="\t")
            except:
                continue


