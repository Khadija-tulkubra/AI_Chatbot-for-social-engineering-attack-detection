import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load cleaned dataset
df = pd.read_csv("dataset_cleaned.csv")



# FIX: Convert labels to 2 categories
df['label'] = df['label'].replace({
    'social_engineering': 'unsafe',
    'safe': 'safe'
})

# Features and labels
X = df['message']
y = df['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Text vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Model
model = LogisticRegression()
model.fit(X_train_vect, y_train)

# Evaluate
y_pred = model.predict(X_test_vect)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, "se_detector_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model and vectorizer saved!")
