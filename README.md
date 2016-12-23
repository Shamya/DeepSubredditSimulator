# Deep Learning based Subreddit simulator 

Reddit is a social news aggregation website with user-created sections called subreddits that are themed around a particular topic. We trained various models on an example subreddit's posts to generate human-like new posts. We explored n-grams, deep neural networks, and Markovify, an out-of-the-box markov chain generator. We evaluated these models using human ratings on applicability and coherence of a subsample of posts generated. We observe that although Markovify scored the best, neural models and n-gram generated more original posts. Neural models also needed larger corpus and higher training time as compared to n-grams and Markovify. Neural models also benefited learning English language representation by pre-training on a large OANC dataset.


##Code
neuralsubredditsimulator contains the modified torch-rnn program that we used for the neural models. main.py was the main script I used to run the models. The checkpoints were too large, so I removed them, but if the model were run again they would be generated in the cv folder.

Ngram_Markovify.ipynb is an iPython Notebook containing the code for the n-gram and Markovify models.
