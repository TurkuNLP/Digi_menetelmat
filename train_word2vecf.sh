W2VF=/home/ginter/word2vecf

python3 make_training_data.py | shuf > tr_data.w2vf
$W2VF/count_and_filter -train tr_data.w2vf -cvocab tr_data.cv -wvocab tr_data.wv -min-count 10
$W2VF/word2vecf -train tr_data.w2vf -wvocab tr_data.wv -cvocab tr_data.cv -output tr_data.vectors -size 50 -negative 10 -iters 5 -dumpcv context_biarcs.vectors -threads 24


