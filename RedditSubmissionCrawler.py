import requests
import sys
from tqdm import tqdm

# ----------------------------------------------------------------------------
#   This file gets the most recent posts of the specified subreddit.
#   All posts are saved in a textfile for later use.
#   This only includes post with a selftext. Images etc. are not retrieved.
#
#   Due to the limitations of the used PushShift API, only 500 submissions can be retrieved at a time. Therefore, one needs
#   to specify if the program should fetch submissions by hour or by day.
#
#   Usage:
#   Run this file from the commandline with the following arguments:
#   1)  whether the program should fetch submissions by hour or by day.
#       fetching hourwise can lead to more submissions being found in popular subreddits, but takes longer.
#   2)  How many days/hours of submissions should be included.
#   3)  a list of subreddits to include
#
#   Example:
#   python RedditSubmissionCrawler.py days 10 relationships jokes
#
#   This would give you the submissions of the last 10 days in the subreddits relationships and jokes
# ----------------------------------------------------------------------------


def getPostsofSubreddits(sublist, timePar = 'days', duration = 10):
    """
    :param self:
    :param sublist: List of subreddits to crawl.
    :param timePar: Choose whether posts of the last x hours, or the last x days should be considered. If hours are chosen,
     more posts will be found especially in popular subreddits.
    :param duration: The amount of hours or days to go back.
    :return:
    """
    #Exceptions
    if duration <= 0:
        raise ValueError("Can't use a negative duration!")
    if timePar != 'days' and timePar != 'hours':
        raise ValueError("Choose either days or hours!")

    #sets the correct string to extract submissions of the last days or hours
    if timePar == 'days':
        timeVar = 'd'
    elif timePar == 'hours':
        timeVar = 'h'

    for s in sublist:
        print ("Getting posts from subreddit /r/{}".format(s))
        output = []
        # Getting posts of each step.
        afterint = 1
        beforeint = 0

        # gets post from the last duration steps (hours or days).
        for counter in tqdm(range(0, duration)):
            # used to access api. the format is (number)d referring to the current date.
            # example: 23d -> the last 23 days
            after =  str(afterint) + timeVar
            before = str(beforeint) + timeVar
            # get redditposts using pushshift api
            getstr = "https://api.pushshift.io/reddit/search/submission/?subreddit={}&size=500&after={}&before={}".format(
                s, after, before)
            #UserAgent is needed to prevent reddit/pushshift from blocking the request
            response = requests.get(getstr, headers={'User-agent': 'DepressionBot'})
            data = response.json()
            # access json file
            for i in range(0, len(data["data"])):
                # only interested in selftext in this case, only include posts with selftext
                if 'selftext' in data["data"][i]:
                    op = data["data"][i]['selftext']
                    # remove all newlines (to preserve information, these could be escaped in the future)
                    op = op.replace('\n', ' ')
                    # don't include removed or deleted posts
                    if (op != "[removed]" and op != "[deleted]" and op !=''):
                        op = op + "\n"
                        output += op
            # to move one day backwards in time
            afterint += 1
            beforeint += 1

        # save as textfile: reddit {subreddit}.txt
        with open('output/reddit_sub_{}_last{}.txt'.format(s,after), 'w') as f:
            for k in output:
                f.write(k)


timePar = sys.argv[1]
duration = int(sys.argv[2])
subreddits = sys.argv[3:]

getPostsofSubreddits(subreddits,timePar,duration)
