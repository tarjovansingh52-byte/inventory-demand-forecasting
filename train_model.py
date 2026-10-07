import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score


print("Loading dataset...")
df = pd.read_excel('cleaned_demand_forecasting (1).xlsx')


cat_map = df.groupby('Category')['Demand'].mean().to_dict()
region_map = df.groupby('Region')['Demand'].mean().to_dict()
weather_map = df.groupby('Weather Condition')['Demand'].mean().to_dict()
season_map = df.groupby('Seasonality')['Demand'].mean().to_dict()

df['Cat_Avg_Demand'] = df['Category'].map(cat_map)
df['Region_Avg_Demand'] = df['Region'].map(region_map)
df['Weather_Avg_Demand'] = df['Weather Condition'].map(weather_map)
df['Season_Avg_Demand'] = df['Seasonality'].map(season_map)


df['Effective_Price'] = df['Price'] * (1 - df['Discount'] / 100.0)
df['Price_Diff'] = df['Price'] - df['Competitor Pricing']
df['Units_Sold_x_Ordered'] = df['Units Sold'] * df['Units Ordered']
df['Units_Sold_x_Price'] = df['Units Sold'] * df['Price']
df['Inventory_Turnover'] = df['Units Sold'] / (df['Inventory Level'] + 1)


mappings = {
    'cat_map': cat_map,
    'region_map': region_map,
    'weather_map': weather_map,
    'season_map': season_map
}

with open('mappings.pkl', 'wb') as f:
    pickle.dump(mappings, f)


features = [
    'Inventory Level', 'Units Sold', 'Units Ordered', 'Price', 'Discount', 
    'Promotion', 'Competitor Pricing', 'Epidemic', 'Category', 'Region', 
    'Weather Condition', 'Seasonality', 'Cat_Avg_Demand', 'Region_Avg_Demand',
    'Weather_Avg_Demand', 'Season_Avg_Demand', 'Effective_Price', 'Price_Diff',
    'Units_Sold_x_Ordered', 'Units_Sold_x_Price', 'Inventory_Turnover'
]

X = df[features]
y = df['Demand']


X_encoded = pd.get_dummies(X, drop_first=True)

model_columns = list(X_encoded.columns)
with open('columns.pkl', 'wb') as f:
    pickle.dump(model_columns, f)


X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)


print("Training High Performance Model...")
model = ExtraTreesRegressor(
    n_estimators=300, 
    max_depth=None, 
    min_samples_split=2, 
    random_state=42, 
    n_jobs=-1
)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred) * 100

print("\n=========================================")
print(f"🎯 Final Model Accuracy (R² Score): {accuracy:.2f}%")
print("=========================================\n")


with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Saved model.pkl, columns.pkl, and mappings.pkl successfully!")