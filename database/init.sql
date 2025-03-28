CREATE TABLE IF NOT EXISTS reddit_posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    score INT,
    author TEXT,
    created_utc TIMESTAMP,
    permalink TEXT,
    url TEXT,
    num_comments INT,
    subreddit TEXT,
    keywords TEXT
);
