# train_improved.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import random
import re

# 1. Load
df = pd.read_csv("dataset_cleaned.csv")  # your cleaned CSV with columns 'label','message'

# 2. Normalize labels -> safe / unsafe
df['label'] = df['label'].replace({'social_engineering':'unsafe', 'safe':'safe', 'spam':'unsafe'})

# 3. Basic rule-based auto labelling to catch missed dangerous messages
# Add simple heuristics: URLs, urgent words, 'click', 'verify', 'password', money requests
url_regex = re.compile(r'https?://|www\.|\.[a-z]{2,3}/')
urgent_keywords = ['urgent', 'immediately', '24 hours', 'suspend', 'suspended', 'verify', 'click here',
                   'reset', 'password', 'account', 'bank', 'transfer', 'pay', 'login', 'secure-login']



def rule_label(text):
    t = str(text).lower()
    if url_regex.search(t):
        return 'unsafe'
    for k in urgent_keywords:
        if k in t:
            return 'unsafe'
    return None

# Apply rules to unlabeled or to confirm labels (optional)
df['auto_rule'] = df['message'].apply(rule_label)
# If rule says unsafe, set label to unsafe (this may overwrite some but helps boost positives)
df.loc[df['auto_rule']=='unsafe', 'label'] = 'unsafe'
df = df.drop(columns=['auto_rule'])

# 4. Balance classes: oversample minority (unsafe) to reach reasonable ratio
counts = df['label'].value_counts()
print("Before balancing:", counts.to_dict())

safe_df = df[df['label']=='safe']
unsafe_df = df[df['label']=='unsafe']

# if unsafe is small, oversample it up to ~50% of safe or at least 500 examples
target_unsafe = min(len(safe_df)//2, max(len(unsafe_df), 500))
if len(unsafe_df) < target_unsafe:
    extras = unsafe_df.sample(target_unsafe - len(unsafe_df), replace=True, random_state=42)
    df = pd.concat([safe_df, unsafe_df, extras], ignore_index=True)
else:
    df = pd.concat([safe_df, unsafe_df], ignore_index=True)

print("After balancing:", df['label'].value_counts().to_dict())

# 5. Simple synthetic augmentation for unsafe (tiny templates)
templates = [
    "Your account will be suspended in 24 hours. Click {} to restore now.",
    "We detected suspicious login. Reset your password here: {}",
    "Immediate action required: confirm payment at {}",
    "You've won a prize! Claim now: {}",
    "Verify your account: {} to avoid suspension"
]
def make_fake_link(i): return f"http://fake-link{i}.com/reset"

aug = []
for i, row in df[df['label']=='unsafe'].sample(min(200, len(df[df['label']=='unsafe'])), random_state=42).iterrows():
    tpl = random.choice(templates)
    aug.append({'label':'unsafe', 'message': tpl.format(make_fake_link(i))})
if aug:
    df = pd.concat([df, pd.DataFrame(aug)], ignore_index=True)

print("After augmentation:", df['label'].value_counts().to_dict())

# 6. Shuffle and prepare features
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
X = df['message']
y = df['label']

# 7. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 8. Vectorize
vectorizer = TfidfVectorizer(stop_words='english', max_features=8000)
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# 9. Model (add class_weight to help imbalance)
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_vect, y_train)

# 10. Evaluate
y_pred = model.predict(X_test_vect)
print(classification_report(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

# 11. Save
joblib.dump(model, "se_detector_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Saved new model and vectorizer")
