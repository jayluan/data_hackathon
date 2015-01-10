import praw
import pickle
import nltk
from sklearn.externals import joblib
from sklearn import linear_model

################################ BEGIN SUBROUTINES ######################################

def pickle_Load(fileName):
    f = open(fileName)
    tempFile = pickle.load(f)
    f.close()
    return tempFile

def get_subreddit_top_comments(subreddit, subLimit):
    r = praw.Reddit(user_agent='language_analyzer')
    submissions = r.get_subreddit(subreddit).get_top(limit=subLimit)
    comments = []
    for submission in submissions:
        for com in submission.comments:
            if not isinstance(com, praw.objects.Comment):
                continue
            #if (com.score>100 or com.score<-20):
            comments.append([com.body, com.score])
    return comments

def pos_tag_comments(comments):
    pos_tagger = pickle_Load('bigram_tagger.pkl')
    for comment in comments:
        sentences = nltk.sent_tokenize(comment[0])
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [pos_tagger.tag(sentence) for sentence in tokenized_sentences]
        comment[0] = tagged_sentences
    return comments

def get_politeness_scores(comments):
    politeness_scores = []
    for comment in comments:
        politeness_total = 0
        for sentence in comment[0].split("  "):
            vectorizer = joblib.load('Politeness_Vectorizer.pkl')
            model = joblib.load('Ridge_Politeness_Classifier.pkl')
            X_test = vectorizer.transform([sentence])
            prediction = model.predict(X_test)
            if prediction==0:  #0 => polite
                politeness_total += 1
            else:
                politeness_total -= 1
        politeness_scores.append(politeness_total)
    return politeness_scores

def get_sentiment_scores(comments):
    afinn = dict(map(lambda (k,v): (k,int(v)), [ line.split('\t') for line in open("AFINN-111.txt") ]))
    sentiment_scores = []
    for comment in comments:
        string_wo_punct = "".join(c for c in comment[0] if c not in ('!','.',':','?',';','"',')','(',']','[',','))
        sentiment_scores.append(sum(map(lambda word: afinn.get(word, 0), string_wo_punct.lower().split())))
    return sentiment_scores

def get_comment_length(comments):
    length_vector = []
    for comment in comments:
        length_vector.append(len(comment[0].split()))
    return length_vector    

def get_number_of_questions(comments):
    question_vector = []
    for comment in comments:
        question_vector.append(len(comment[0].split("?"))-1)
    return question_vector

################################ END SUBROUTINE #########################################

comments = get_subreddit_top_comments("relationship_advice", 1000)
comments += get_subreddit_top_comments("relationships",1000)
comments += get_subreddit_top_comments("dating_advice",1000)
politeness_vector = get_politeness_scores(comments)
sentiment_vector = get_sentiment_scores(comments)
length_vector = get_comment_length(comments)
question_vector = get_number_of_questions(comments)

for i in range(len(comments)):
    print str(comments[i][1])+","+str(politeness_vector[i])+","+str(sentiment_vector[i])+","+str(length_vector[i])+","+str(question_vector[i])





