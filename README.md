# inventory-demand-forecasting
Enterprise Machine Learning Demand Prediction Platform for forecasting product demand based on inventory, pricing, and seasonal parameters.
# Project Overview
This project is a Machine Learning–based demand forecasting system that predicts product demand levels (Low, Medium, High) based on multiple business and environmental factors. It helps businesses optimize inventory management, reduce overstock/understock risks, and improve decision‑making.
The trained ML model is stored in model.pkl, which contains the serialized version of the best performing algorithm. This file allows the system to make predictions instantly without retraining the model each time.
# Key Features
1. Demand Prediction: Forecasts demand levels (Low, Medium, High) using historical and contextual data.

2. Multiple Input Factors: Considers variables such as inventory levels, units sold, units ordered, price, discount, competitor pricing, category, region, weather, seasonality, promotions, and epidemic conditions.

3. Model Persistence (model.pkl):

* Stores the trained ML model for reuse.

* Enables fast predictions in production environments.

* Ensures consistency between training and deployment.

4. Web Integration: Flask application with a user‑friendly form for input and real‑time demand forecasting.

5. Visualization: Displays predicted demand units, demand category, and model accuracy with clear UI elements.
# Technologies Used
1. Programming Language: Python

2. Libraries:

* pandas – data preprocessing

* numpy – numerical operations

* scikit-learn – ML algorithms and evaluation

* Flask – web application framework

* render_template, request, jsonify – Flask utilities for routing, handling input, and returning JSON responses

* pickle – model serialization (model.pkl)

3. Model Storage: Pickle (model.pkl)

4. Version Control: Git & GitHub
# Workflow
1. Data Collection → Gather inventory, sales, and contextual data.

2. Preprocessing → Clean and prepare dataset for training.

3. Model Training → Train ML models (Decision Tree, Logistic Regression, KNN, ExtraTreesRegressor).

4. Evaluation → Compare accuracy and select best model.

5. Model Saving → Serialize trained model into model.pkl.

6. Web Deployment → Flask app allows users to input values and get demand forecasts.

7. Prediction Output → Displays demand units, demand level (Low/Medium/High), and accuracy.
# Future Scope
1. Add advanced ML models (Random Forest, XGBoost, Neural Networks).

2. Deploy on cloud platforms (AWS, Azure, IBM Cloud) for scalability.

3. Integrate with ERP systems for real‑time inventory updates.

4. Expand dataset with more features (customer demographics, regional trends).
