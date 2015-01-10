import pandas as pd

#image_id,unixtime,rawtime,title,total_votes,reddit_id,number_of_upvotes,subreddit,number_of_downvotes,localtime,score,number_of_comments,username


def load_reddit_csv(fname):
    d = pd.read_csv('redditSubmissions.csv', sep=',', error_bad_lines=False, dtype={'unixtime': np.float64})
    return data
    

def plot_subs(data):
    subs = data['subreddit'].value_counts()
    ax = subs[:20].plot(kind='bar', title='Top 20 Subreddits From Data')
    ax.set_xlabel("Subreddits")
    ax.set_ylabel("Number of Submissions")
    plt.show()
