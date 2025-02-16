# Here we continue after the suppliers have given us quotes
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import json

# Train AI Model for Predicting Customer Acceptance
# This model predicts whether a customer will accept a given quote based on past data.
customer_data = pd.DataFrame([
    {"price": 4.5, "delivery_time": 6, "reliability": 8, "accepted": 1},
    {"price": 4.2, "delivery_time": 8, "reliability": 7, "accepted": 0},
    {"price": 4.8, "delivery_time": 5, "reliability": 9, "accepted": 1},
    {"price": 4.1, "delivery_time": 7, "reliability": 6, "accepted": 0},
    {"price": 4.6, "delivery_time": 6, "reliability": 9, "accepted": 1},
    {"price": 4.3, "delivery_time": 9, "reliability": 7, "accepted": 0},
])

X_customer = customer_data.drop(columns=["accepted"])
y_customer = customer_data["accepted"]

X_train, X_test, y_train, y_test = train_test_split(X_customer, y_customer, test_size=0.2, random_state=42)

customer_model = RandomForestClassifier(n_estimators=100, random_state=42)
customer_model.fit(X_train, y_train)


# Contains supplier details such as pricing, delivery time, reliability, and cost.
supplier_data = pd.DataFrame([
    {"supplier": "Supplier A", "price": 4.5, "delivery_time": 6, "reliability": 8, "cost": 3.0, "product_type": "shirt"},
    {"supplier": "Supplier B", "price": 4.2, "delivery_time": 8, "reliability": 7, "cost": 2.8, "product_type": "shirt"},
    {"supplier": "Supplier C", "price": 4.8, "delivery_time": 5, "reliability": 9, "cost": 3.2, "product_type": "shoes"},
    {"supplier": "Supplier D", "price": 4.1, "delivery_time": 7, "reliability": 6, "cost": 2.9, "product_type": "shirt"},
    {"supplier": "Supplier E", "price": 4.6, "delivery_time": 6, "reliability": 9, "cost": 3.1, "product_type": "shoes"},
    {"supplier": "Supplier F", "price": 4.3, "delivery_time": 9, "reliability": 7, "cost": 3.0, "product_type": "shirt"},
])

# Calculate profit margin for each supplier
supplier_data['profit_margin'] = supplier_data['price'] - supplier_data['cost']

# Define customer requirements (Dummy data)
customer_preferences = {
    "budget": 4.5,
    "required_delivery_time": 6,
    "required_reliability": 8,
    "product_type": "shirt",
    "quantity": 10
}

# Function to calculate how closely a supplier quote matches customer needs
def calculate_closeness_score(supplier_row, customer_prefs):
    price_diff = abs(supplier_row['price'] - customer_prefs['budget'])
    delivery_diff = abs(supplier_row['delivery_time'] - customer_prefs['required_delivery_time'])
    reliability_diff = abs(supplier_row['reliability'] - customer_prefs['required_reliability'])
    product_match = 1 if supplier_row['product_type'] == customer_prefs['product_type'] else 10
    return price_diff + delivery_diff + reliability_diff + product_match

#Predict Customer Acceptance Probability
supplier_data["acceptance_probability"] = customer_model.predict_proba(supplier_data[["price", "delivery_time", "reliability"]])[:, 1]

# Train AI Model for Predicting Profit Margins
X_margin = supplier_data.drop(columns=["profit_margin", "supplier", "product_type", "acceptance_probability"])
y_margin = supplier_data["profit_margin"]

X_train_margin, X_test_margin, y_train_margin, y_test_margin = train_test_split(X_margin, y_margin, test_size=0.2, random_state=42)

margin_model = RandomForestRegressor(n_estimators=100, random_state=42)
margin_model.fit(X_train_margin, y_train_margin)

# Predict profit margins for suppliers
supplier_data['predicted_margin'] = margin_model.predict(supplier_data[["price", "delivery_time", "reliability", "cost"]])
predicted_margin=supplier_data['predicted_margin']
# Step 6: Rank Suppliers
supplier_data['closeness_score'] = supplier_data.apply(lambda row: calculate_closeness_score(row, customer_preferences), axis=1)

# Step 7: Final Score Calculation (Higher score = better choice)
supplier_data['final_score'] = supplier_data['acceptance_probability'] * (1 / supplier_data['closeness_score']) * supplier_data['predicted_margin']

# Select the best supplier
best_supplier = supplier_data.sort_values(by="final_score", ascending=False).iloc[0]

# Step 8: Generate Final Quote for the Customer
def generate_final_quote(supplier_name, price_per_unit, quantity, predicted_margin):
    total_price = price_per_unit * quantity
    
    total_profit = predicted_margin * quantity
    quote= f"""
===========================================
FINAL QUOTE FOR CUSTOMER
===========================================
Selected Supplier: {supplier_name}
Price per Unit: ${price_per_unit}
Quantity: {quantity}
Total Price: ${total_price}
Key Benefits:
- AI-optimized supplier selection
- Competitive pricing
- Reliable supplier
Offer Validity: 30 Days
Contact us for any queries.
"""
    return quote,total_profit

# Customer Feedback Collection
def collect_feedback():
    while True:
        feedback = input("\nDid the customer accept the quote? (yes/no): ").strip().lower()
        if feedback == "yes":
            print("Quote accepted! Updating the system for future recommendations.")
            return True
        elif feedback == "no":
            print("Quote rejected! We will improve our recommendations.")
            return False
        else:
            print("Please choose one (yes/no)")

# Step 10: Save Feedback for AI Model Improvement
def save_feedback_data(supplier_name, price, delivery_time, reliability, accepted):
    new_entry = {
        "price": float(price),
        "delivery_time": int(delivery_time),
        "reliability": int(reliability),
        "accepted": int(accepted)
    }
    try:
        with open("supplier_feedback.json", "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    with open("supplier_feedback.json", "w") as file:
        json.dump(data, file, indent=4)

# Step 11: Execute Full Workflow
def main():
    print("\n### SUPPLIER QUOTATION ANALYSIS ###")
    for _, q in supplier_data.iterrows():
        print(f"{q['supplier']} - Price: ${q['price']}, Delivery: {q['delivery_time']} days, Reliability: {q['reliability']}/10")

    print("\n### AI-Powered Supplier Selection ###")
    for _, row in supplier_data.iterrows():
        print(f"{row['supplier']} - Predicted Acceptance Probability: {round(row['acceptance_probability'] * 100, 2)}%")

    print(f"\n✅ Best Supplier Selected: {best_supplier['supplier']}")

    # Generate and display final quote
    final_quote,total_profit = generate_final_quote(best_supplier["supplier"], best_supplier["price"], customer_preferences["quantity"],best_supplier["predicted_margin"])
    print(final_quote)
    print(f"Profit: {total_profit}")

    # Collect customer feedback and update AI system
    feedback_accepted = collect_feedback()
    save_feedback_data(best_supplier["supplier"], best_supplier["price"], best_supplier["delivery_time"], best_supplier["reliability"], int(feedback_accepted))

# Run the script
main()
