from flask import Flask, render_template, jsonify, request
from pprint import pprint
from waitress import serve
import random
import os

defaultSettings = True
maxMeat = 3
maxCheese = 2
maxTopping = 6
maxSauce = 2


app = Flask(__name__)

def getOption(maxNum, givenList):
    choices = []
    for i in range(maxNum):
        choices.append(random.choice(givenList))
    return choices

@app.route('/')
def index():
    return render_template('index.html')

#Gets the data from the froms from the frontend if the form is submitted
@app.route('/submit', methods=['POST'])
def handle_submit():

    global defaultSettings, maxMeat, maxCheese, maxTopping, maxSauce

    # Grab whichever value was sent by the submitted form
    max_meat_str = request.form.get('maxMeat')
    max_cheese_str = request.form.get('maxCheese')
    max_topping_str = request.form.get('maxTopping')
    max_sauce_str = request.form.get('maxSauce')
    
    try:
        # Check and update ONLY the item that was actually submitted
        if max_meat_str is not None:
            maxMeat = int(max_meat_str)
            defaultSettings = False
            print(f"User chose max meat option: {maxMeat}")
            return f"Selection saved! Max Meats: {maxMeat}"

        elif max_cheese_str is not None:
            maxCheese = int(max_cheese_str)
            defaultSettings = False
            print(f"User chose max cheese option: {maxCheese}")
            return f"Selection saved! Max Cheese: {maxCheese}"

        elif max_topping_str is not None:
            maxTopping = int(max_topping_str)
            defaultSettings = False
            print(f"User chose max toppings option: {maxTopping}")
            return f"Selection saved! Max Toppings: {maxTopping}"

        elif max_sauce_str is not None:
            maxSauce = int(max_sauce_str)
            defaultSettings = False
            print(f"User chose max sauce option: {maxSauce}")
            return f"Selection saved! Max Sauce: {maxSauce}"

    except ValueError:
        return "Invalid selection.", 400

    return "No valid selection made.", 400

@app.route('/run-function', methods=['POST'])
def run_function():
    base = ["White", "Wheat", "Lettuce Wrap"]
    meat = ["Turkey", "Ham", "Salami Capicola", "Chicken", "Beef",
            "Chicken Salad", "Pork", "Sausage", "Pepperoni", "Bacon", "None"]
    cheese = ["Provolone", "Mozzarella", "Cheddar", "Bleu Cheese", "None"]
    toppings = ["Lettuce", "Tomato", "Onion", "Pickles", "Olives",
                "Banana Peppers", "Gardinara Peppers", "Cucumbers", "Spinach",
                "Avocado", "Garlic Butter", "Egg", "Walnuts", "Cranberries",
                "Italian Seasoning", "Grated Parmesan", "Salt", "Pepper", "None"]
    sauces = ["Mayo", "Mustard", "Honey Mustard", "Ranch", "Chipotle Ranch",
              "Buffalo Sauce", "BBQ", "Caesar", "V&O", "Italian Vin",
              "Spicy Mustard", "Balsamic", "Pepper Oil", "Marinara", "Au Jus", "None"]
    
    #default settings activated on website boot or no forms submitted
    if defaultSettings:
        numMeat = random.randint(0, 3)
        numCheese = random.randint(0, 2)
        numTopping = random.randint(0, 6)
        numSauce = random.randint(0, 2)
    #At least one max option form submitted
    else:
        numMeat = random.randint(0, maxMeat)
        numCheese = random.randint(0, maxCheese)
        numTopping = random.randint(0, maxTopping)
        numSauce = random.randint(0, maxSauce)

    # This creates the clean JSON data package the Javascript is waiting for
    return jsonify({
        "Bread/Base": getOption(1, base),
        "Meat": getOption(numMeat, meat),
        "Cheese": getOption(numCheese, cheese),
        "Toppings": getOption(numTopping, toppings),
        "Sauces": getOption(numSauce, sauces)
    })

if __name__ == "__main__":
       port = int(os.environ.get("PORT", 8000))
       serve(app, host="0.0.0.0", port=port)