from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import joblib
 
# Create dummy dataset
X, y = make_classification(
    n_samples=100,
    n_features=3,
    n_informative=3,
    n_redundant=0,
    random_state=42
)
 
# Train model
model = RandomForestClassifier()
model.fit(X, y)
 
# Save model
joblib.dump(model, 'model.pkl')
print('model.pkl created successfully')
