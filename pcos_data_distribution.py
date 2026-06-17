import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("PCOS_data.csv")

# Clean columns but don't drop all rows with any missing values blindly
data = data.drop(columns=[col for col in data.columns if "Unnamed" in col or "Patient" in col], errors='ignore')

# Optional: Fill missing values (alternative to dropna)
data = data.fillna(data.mean(numeric_only=True))

# Display shape after cleaning
print(f"Total records after cleaning: {data.shape[0]}")

# Show PCOS class distribution
print("\n🔍 Class distribution (PCOS vs Non-PCOS):")
print(data['PCOS (Y/N)'].value_counts())
print("\n(0 = Non-PCOS, 1 = PCOS)")

# Train-test split
X = data.drop('PCOS (Y/N)', axis=1)
y = data['PCOS (Y/N)']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Print split info
print(f"\nTraining samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

