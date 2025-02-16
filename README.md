# HelloPrints_Quotation

**Requirements:**
Python 3.x
pandas
numpy
scikit-learn
install using `pip install pandas numpy scikit-learn`

**How to Run:**
-Download or clone this repository.
-Navigate to the project directory where the Python script is located.
-Run part-1 for the first part of code (chatbot+ Supplier Ranking+ RFQ standardization) using `python Part-1.py`

Example Input:
```
Bot: How may I assist you today?
1. Services
2. Products
You: product
>Bot: Do you want to print something? (yes/no)
>You: yes
>Bot: What do you want to print?
1. T-shirt
2. Brochure
3. Cup
4. Other
You: t-shirt
Bot: May I know the quantity?
You: 50
Bot: May I know the delivery time? (in days)
You: 7
Bot: May I know your budget in Euros? Do not add currency
You: 100
Bot: Can you please upload the image you want to print in HD form? (Enter file path)
You: /path/to/image.jpg
```

-Run part-2 for the second part of code using `python Part-2.py`

-The program will:
  Show supplier quotations,
  Predict customer acceptance probabilities,
  Display the selected best supplier,
  Generate a final quote for the customer,
  Ask for customer feedback (whether they accepted the quote or not),
  Save feedback to improve the AI model for future use.
  
  **Example Input**
  `Did the customer accept the quote? (yes/no): yes`

