import json
from sklearn.model_selection import train_test_split

# Load JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Split data into features and labels
X = [entry['question'] for entry in data]
y = [entry['query'] for entry in data]

# Split data into training and validation sets (80% training, 20% validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

context = "You are a chat bot tasked with converting natural language queries into SQL queries given the following schema: \n\n" + open("../databaseFiles/schema.sql").read()

# Save training data to train.jsonl
with open('train.jsonl', 'w') as train_file:
    for question, query in zip(X_train, y_train):
        train_data = {
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": question},
                {"role": "assistant", "content": query}
            ]
        }
        train_file.write(json.dumps(train_data) + '\n')

# Save validation data to validation.jsonl
with open('validation.jsonl', 'w') as val_file:
    for question, query in zip(X_val, y_val):
        val_data = {
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": question},
                {"role": "assistant", "content": query}
            ]
        }
        val_file.write(json.dumps(val_data) + '\n')
