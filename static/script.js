document.getElementById('forecasting-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('predict-btn');
    const resultDisplay = document.getElementById('result-display');

    submitBtn.innerText = "Analyzing & Predicting...";
    submitBtn.disabled = true;

    const formData = {
        category: document.getElementById('category').value,
        region: document.getElementById('region').value,
        inventory_level: document.getElementById('inventory_level').value,
        units_sold: document.getElementById('units_sold').value,
        units_ordered: document.getElementById('units_ordered').value,
        price: document.getElementById('price').value,
        discount: document.getElementById('discount').value,
        competitor_pricing: document.getElementById('competitor_pricing').value,
        weather_condition: document.getElementById('weather_condition').value,
        seasonality: document.getElementById('seasonality').value,
        promotion: document.getElementById('promotion').value,
        epidemic: document.getElementById('epidemic').value
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.status === 'success') {
            resultDisplay.innerHTML = `
                <div class="result-container">
                    <p style="color: var(--text-muted); font-weight: 600;">Predicted Units Demand</p>
                    <div class="result-metric">${data.predicted_demand}</div>
                    <span class="badge" style="background-color: ${data.status_color}; color: #000;">
                        ${data.demand_level} Demand
                    </span>
                    <hr style="border: 0.5px solid var(--border); margin: 20px 0;">
                    <p style="font-size: 12px; color: var(--text-muted);">Model Accuracy: <strong>${data.accuracy}</strong></p>
                </div>
            `;
        } else {
            resultDisplay.innerHTML = `<p style="color: #e74c3c;">Error: ${data.message}</p>`;
        }
    } catch (err) {
        resultDisplay.innerHTML = `<p style="color: #e74c3c;">Connection Error. Make sure Flask server is running.</p>`;
    } finally {
        submitBtn.innerText = "Generate Demand Forecast";
        submitBtn.disabled = false;
    }
});