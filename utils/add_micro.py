import datetime
import csv
import argparse

# Parser setup
parser = argparse.ArgumentParser(description="Simple CMS for Microblogging")
parser.add_argument('content', type=str, nargs='?', help='Content of the microblog')

# Parse arguments
args = parser.parse_args()
if args.content:
    content = args.content
else:
    content = input("Enter the content of the microblog: ")

# Get current datetime and format it to "YYYY-MM-DD HH:MM"
publish_date = datetime.datetime.now()
formatted_date = publish_date.strftime("%Y-%m-%d %H:%M")

# Open CSV file and append a new row with formatted date and content
with open('./blog_app/db/micros.csv', 'a', encoding='UTF-8', newline='') as micros_db:
    writer = csv.writer(micros_db)
    writer.writerow([formatted_date, content])

print(f"Added microblog: {formatted_date} - {content}")
