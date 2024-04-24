import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertTokenizer, BertModel, BertConfig
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the CSV data
data = pd.read_csv("./manual_keyword_selection/requests_mapped_to_keywords.csv")
if data.isnull():
    print("Data is null")

# Select only the "request" and "request_type" columns
selected_data = data[["request", "request_type"]]

# Split data into train and test sets
train_data, test_data = train_test_split(selected_data, train_size=1000, test_size=len(selected_data) - 1000, shuffle=True)

# Define a simple classifier on top of BERT
class Classifier(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x

# Define parameters
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
config = BertConfig.from_pretrained(model_name)
hidden_size = 256  # Size of hidden layer in the classifier

# Load BERT model
bert_model = BertModel.from_pretrained(model_name)

# Freeze BERT parameters
for param in bert_model.parameters():
    param.requires_grad = False

# Create classifier
output_size = len(train_data["request_type"].unique())  # Number of unique labels in the training data
classifier = Classifier(config.hidden_size, hidden_size, output_size)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(classifier.parameters(), lr=0.001)

# Convert labels to numerical values
label_encoder = LabelEncoder()
train_labels_encoded = label_encoder.fit_transform(train_data["request_type"])
test_labels_encoded = label_encoder.transform(test_data["request_type"])

# Tokenize input requests for train set
tokenized_train_texts = [tokenizer(request, return_tensors="pt", truncation=True, padding=True) for request in train_data["request"].tolist()]

# Tokenize input requests for test set
tokenized_test_texts = [tokenizer(request, return_tensors="pt", truncation=True, padding=True) for request in test_data["request"].tolist()]

# Prepare train set
train_inputs = [torch.tensor(tokenized_text["input_ids"]) for tokenized_text in tokenized_train_texts]
# Prepare test set
test_inputs = [torch.tensor(tokenized_text["input_ids"]) for tokenized_text in tokenized_test_texts]


# Train the classifier
for epoch in range(10):
    classifier.train()
    running_loss = 0.0
    for inputs, labels in zip(train_inputs, train_labels_encoded):
        optimizer.zero_grad()
        outputs = bert_model(inputs)[0].mean(dim=1).squeeze()
        outputs = classifier(outputs)
        loss = criterion(outputs.unsqueeze(0), torch.tensor([labels]))
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {running_loss}")

# Evaluate the classifier on the test set
classifier.eval()
predicted_labels = []
true_labels = []
for inputs, labels in zip(test_inputs, test_labels_encoded):
    outputs = bert_model(inputs)[0].mean(dim=1).squeeze()
    outputs = classifier(outputs)
    predicted_label = torch.argmax(outputs).item()
    predicted_labels.append(predicted_label)
    true_labels.append(labels)

# Calculate accuracy
accuracy = accuracy_score(true_labels, predicted_labels)
print(f"Accuracy: {accuracy}")
