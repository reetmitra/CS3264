import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_util import process_data

df = pd.read_csv('../dataset/andrew_diabetes.csv',sep=';')

df.head()

df.info()

# Train a Naive Bayes model

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# Split the data into training and testing sets
df = process_data(df)
X = df.drop('class', axis=1)
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Naive Bayes model
# In Weka:
# - useKernelEstimator: False -> Using GaussianNB (normal distribution assumption)
# - useSupervisedDiscretization: False -> No discretization preprocessing
nb_model = GaussianNB(
    # GaussianNB uses normal distribution assumption for features
    # which corresponds to Weka's default Naive Bayes with useKernelEstimator=False
    var_smoothing=1e-9  # Default, similar to Weka's default
)
nb_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = nb_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print(classification_report(y_test, y_pred, zero_division=1))

# Check class distribution in predictions
print(f"\nClass distribution in predictions: {np.bincount(y_pred)}")
print(f"Class distribution in test set: {np.bincount(y_test)}")

# Get class probabilities for a deeper look
y_prob = nb_model.predict_proba(X_test)
print(f"\nSample of class probabilities (first 5):")
for i in range(min(5, len(y_test))):
    print(f"Example {i+1}: Class 0 prob: {y_prob[i][0]:.4f}, Class 1 prob: {y_prob[i][1]:.4f}, True class: {y_test.iloc[i]}")

# Plot confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Diabetes', 'Diabetes'],
            yticklabels=['No Diabetes', 'Diabetes'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Naive Bayes Confusion Matrix')
plt.savefig('naivebayes_confusion_matrix.png')
plt.close()

# Optional: Display feature importance by class
print("\nFeature means by class:")
feature_means = {}
for i, class_label in enumerate([0, 1]):
    feature_means[f"Class {class_label}"] = pd.Series(nb_model.theta_[i], index=X.columns)

feature_means_df = pd.DataFrame(feature_means)
feature_means_df['Difference'] = abs(feature_means_df['Class 0'] - feature_means_df['Class 1'])
feature_means_df = feature_means_df.sort_values('Difference', ascending=False)
print(feature_means_df) 