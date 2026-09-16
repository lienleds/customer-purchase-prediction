"""
Customer Purchase Prediction using Logistic Regression
AI Foundation Training Exercise

This script builds a Logistic Regression model to predict whether a customer 
will make a purchase based on their Age and EstimatedSalary.

Author: AI Foundation Student
Date: 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import warnings

warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# STEP 1: LOAD AND EXPLORE THE DATASET
# ============================================================================
print("=" * 80)
print("STEP 1: LOAD AND EXPLORE THE DATASET")
print("=" * 80)

# Load the dataset
df = pd.read_csv('Social_Network_Ads.csv')

# Display basic information
print("\n1.1 Dataset Overview:")
print(f"Dataset shape: {df.shape}")
print(f"Total records: {len(df)}")
print(f"Total features: {len(df.columns)}")

print("\n1.2 First 5 rows of the dataset:")
print(df.head())

print("\n1.3 Dataset Info:")
print(df.info())

print("\n1.4 Statistical Summary:")
print(df.describe())

# Check for missing values
print("\n1.5 Missing Values:")
print(df.isnull().sum())

# Check for duplicates
print(f"\n1.6 Duplicate records: {df.duplicated().sum()}")

# Check class distribution
print("\n1.7 Class Distribution (Purchase behavior):")
print(df['Purchased'].value_counts())
print("\nPurchase distribution (%):")
print(df['Purchased'].value_counts(normalize=True) * 100)

# ============================================================================
# STEP 2: DATA CLEANING
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: DATA CLEANING")
print("=" * 80)

# Since there are no missing values or duplicates, data is clean
print("\n✓ Dataset is clean - No missing values or duplicates found!")
print("✓ All features are numerical - No encoding needed")

# ============================================================================
# STEP 3: SELECT FEATURES
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: SELECT FEATURES")
print("=" * 80)

# Select features (Age and EstimatedSalary) and target (Purchased)
X = df[['Age', 'EstimatedSalary']]  # Features
y = df['Purchased']                  # Target variable

print("\nFeatures selected:")
print("  - Age")
print("  - EstimatedSalary")
print(f"\nFeature matrix shape: {X.shape}")
print(f"Target vector shape: {y.shape}")

print("\nFeature correlations with Purchase decision:")
correlation = df[['Age', 'EstimatedSalary', 'Purchased']].corr()
print(correlation)

# ============================================================================
# STEP 4: SPLIT DATA
# ============================================================================
print("\n" + "=" * 80)
print("STEP 4: SPLIT DATA INTO TRAINING AND TESTING SETS")
print("=" * 80)

# Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
print(f"Testing set size: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")

print(f"\nTraining set purchase distribution:")
print(y_train.value_counts())
print(f"\nTesting set purchase distribution:")
print(y_test.value_counts())

# ============================================================================
# STEP 5: FEATURE SCALING
# ============================================================================
print("\n" + "=" * 80)
print("STEP 5: FEATURE SCALING")
print("=" * 80)

# Apply StandardScaler to normalize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\nFeature scaling applied using StandardScaler")
print("\nBefore scaling - Training set statistics:")
print(f"  Age - Mean: {X_train['Age'].mean():.2f}, Std: {X_train['Age'].std():.2f}")
print(f"  Salary - Mean: {X_train['EstimatedSalary'].mean():.2f}, Std: {X_train['EstimatedSalary'].std():.2f}")

print("\nAfter scaling - Training set statistics:")
print(f"  Age - Mean: {X_train_scaled[:, 0].mean():.4f}, Std: {X_train_scaled[:, 0].std():.4f}")
print(f"  Salary - Mean: {X_train_scaled[:, 1].mean():.4f}, Std: {X_train_scaled[:, 1].std():.4f}")

# ============================================================================
# STEP 6: TRAIN LOGISTIC REGRESSION MODEL
# ============================================================================
print("\n" + "=" * 80)
print("STEP 6: TRAIN LOGISTIC REGRESSION MODEL")
print("=" * 80)

# Create and train the model
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train_scaled, y_train)

print("\n✓ Logistic Regression model trained successfully!")

print("\nModel Parameters:")
print(f"  Coefficients: {lr_model.coef_[0]}")
print(f"  Intercept: {lr_model.intercept_[0]:.4f}")

# Feature importance
print("\nFeature Importance (Coefficients):")
feature_importance = pd.DataFrame({
    'Feature': ['Age', 'EstimatedSalary'],
    'Coefficient': lr_model.coef_[0],
    'Absolute_Coefficient': np.abs(lr_model.coef_[0])
})
feature_importance = feature_importance.sort_values('Absolute_Coefficient', ascending=False)
print(feature_importance)

# ============================================================================
# STEP 7: EVALUATE MODEL
# ============================================================================
print("\n" + "=" * 80)
print("STEP 7: EVALUATE MODEL")
print("=" * 80)

# Make predictions on both training and testing sets
y_pred_train = lr_model.predict(X_train_scaled)
y_pred_test = lr_model.predict(X_test_scaled)

# Calculate accuracy scores
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\n7.1 Accuracy Scores:")
print(f"  Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"  Testing Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Confusion Matrix
cm_train = confusion_matrix(y_train, y_pred_train)
cm_test = confusion_matrix(y_test, y_pred_test)

print(f"\n7.2 Confusion Matrix (Training Set):")
print(cm_train)
print(f"\n  True Negatives: {cm_train[0, 0]}")
print(f"  False Positives: {cm_train[0, 1]}")
print(f"  False Negatives: {cm_train[1, 0]}")
print(f"  True Positives: {cm_train[1, 1]}")

print(f"\n7.3 Confusion Matrix (Testing Set):")
print(cm_test)
print(f"\n  True Negatives: {cm_test[0, 0]}")
print(f"  False Positives: {cm_test[0, 1]}")
print(f"  False Negatives: {cm_test[1, 0]}")
print(f"  True Positives: {cm_test[1, 1]}")

# Classification Report
print("\n7.4 Classification Report (Testing Set):")
print(classification_report(y_test, y_pred_test, target_names=['No Purchase', 'Purchase']))

# ============================================================================
# STEP 8: FEATURE INTERPRETATION
# ============================================================================
print("\n" + "=" * 80)
print("STEP 8: FEATURE INTERPRETATION & INSIGHTS")
print("=" * 80)

print("\n8.1 Feature Influence Analysis:")
print("\nCoefficient Interpretation:")
age_coeff = lr_model.coef_[0][0]
salary_coeff = lr_model.coef_[0][1]

print(f"\n  Age Coefficient: {age_coeff:.6f}")
if age_coeff > 0:
    print(f"    → Each additional year of age INCREASES the likelihood of purchase")
    print(f"    → Older customers are MORE likely to purchase")
else:
    print(f"    → Each additional year of age DECREASES the likelihood of purchase")
    print(f"    → Younger customers are MORE likely to purchase")

print(f"\n  EstimatedSalary Coefficient: {salary_coeff:.6f}")
if salary_coeff > 0:
    print(f"    → Each additional dollar in salary INCREASES the likelihood of purchase")
    print(f"    → Customers with higher salary are MORE likely to purchase")
else:
    print(f"    → Each additional dollar in salary DECREASES the likelihood of purchase")
    print(f"    → Customers with lower salary are MORE likely to purchase")

print("\n8.2 Feature Importance Ranking:")
importance_abs = np.abs(lr_model.coef_[0])
most_important = np.argmax(importance_abs)
feature_names = ['Age', 'EstimatedSalary']
print(f"\n  Most Influential Feature: {feature_names[most_important]}")
print(f"    Relative importance: {importance_abs[most_important] / importance_abs.sum() * 100:.2f}%")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\n" + "=" * 80)
print("STEP 9: CREATING VISUALIZATIONS")
print("=" * 80)

# Create a figure with multiple subplots
fig = plt.figure(figsize=(16, 12))

# 1. Feature Distribution by Purchase Status
ax1 = plt.subplot(2, 3, 1)
df[df['Purchased'] == 0]['Age'].hist(bins=20, alpha=0.6, label='No Purchase', color='blue')
df[df['Purchased'] == 1]['Age'].hist(bins=20, alpha=0.6, label='Purchase', color='orange')
ax1.set_xlabel('Age')
ax1.set_ylabel('Frequency')
ax1.set_title('Age Distribution by Purchase Status')
ax1.legend()

ax2 = plt.subplot(2, 3, 2)
df[df['Purchased'] == 0]['EstimatedSalary'].hist(bins=20, alpha=0.6, label='No Purchase', color='blue')
df[df['Purchased'] == 1]['EstimatedSalary'].hist(bins=20, alpha=0.6, label='Purchase', color='orange')
ax2.set_xlabel('Estimated Salary')
ax2.set_ylabel('Frequency')
ax2.set_title('Salary Distribution by Purchase Status')
ax2.legend()

# 2. Scatter plot of Age vs Salary colored by Purchase
ax3 = plt.subplot(2, 3, 3)
scatter = ax3.scatter(df[df['Purchased'] == 0]['Age'], 
                     df[df['Purchased'] == 0]['EstimatedSalary'],
                     alpha=0.5, c='blue', label='No Purchase', s=50)
scatter = ax3.scatter(df[df['Purchased'] == 1]['Age'], 
                     df[df['Purchased'] == 1]['EstimatedSalary'],
                     alpha=0.5, c='orange', label='Purchase', s=50)
ax3.set_xlabel('Age')
ax3.set_ylabel('Estimated Salary')
ax3.set_title('Age vs Salary - Purchase Distribution')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 3. Confusion Matrix Heatmap
ax4 = plt.subplot(2, 3, 4)
sns.heatmap(cm_test, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax4,
            xticklabels=['No Purchase', 'Purchase'],
            yticklabels=['No Purchase', 'Purchase'])
ax4.set_ylabel('Actual')
ax4.set_xlabel('Predicted')
ax4.set_title('Confusion Matrix (Test Set)')

# 4. Feature Importance
ax5 = plt.subplot(2, 3, 5)
features = ['Age', 'EstimatedSalary']
importance = np.abs(lr_model.coef_[0])
colors = ['#1f77b4', '#ff7f0e']
bars = ax5.bar(features, importance, color=colors)
ax5.set_ylabel('Absolute Coefficient Value')
ax5.set_title('Feature Importance in Model')
ax5.grid(True, alpha=0.3, axis='y')
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.6f}', ha='center', va='bottom')

# 5. Model Accuracy Comparison
ax6 = plt.subplot(2, 3, 6)
accuracies = [train_accuracy, test_accuracy]
labels = ['Training', 'Testing']
colors = ['#2ca02c', '#d62728']
bars = ax6.bar(labels, accuracies, color=colors)
ax6.set_ylabel('Accuracy Score')
ax6.set_ylim([0, 1])
ax6.set_title('Model Accuracy Comparison')
ax6.grid(True, alpha=0.3, axis='y')
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2%}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('customer_purchase_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved as 'customer_purchase_analysis.png'")
plt.show()

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("\n" + "=" * 80)
print("FINAL SUMMARY REPORT")
print("=" * 80)

print(f"""
DATASET SUMMARY:
  • Total Records: {len(df)}
  • Features Used: Age, EstimatedSalary
  • Target Variable: Purchased (0: No, 1: Yes)
  • Purchase Rate: {(y.sum()/len(y)*100):.2f}%

DATA SPLIT:
  • Training Set: {len(X_train)} records (80%)
  • Testing Set: {len(X_test)} records (20%)

MODEL PERFORMANCE:
  • Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)
  • Testing Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)

CONFUSION MATRIX (TEST SET):
  • True Negatives: {cm_test[0, 0]}  (Correctly predicted no purchase)
  • False Positives: {cm_test[0, 1]} (Incorrectly predicted purchase)
  • False Negatives: {cm_test[1, 0]} (Missed actual purchases)
  • True Positives: {cm_test[1, 1]}  (Correctly predicted purchase)

FEATURE IMPORTANCE:
  • Most Important: {feature_names[most_important]}
  • Age Coefficient: {age_coeff:.6f}
  • Salary Coefficient: {salary_coeff:.6f}

KEY INSIGHTS:
  • Age appears to be {'MORE' if importance_abs[0] > importance_abs[1] else 'LESS'} influential than Salary
  • Customers with {'HIGHER' if salary_coeff > 0 else 'LOWER'} salaries are more likely to purchase
  • Customers who are {'OLDER' if age_coeff > 0 else 'YOUNGER'} are more likely to purchase
""")

print("=" * 80)
print("✓ Analysis Complete!")
print("=" * 80)
