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

blog = {
    'date': datetime.datetime.now(),
    'title': None,
    'description': None,
    'filepath': None,
    'permalink': None,
    'tags': None
}

# base title and description
blog['title'] = str(input('Blog Title: '))
blog['description'] = str(input('Description: '))

stripped_title = blog['title'].split(' ')
delimited_title = '-'.join(stripped_title)

# blog path
path = blog['date'].strftime("%Y-%m-%d") + '-' + delimited_title

blog['filepath'] = os.path('app', 'db', '_posts', path)
blog['permalink'] = os.join('posts', path)

# tags
tags = [tag for tag in str(input('Tags: ')).split()]
blog['tags'] = tags



try: 
    # create the blog
    with open(blog['filepath']+ '.md', 'w', encoding='UTF-8') as blog: 
        blog.write(blog['content'])

    # then create entry
    try: 
        with open(DB_PATH, 'a'): 
            writer = csv.writer()
            writer.write(
                list(blog)
            )
    except Exception as e:
        print("""\n Failed to create DB Entry""")
        exit(e) 

except Exception as e:
    print("""\n Failed to write the blog.""")
    exit(e) 
