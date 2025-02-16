# In this script we are using rule-based chatbot to gather project details and ranking best suppliers and generating a standardize RFQ to send to user

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

# 1. Chatbot for Customer Inquiry
def chatbot():
    print("Bot: How may I assist you today?")
    print("1. Services")
    print("2. Products")

    choice = input("👉 You: ").strip().lower()

    if "product" in choice:
        print("Bot: Do you want to print something? (yes/no)")
        print_choice = input("You: ").strip().lower()

        if print_choice == "yes":
            print(" Bot: What do you want to print?")
            print("1. T-shirt\n2. Brochure\n3. Cup\n4. Other")
            product = input("You: ").strip().lower()

            print("  Bot: May I know the quantity?")
            quantity = input("You: ").strip()

            print("  Bot: May I know the delivery time? (in days)")
            delivery_time = input("You: ").strip()

            print("  Bot: May I know your budget in Euros? Do not add currency")
            budget = input("You: ").strip()

            print("  Bot: Can you please upload the image you want to print in HD form? (Enter file path)")
            image_path = input("You: ").strip()

            
            try:
                with open(image_path, "rb") as img_file:
                    print("✅ Image uploaded successfully!")
                    image_uploaded = True
            except FileNotFoundError:
                print("❌ Error: File not found. Please upload a valid image.")
                image_uploaded = False

            
            return {
                'product_type': product.capitalize(),
                'quantity': int(quantity),
                'delivery_time': int(delivery_time),
                'budget':int(budget),
                'image_uploaded': image_uploaded
            }
        else:
            print("  Bot: Okay! Let me know if you need any other service.")
            return None
    elif "service" in choice:
        print("  Bot: What service do you need? Please provide details.")
        service_details = input("👉 You: ").strip()
        print(f"  Bot: Got it! You need help with: {service_details}")
        return None
    else:
        print("  Bot: I'm sorry, I didn't understand. Please try again.")
        return None

# 2. AI Model for Supplier Ranking
def rank_suppliers(customer_details):
    """
    This function ranks suppliers based on a trained Random Forest model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Dummy training data (cost, delivery time, reliability score)
    data = [
        [500, 5, 9],  # Supplier A
        [450, 7, 7],  # Supplier B
        [520, 4, 8]   # Supplier C
    ]
    labels = [1, 0, 1]  # 1: Chosen Before, 0: Not Chosen

    model.fit(data, labels)

    # Predict ranking based on customer needs
    X = np.array([
        [customer_details['budget'], customer_details['delivery_time'], customer_details['reliability']]
    ])

    supplier_scores = model.predict_proba(X)[:, 1] 
    return supplier_scores

# 3. RFQ Generation (Standardized Template)
def generate_rfq(customer_name, company_name, product_type, quantity, delivery_time):
    """Generates a standardized RFQ document"""
    rfq_template = f"""
    ============================================
                REQUEST FOR QUOTATION (RFQ)
    ============================================
    Date: {datetime.today().strftime('%Y-%m-%d')}

    Customer Details:
    --------------------------------------------
    Company Name: {company_name}
    Contact Person: {customer_name}

    Project Details:
    --------------------------------------------
      Product Type: {product_type}
    Quantity: {quantity}
    Delivery Time Required: {delivery_time} days
    

    Requirements:
    --------------------------------------------
    - All quotations must include pricing, taxes, and shipping costs.
    - Please provide estimated delivery timelines and payment terms.
    - Quote validity should be at least 30 days from the date of submission.

    Submission Details:
    --------------------------------------------
    Send your quotation to: procurement@company.com
    Deadline for Submission: {datetime.today().strftime('%Y-%m-%d')} + 1 day

    Thank you for your prompt response.

    Best Regards,  
    {customer_name}  
    {company_name}  
    """
    return rfq_template

# 4. Putting Everything Together


customer_details = chatbot()

if customer_details:
    
    customer_details['reliability'] = 8  # Preferred supplier reliability score

    supplier_scores = rank_suppliers(customer_details)

    # Rank and Filter Top Suppliers (Top 2 for example)
    sorted_supplier_indexes = np.argsort(supplier_scores)[::-1]  
    top_suppliers = sorted_supplier_indexes[:2]  # Top 2 suppliers

    # Step 5: Generate and Send RFQs to Top Suppliers
    customer_name = "Michael Heerkens"
    company_name = "Hello Print"
    product_type = customer_details['product_type']
    quantity = customer_details['quantity']
    delivery_time = customer_details['delivery_time']
   

    rfq = generate_rfq(customer_name, company_name, product_type, quantity, delivery_time)

    # Display RFQs Sent
    for supplier in top_suppliers:
        print(f"\n📩 Sending RFQ to Supplier {supplier + 1}...")
        print(rfq)
