import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------
# 1. Load Dataset
# -----------------------------

data = pd.read_csv("data/scam_dataset.csv")
print("Dataset loaded successfully!")
print("Total records:", len(data))

print("\nCategory distribution:")
print(data["category"].value_counts())


# -----------------------------
# 2. Text Preprocessing
# -----------------------------

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


data["clean_message"] = data["message"].apply(clean_text)

print("\nOriginal and cleaned text:")
print(data[["message", "clean_message"]].head())


# -----------------------------
# 3. Train/Test Split
# -----------------------------

X = data["clean_message"]
y = data["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# 4. TF-IDF
# -----------------------------

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("\nTraining TF-IDF shape:", X_train_tfidf.shape)
print("Testing TF-IDF shape:", X_test_tfidf.shape)


# -----------------------------
# 5. Train ML Model
# -----------------------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train_tfidf, y_train)

print("\nModel trained successfully!")


# -----------------------------
# 6. Model Evaluation
# -----------------------------

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# -----------------------------
# 7. Test Custom Message
# -----------------------------

message = [
    "Congratulations! You won a lottery. Pay 500 to claim your prize."
]

message_clean = [clean_text(message[0])]

message_tfidf = vectorizer.transform(message_clean)

prediction = model.predict(message_tfidf)

probabilities = model.predict_proba(message_tfidf)

confidence = probabilities.max() * 100

print("\nCustom Message:")
print(message[0])

print("\nPrediction:", prediction[0])
print("Confidence:", round(confidence, 2), "%")