import praw
from config.reddit_config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_PASSWORD, REDDIT_USERNAME, SUBREDDIT_NAME


def fetch_top_posts(limit=100, time_filter='day'):

    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=REDDIT_USER_AGENT
    )

    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    posts = []

    for post in subreddit.top(limit=limit, time_filter=time_filter):
        posts.append({
            "id": post.id,
            "title": post.title,
            "score": post.score,
            "author": str(post.author),
            "created_utc": post.created_utc,
            "permalink": post.permalink,
            "url": post.url,
            "num_comments": post.num_comments,
            "subreddit": str(post.subreddit),
        })

    return posts

if __name__ == "__main__":
    top_posts = fetch_top_posts()
    for post in top_posts:
        print(post)
