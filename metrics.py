from prometheus_client import Counter

gifs_posted = Counter('rainbow_gifs_gifs_posted', 'Number of gifs posted')

gifs_created = Counter('rainbow_gifs_gifs_created', 'Number of gifs that finish processing')