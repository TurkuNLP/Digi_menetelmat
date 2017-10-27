
echo $f ;
zcat /home/mavela/cl2017/nodalida2/data/doc_ngrams/$1/full_text.txt.gz |
egrep -v "^#" |
head -50  |
cut -f 2 |
perl -pe 's/\n/ /g'

