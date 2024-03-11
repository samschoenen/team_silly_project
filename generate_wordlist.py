import csv
from collections import Counter

# Define the path to the CSV file
csv_file = 'alpaca_data_cleaned.csv'

# Define the column names in the CSV file
message_id_column = 'message_id'
msg_column = 'message'

# Create an empty list to store the words
word_list = []

# Read the CSV file and filter the data
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row[message_id_column] == '0':
            words = row[msg_column].split()
            word_list.extend(words)

# Count the occurrences of each word
word_count = Counter(word_list)

# Print the word count
for word, count in word_count.items():
    print(f'{word}: {count}')

# Save the word count to a file
word_count_file = 'word_count.txt'
with open(word_count_file, 'w') as file:
    for word, count in word_count.items():
        file.write(f'{word}: {count}\n')

print(f'Word count saved to {word_count_file}.')
