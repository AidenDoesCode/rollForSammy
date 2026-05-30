from flask import Flask, render_template, jsonify, request
from pprint import pprint
from waitress import serve
import random
import os

# --- Tracking State ---
is_exact_choice = {
    "meat": False,
    "cheese": False,
    "topping": False,
    "sauce": False
}

settings = {
    "meat": 3,      
    "cheese": 2,    
    "topping": 6,   
    "sauce": 2      
}

app = Flask(__name__)

def getOption(maxNum, givenList):
    # If the user or randomizer generated 0 choices, return an empty list immediately
    if maxNum == 0:
        return []
    
    choices = []
    for i in range(maxNum):
        choices.append(random.choice(givenList))
    return choices

@app.route('/')
def index():
    return render_template('index.html')


# Specific Choice Forms (Exact Amount Chosen)
@app.route('/submit-choice', methods=['POST'])
def handle_submit_choice():
    global is_exact_choice, settings

    max_meat_str = request.form.get('numMeat')
    max_cheese_str = request.form.get('numCheese')
    max_topping_str = request.form.get('numTopping')
    max_sauce_str = request.form.get('numSauce')

    try:
        if max_meat_str is not None:
            settings["meat"] = int(max_meat_str)
            is_exact_choice["meat"] = True
            return f"Selection saved! Exact Meat/s: {settings['meat']}"

        elif max_cheese_str is not None:
            settings["cheese"] = int(max_cheese_str)
            is_exact_choice["cheese"] = True
            return f"Selection saved! Exact Cheese: {settings['cheese']}"

        elif max_topping_str is not None:
            settings["topping"] = int(max_topping_str)
            is_exact_choice["topping"] = True
            return f"Selection saved! Exact Topping/s: {settings['topping']}"

        elif max_sauce_str is not None:
            settings["sauce"] = int(max_sauce_str)
            is_exact_choice["sauce"] = True
            return f"Selection saved! Exact Sauce/s: {settings['sauce']}"

    except ValueError:
        return "Invalid selection.", 400

    return "No valid selection made.", 400


# Random Max Form Submits (Upper limit range chosen)
@app.route('/submit-random', methods=['POST'])
def handle_submit_random():
    global is_exact_choice, settings

    max_meat_str = request.form.get('maxMeat')
    max_cheese_str = request.form.get('maxCheese')
    max_topping_str = request.form.get('maxTopping')
    max_sauce_str = request.form.get('maxSauce')
    
    try:
        if max_meat_str is not None:
            settings["meat"] = int(max_meat_str)
            is_exact_choice["meat"] = False
            return f"Selection saved! Max Meats: {settings['meat']}"

        elif max_cheese_str is not None:
            settings["cheese"] = int(max_cheese_str)
            is_exact_choice["cheese"] = False
            return f"Selection saved! Max Cheese: {settings['cheese']}"

        elif max_topping_str is not None:
            settings["topping"] = int(max_topping_str)
            is_exact_choice["topping"] = False
            return f"Selection saved! Max Toppings: {settings['topping']}"

        elif max_sauce_str is not None:
            settings["sauce"] = int(max_sauce_str)
            is_exact_choice["sauce"] = False
            return f"Selection saved! Max Sauce: {settings['sauce']}"

    except ValueError:
        return "Invalid selection.", 400

    return "No valid selection made.", 400


@app.route('/run-function', methods=['POST'])
def run_function():
    base = ["White", "Wheat", "Lettuce Wrap"]
    
    # Removed "None" string options from arrays to prevent double-empty returns
    meat = ["Turkey", "Ham", "Salami Capicola", "Chicken", "Beef",
            "Chicken Salad", "Pork", "Sausage", "Pepperoni", "Bacon"]
    cheese = ["Provolone", "Mozzarella", "Cheddar", "Bleu Cheese"]
    toppings = ["Lettuce", "Tomato", "Onion", "Pickles", "Olives",
                "Banana Peppers", "Gardinara Peppers", "Cucumbers", "Spinach",
                "Avocado", "Garlic Butter", "Egg", "Walnuts", "Cranberries",
                "Italian Seasoning", "Grated Parmesan", "Salt", "Pepper"]
    sauces = ["Mayo", "Mustard", "Honey Mustard", "Ranch", "Chipotle Ranch",
              "Buffalo Sauce", "BBQ", "Caesar", "V&O", "Italian Vin",
              "Spicy Mustard", "Balsamic", "Pepper Oil", "Marinara", "Au Jus"]
    
    # Meat logic
    if is_exact_choice["meat"]:
        numMeat = settings["meat"]
    else:
        numMeat = random.randint(0, settings["meat"])

    # Cheese logic
    if is_exact_choice["cheese"]:
        numCheese = settings["cheese"]
    else:
        numCheese = random.randint(0, settings["cheese"])

    # Topping logic
    if is_exact_choice["topping"]:
        numTopping = settings["topping"]
    else:
        numTopping = random.randint(0, settings["topping"])

    # Sauce logic
    if is_exact_choice["sauce"]:
        numSauce = settings["sauce"]
    else:
        numSauce = random.randint(0, settings["sauce"])

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