"""
Anthony Robnett
EN.625.800.21.FA22 Independent Study Fall 2022

Tutorial source reference:
    @article{angelov2020top2vec,
          title={Top2Vec: Distributed Representations of Topics},
          author={Dimo Angelov},
          year={2020},
          eprint={2008.09470},
          archivePrefix={arXiv},
          primaryClass={cs.CL}
    }
    https://github.com/ddangelov/Top2Vec#top2vec
    Top2Vec API Guide
    https://top2vec.readthedocs.io/en/latest/api.html
"""
# Imported Libraries:
import pandas as pd  # for data analysis tasks
import numpy as np
import matplotlib.pyplot as plt
from top2vec import Top2Vec
# Web scraped Sub-Reddit Text Data:
reddit_data = "data5.csv"
df = pd.read_csv(reddit_data)
# Multiply list by 10 for it to find at least 2 topics.
# https://stackoverflow.com/questions/65785949/valueerror-need-at-least-one-array-to-concatenate-in-top2vec-error
documents = df['Title'].tolist()*10
# Train Model
model = Top2Vec(documents=documents, speed="learn", min_count=10, workers=20)
# Get Number of Topics
print("The number of topics that Top2Vec has found in the data: ")
num_topics = model.get_num_topics()
print(num_topics)
# Get Topic Sizes
topic_sizes, topic_nums = model.get_topic_sizes()
print("The number of documents most similar to each topic: ")
print(topic_sizes)
print("The unique index of every topic will be returned: ")
print(topic_nums)
# Get Topics
topic_words, word_scores, topic_nums = model.get_topics(num_topics)
print("The top 50 words are returned, in order of semantic similarity to topic: ")
print(topic_words)
print("The cosine similarity scores of the top 50 words to the topic: ")
print(word_scores)
print("The unique index of every topic will be returned: ")
print(topic_nums)
# Search for topics most similar to "depression".
topic_words, word_scores, topic_scores, topic_nums = model.search_topics(keywords=["depression"], num_topics=5)
print("The top 50 words are returned, in order of semantic similarity to topic, 'depression': ")
print(topic_words)
print("The cosine similarity scores of the top 50 words to the topic: ")
print(word_scores)
print("The cosine similarity to the search keywords: ")
print(topic_scores)
print("The unique index of every topic will be returned: ")
print(topic_nums)
# Generate Word Clouds
topic_words, word_scores, topic_scores, topic_nums = model.search_topics(keywords=["depression"], num_topics=5)
print(topic_nums[0])
for topic in topic_nums:
    model.generate_topic_wordcloud(topic)
