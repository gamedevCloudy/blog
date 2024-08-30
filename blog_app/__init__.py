from flask import Flask, render_template
import csv
import os
from datetime import datetime

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

@app.route('/')
def blog(): 
    return render_template('index.html', micros=micros)

if __name__ == '__main__':
    app.run(debug=True)
