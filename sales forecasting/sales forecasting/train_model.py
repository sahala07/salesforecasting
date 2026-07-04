import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

import pickle

#load dataset
df=pd.read_csv("sales.csv")

print(df.head())
print("\n Dataset Information")
print(df.info())
print("\nStatistical Summary")
print(df.describe())
#data preprocessing
print(df.isnull().sum())
df.dropna(inplace=True)
df.fillna(df.mean(numeric_only=True),inplace=True)
print("\nDuplicate Rows:",df.duplicated().sum())
df.drop_duplicates(inplace=True)
df["date"] = pd.to_datetime(df["date"],dayfirst=True)
df["Year"] = df["date"].dt.year
df["Month"] = df["date"].dt.month
df["Day"] = df["date"].dt.day
df.drop(columns=["date"])
df.drop("date", axis=1, inplace=True)
print("\n Processed Data")
print(df.head())

#graph plot
#sales distribution
plt.figure(figsize=(6,4))
plt.hist(df["sales"],bins=20)
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.show()
#trend
plt.figure(figsize=(6,4))
plt.plot(df["sales"])
plt.title("sales Trend")
plt.show()
#box plot
plt.figure(figsize=(4,5))
plt.boxplot(df["sales"])
plt.title("sales")
plt.show()

#input
X = df.drop("sales", axis=1)
y = df["sales"]

#spliting data to train and test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



#ALGORITHM
#LINEAR REGRESSION
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

print("Linear Regression Results")
print("--------------------------")
lr_r2=r2_score(y_test, lr_pred)
lr_mae= mean_absolute_error(y_test, lr_pred)
lr_rmse= np.sqrt(mean_squared_error(y_test, lr_pred))

#KNN Regression
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
knn_pred= knn.predict(X_test_scaled)

print("KNN Results")
print("--------------------")

knn_r2= r2_score(y_test, knn_pred)
knn_mae= mean_absolute_error(y_test,knn_pred)
knn_rmse= np.sqrt(mean_squared_error(y_test,knn_pred))

# Randon Forest
rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)

print("Random Forest Results")
print("----------------------")

rf_r2= r2_score(y_test,rf_pred)
rf_mae= mean_absolute_error(y_test,rf_pred)
rf_rmse= np.sqrt(mean_squared_error(y_test,rf_pred))

#result
results = pd.DataFrame({
    "Model": ["Linear Regression", "KNN", "Random Forest"],
    "R2 Score": [lr_r2, knn_r2, rf_r2],
    "MAE": [lr_mae, knn_mae, rf_mae],
    "RMSE": [lr_rmse, knn_rmse, rf_rmse]
})
#model comparison

print("\n-----------------------")
print("MODEL COMPARISON")
print("----------------------")

print(results)

#comparison graph

models = ["Linear Regression", "KNN", "Random Forest"]
scores = [lr_r2, knn_r2, rf_r2]
plt.figure(figsize=(8,5))
plt.bar(models, scores)

plt.title("Model Comparison (R² Score)")
plt.xlabel("Models")
plt.ylabel("R² Score")
plt.ylim(0, 1)

for i, score in enumerate(scores):
    plt.text(i, score + 0.02, f"{score:.2f}", ha='center')

plt.show()

#best model
scores = {
    "Linear Regression": lr_r2,
    "KNN": knn_r2,
    "Random Forest": rf_r2
}
best_model = max(scores, key=scores.get)
print("\nBest Model:", best_model)

if best_model == "Linear Regression":
    pickle.dump(lr, open("model.pkl", "wb"))

elif best_model == "KNN":
    pickle.dump(knn, open("model.pkl", "wb"))
    pickle.dump(scaler, open("scaler.pkl", "wb"))

else:
    pickle.dump(rf, open("model.pkl", "wb"))

print("Best model saved successfully!")