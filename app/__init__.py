from flask import Flask, render_template, make_response 
import csv
import os
from datetime import datetime
from mistletoe import markdown
from email.utils import format_datetime

app = Flask(__name__)

class Micro: 
    def __init__(self, publish_date, content): 
        parsed_date = datetime.strptime(publish_date, "%Y-%m-%d %H:%M")
        self.publish_date = parsed_date.strftime("%d-%m-%Y")
        self.publish_time = parsed_date.strftime("%H:%M")
        self.content = content

def load_micros(latest_k=0) -> list:
    """
    Get the latest 'k' micro blogs. 
    Default 'k' = 0 is an optional argument, so returns all micros sorted by date posted. 
    """
    micros = []
    CSV_FILE_PATH = os.path.join(app.root_path, 'db', 'micros.csv')
    
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:  # Ensure there are at least two columns
                    micros.append(Micro(row[0], row[1]))
    except FileNotFoundError:
        print(f"Error: {CSV_FILE_PATH} not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    
    if latest_k == 0: 
        return micros[::-1]
    else: 
        micros = micros[-(latest_k)::]
        micros = micros[::-1]
        return micros

def load_blogs(latest_k=0) -> list: 
    """
    Get the latest 'k' blogs. 
    Default 'k' = 0 is an optional argument, so returns all blogs sorted by date posted. 
    """
    blogs = []
    CSV_FILE_PATH = os.path.join(app.root_path, 'db', 'posts.csv')
    try: 
        with open(CSV_FILE_PATH, mode='r', encoding='UTF-8') as file: 
            reader = csv.reader(file)
            for row in reader: 
                blog= {}
                post_time = datetime.strptime(row[0], "%Y-%m-%d %H:%M")
                
                blog['datetime'] = post_time.strftime("%d-%m-%Y") + " " + post_time.strftime('%H:%M')
                blog['title'] = row[1]
                blog['description'] = row[2]
                blog['path'] = row[3]
                blog['permalink'] = row[4]

                blogs.append(blog)
           
    except Exception as e: 
        print("Failed loading blogs.. ")
        exit(e)
    
    if latest_k == 0: 
        return blogs[::-1]
    else: 
        blogs = blogs[-(latest_k):]
        blogs = blogs[::-1]
        return blogs

def read_content(post) -> str: 
    file_path = app.root_path +  post['path'] + '.md'
    print(file_path)
    with open(file_path, 'r') as f: 
        content = f.read()
    content = markdown(content)

    return content

@app.route('/')
def blog(): 
    blogs = load_blogs(latest_k=3)
    micros = load_micros(latest_k=3)
    return render_template('index.html', micros=micros, blogs=blogs)

@app.get('/posts/<post_name>.html')
def go_to_blog(post_name):
    posts = load_blogs()

    post_to_display = [post for post in posts if post['permalink'] == f'posts/{post_name}']

    content = read_content(post_to_display[0])

    return render_template('blog.html', post=post_to_display[0], content=content)

@app.get('/blogs.html')
def get_blogs(): 
    blogs = load_blogs()
    return render_template('blogs.html', blogs=blogs)

@app.get('/micros.html')
def get_micros(): 
    micros = load_micros() 
    return render_template('micros.html', micros=micros)

@app.route('/feed.xml')
def rss_feed():
    blogs = load_blogs()  # Fetch blog posts
    
    # Set the latest post date for the <lastBuildDate> in RSS feed
    if blogs:
        last_build_date = format_datetime(datetime.strptime(blogs[0]['datetime'], "%d-%m-%Y %H:%M"))
    else:
        last_build_date = format_datetime(datetime.now())


    for i in range(len(blogs)): 
        blogs[i]['content'] = read_content(blogs[i])
    
    # Render the RSS feed using an XML template
    rss = render_template('feed.rss', blogs=blogs, last_build_date=last_build_date)
    response = make_response(rss)
    response.headers['Content-Type'] = 'application/rss+xml'  # Ensure correct content type for RSS
    return response


@app.route('/nav.html')
def nav(): 
    return render_template('nav.html')

if __name__ == '__main__':
    app.run(debug=True)
