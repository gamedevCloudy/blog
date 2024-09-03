from flask import Flask, render_template
import csv
import os
from datetime import datetime
from mistletoe import markdown
import html
app = Flask(__name__)

class Micro: 
    def __init__(self, publish_date, content): 
        parsed_date = datetime.strptime(publish_date, "%Y-%m-%d %H:%M")
        # Format date as 'YYYY-MM-DD' and time as 'HH:MM'
        self.publish_date = parsed_date.strftime("%d-%m-%Y")
        self.publish_time = parsed_date.strftime("%H:%M")
        self.content = content

def load_micros():
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
    
    if len(micros) >=3: 
        micros = micros[-3::]
        micros = micros[::-1]
        return micros
    return micros[::-1]

micros = load_micros()


def load_blogs(): 
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
                blog['permalink'] = row[4]

                blogs.append(blog)
           
    except Exception as e: 

        print("Failed loading blogs.. ")
        exit(e)
    # 
    blogs = blogs[-3:]
    blogs = blogs[::-1]
    return blogs

def load_posts(): 
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
                blog['permalink'] = row[4]
                blog['path'] = row[3]
                blogs.append(blog)
           
    except Exception as e: 

        print("Failed loading blogs.. ")
        exit(e)
    # 
    return blogs

blogs = load_blogs()
@app.route('/')
def blog(): 
    return render_template('index.html', micros=micros, blogs=blogs)

@app.get('/posts/<post_name>.html')
def go_to_blog(post_name):
    print(post_name)
    posts = load_posts()

    # Find the current post based on the permalink
    current_post = [post for post in posts if post['permalink'] == f'posts/{post_name}']
    fpath = app.root_path + current_post[0]['path'] + '.md'
    
    # Read the Markdown file content
    with open(fpath, 'r') as post_file:
        post_content = post_file.read()

    # Convert Markdown to HTML
    html_content = markdown(post_content)
   
    return render_template('blog.html', post = current_post[0], content = html_content)
if __name__ == '__main__':
    app.run(debug=True)


@app.get('/blogs.html')
def get_blogs(): 
    blogs = load_posts()

    return render_template('blogs.html', blogs = blogs[::-1])