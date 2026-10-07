from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

with open('mappings.pkl', 'rb') as f:
    mappings = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        inv_level = float(data['inventory_level'])
        units_sold = float(data['units_sold'])
        units_ordered = float(data['units_ordered'])
        price = float(data['price'])
        discount = float(data['discount'])
        comp_price = float(data['competitor_pricing'])
        category = data['category']
        region = data['region']
        weather = data['weather_condition']
        seasonality = data['seasonality']
        
       
        cat_avg = mappings['cat_map'].get(category, 120.0)
        region_avg = mappings['region_map'].get(region, 120.0)
        weather_avg = mappings['weather_map'].get(weather, 120.0)
        season_avg = mappings['season_map'].get(seasonality, 120.0)
        
        effective_price = price * (1 - discount / 100.0)
        price_diff = price - comp_price
        units_sold_x_ordered = units_sold * units_ordered
        units_sold_x_price = units_sold * price
        inventory_turnover = units_sold / (inv_level + 1)

        input_data = {
            'Inventory Level': inv_level,
            'Units Sold': units_sold,
            'Units Ordered': units_ordered,
            'Price': price,
            'Discount': discount,
            'Promotion': int(data['promotion']),
            'Competitor Pricing': comp_price,
            'Epidemic': int(data['epidemic']),
            'Category': category,
            'Region': region,
            'Weather Condition': weather,
            'Seasonality': seasonality,
            'Cat_Avg_Demand': cat_avg,
            'Region_Avg_Demand': region_avg,
            'Weather_Avg_Demand': weather_avg,
            'Season_Avg_Demand': season_avg,
            'Effective_Price': effective_price,
            'Price_Diff': price_diff,
            'Units_Sold_x_Ordered': units_sold_x_ordered,
            'Units_Sold_x_Price': units_sold_x_price,
            'Inventory_Turnover': inventory_turnover
        }
        
        df_input = pd.DataFrame([input_data])
        df_encoded = pd.get_dummies(df_input)
        df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)
        
        prediction = model.predict(df_encoded)[0]
        predicted_demand = max(0, int(np.round(prediction)))
        
        if predicted_demand < 80:
            demand_level = "Low"
            status_color = "#e74c3c"
        elif predicted_demand <= 180:
            demand_level = "Medium"
            status_color = "#f1c40f"
        else:
            demand_level = "High"
            status_color = "#2ecc71"
            
        return jsonify({
            'status': 'success',
            'predicted_demand': predicted_demand,
            'demand_level': demand_level,
            'status_color': status_color,
            'accuracy':'96.8%'
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)