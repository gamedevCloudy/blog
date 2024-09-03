from app import app, load_posts
from flask_frozen import Freezer

# Initialize the Freezer with your Flask app
freezer = Freezer(app)

# Register a generator for dynamic routes (if any)
@freezer.register_generator
def go_to_blog():
    # Load all posts
    posts = load_posts()
    # Yield all dynamic URLs for posts
    for post in posts:
        # Assumes the 'permalink' is part of the URL for the post
        yield {'post_name': post['permalink'].split('/')[-1]}


# Enforce `.html` extension for URLs
@app.url_defaults
def add_extension(endpoint, values):
    if 'url' not in values:
        return
    if endpoint == 'go_to_blog' and not values['url'].endswith('.html'):
        values['url'] += '.html'
    if endpoint == 'blogs' and not values['url'].endswith('.html'):
        values['url'] += '.html'

if __name__ == '__main__':
    freezer.freeze()

if __name__ == '__main__':
    freezer.freeze()
