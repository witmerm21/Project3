Project 3: Naïve Bayes Classifier 

All of the script files are saved on Picotte:
\ifs\group\eces450650Grp\ECES45060_WI\project3

All of the files share a similar naming pattern:
running type -> jelly/train/classify
taxa level -> k,p,c,o,f
which group it was in -> 1-5
how much of the original data was used for training -> 50/40/20

Classifiers also have n or f or near neighbor or far neighbor.

Example file name: trainc1_50.sh


Jellyfish files -> used to find the k-mers of each of the sequencess
They are labeled jellyc1_50.sh

Train files -> used to train the NBC on a particular training set
They are labeled trainc1_50.sh

Classify files -> used to classify a particular random set of sequences
They are labeled classify1_50.sh

There are three "master" files that run each script. So we could run one slurm job instead of 75-150.
jelly_run.sh  train_run.sh  classify_run.sh
