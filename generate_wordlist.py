import csv
from collections import Counter
import re

# Define the path to the CSV file
csv_file = 'alpaca_data_cleaned.csv'

# Define the column names in the CSV file
message_id_column = 'message_id'
msg_column = 'message'

# Create an empty list to store the words
word_list = []

# Read the CSV file and filter the data
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row[message_id_column] == '0':
            # Tokenize the text into words (ignoring punctuation)
            words = re.findall(r'\b\w+\b', row[msg_column].lower())
            word_list.extend(words)

# Count the occurrences of each word
word_count = Counter(word_list)

# Sort the word count by count in descending order
sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))

# Print the sorted word count
for word, count in sorted_word_count.items():
    print(f'{word}: {count}')

# Save the sorted word count to a file
word_count_file = 'word_count.txt'
with open(word_count_file, 'w', encoding='utf-8') as file:
    for word, count in sorted_word_count.items():
        file.write(f'{word}: {count}\n')

print(f'Word count saved to {word_count_file}.')

