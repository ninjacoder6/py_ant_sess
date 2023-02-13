"""
Anthony Robnett
EN.605. 633 81 : Social Media Analytics
Module 11: Topic Modeling - Assignment
    Perform topic modeling for social media content of your choice with gensim or an
    alternative and visualize your results with a tool such as PyLDAvis.
Tutorial site reference:
    Topic Modeling in Python: Latent Dirichlet Allocation (LDA) by Shashank Kapadia
    https://towardsdatascience.com/end-to-end-topic-modeling-in-python-latent-dirichlet-allocation-lda-35ce4ed6b3e0
"""
# Wrapping the code exection logic into the if __name__ == '__main__' guard
# https://discuss.pytorch.org/t/runtimeerror-an-attempt-has-been-made-to-start-a-new-process-
# before-the-current-process-has-finished-its-bootstrapping-phase/145462
if __name__ == '__main__':
    # 1. Loading data &
    import pandas as pd # Importing modules
    import os
    os.chdir('..')
    # Read data into papers
    reddit_data = "C:/Users/arobn_avh2i9u/PycharmProjects/Independent Study/data5.csv"
    papers = pd.read_csv(reddit_data)
    print(papers.head())

    # 2. Data Cleaning
    # Remove the columns
   
    papers.head() # Print out the first rows of papers
    # Remove punctuation/lower casing
    import re # Load the regular expression library
    # Remove punctuation
    papers['paper_text_processed'] = papers['Title'].map(lambda x: re.sub('[,\.!?]', '', x))
    # Convert the titles to lowercase
    papers['paper_text_processed'] = papers['paper_text_processed'].map(lambda x: x.lower())
    papers['paper_text_processed'].head() # Print out the first rows of papers

    # 3. Exploratory analysis
    from wordcloud import WordCloud # Import the wordcloud library
    long_string =  ','.join(list(papers['Title'].values)) # Join the different processed titles together.
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string) # Generate a word cloud
    wordcloud.to_image() # Visualize the word cloud

    # 4. Preparing data for LDA analysis:
    import gensim
    from gensim.utils import simple_preprocess
    import nltk
    # nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True)) # deacc=True removes punctuations
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc))
                 if word not in stop_words] for doc in texts]
    data = papers.paper_text_processed.values.tolist()
    data_words = list(sent_to_words(data))
    data_words = remove_stopwords(data_words) # remove stop words
    print(data_words[:1][0][:30])
    import gensim.corpora as corpora
    id2word = corpora.Dictionary(data_words) # Create Dictionary
    texts = data_words # Create Corpus
    corpus = [id2word.doc2bow(text) for text in texts] # Term Document Frequency
    print(corpus[:1][0][:30]) # View

    # 5. LDA model training:
    # using fork to start your child processes
    # https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing
    '''import parallelTestModule
    if __name__ == '__main__':
        extractor = parallelTestModule.ParallelExtractor()
        extractor.runInParallel(numProcesses=2, numThreads=4)'''
    from pprint import pprint
    num_topics = 10 # number of topics
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics=num_topics) # Build LDA model
    pprint(lda_model.print_topics()) # Print the Keyword in the 10 topics
    doc_lda = lda_model[corpus]

    # 6. Analyzing LDA model results:
    # use gensim_models rather than gensim
    # https://stackoverflow.com/questions/66759852/no-module-named-pyldavis
    import pyLDAvis.gensim_models as gensimvis
    import pickle
    import pyLDAvis
    # Visualize the topics
    LDAvis_data_filepath = os.path.join('C:/Users/arobn_avh2i9u/PycharmProjects/'
                                        'Social Media Analytics/Module 11 Topic Modeling/'
                                        'ldavis_prepared_' + str(num_topics))
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)
    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)
    pyLDAvis.save_html(LDAvis_prepared, 'C:/Users/arobn_avh2i9u/PycharmProjects/'
                                        'Social Media Analytics/Module 11 Topic Modeling/'
                                        'ldavis_prepared_' + str(num_topics) + '.html')
    LDAvis_prepared


