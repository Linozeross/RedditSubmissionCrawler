# RedditSubmissionCrawler
Program that saves the submissions of given subreddits for later use.

# Usage
Run this file from the commandline with the following arguments:
1)  whether the program should fetch submissions by hour or by day. Fetching hourwise can lead to more submissions being found in popular subreddits, but takes longer.
2)  How many days/hours of submissions should be included.
3)  a list of subreddits to include

# Example
python RedditSubmissionCrawler.py days 10 relationships jokes

This would give you the submissions of the last 10 days in the subreddits /r/relationships and /r/jokes
