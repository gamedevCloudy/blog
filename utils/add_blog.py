import datetime
import csv
import os
"""
CSV structure: 
- should contain post metadata: 
    - title
    - description
    - filepath
    - date 
    - permalink?
    - tags? 
- actual file is separate: contains content 
"""

DB_PATH = './app/db/posts.csv'

blog: dict= { 
    'date': None,
    'title': None,
    'description': None,
    'filepath': None,
    'permalink': None,
    'tags': None
}

t = datetime.datetime.now()
formatted_t = t.strftime("%Y-%m-%d %H:%M")
blog['date'] = formatted_t

# base title and description
blog['title'] = str(input('Blog Title: '))
blog['description'] = str(input('Description: '))


stripped_title: str = blog['title'].lower().strip().split(' ')
delimited_title: str = '-'.join(stripped_title)

# blog path
path: str= t.strftime("%Y-%m-%d") + '-' + delimited_title

blog['filepath'] = os.path.join('app', 'db', '_posts', path)
blog['permalink'] = os.path.join('posts', path)

# tags
tags = [tag for tag in str(input('Tags: ')).split()]
blog['tags'] = tags



try: 
    # create the blog
    filename = blog['filepath']+".md"
    print(filename)
    with open(filename, 'w', encoding='UTF-8') as blog_file: 
        print("a")
        content = str(input("Enter blog_file content: "))
        blog_file.writelines(content)
        blog_file.close()

except Exception as e:
    print("""\n Failed to write the blog.""")
    exit(e) 
# then create entry

try: 
    with open(DB_PATH, 'a') as blog_db: 
        writer = csv.writer(blog_db)
        writer.writerow(blog.values())
       
except Exception as e:
    print("""\n Failed to create DB Entry""")
    exit(e) 

