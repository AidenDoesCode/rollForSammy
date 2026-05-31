from flask import Flask, render_template, jsonify, request
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

# State tracker for excluded ingredients
excluded_items = []

app = Flask(__name__)

def getOption(maxNum, givenList):
    # Safe guard if user picks 0 ingredients or everything is excluded
    if maxNum == 0 or not givenList:
        return []
    
    choices = []
    for i in range(maxNum):
        choices.append(random.choice(givenList))
    return choices

@app.route('/')
def index():
    return render_template('index.html')

# --- Exclusions Form Handler ---
@app.route('/submit-exclusions', methods=['POST'])
def handle_exclusions():
    global excluded_items
    excluded_items = request.form.getlist('exclude')
    return f"Selection saved! Excluded {len(excluded_items)} specific items."

# --- Specific Choice Forms (Exact Amount) ---
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

# --- Random Max Form Submits (Upper Limit Range) ---
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

# --- Generator Logic ---
@app.route('/run-function', methods=['POST'])
def run_function():
    base = ["White", "Wheat", "Lettuce Wrap"]
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
    
    # --- Filter Lists using User Veto Choices ---
    active_meat = [m for m in meat if m not in excluded_items]
    active_cheese = [c for c in cheese if c not in excluded_items]
    active_toppings = [t for t in toppings if t not in excluded_items]
    active_sauces = [s for s in sauces if s not in excluded_items]

    # Process counts based on choice types
    numMeat = settings["meat"] if is_exact_choice["meat"] else random.randint(0, settings["meat"])
    numCheese = settings["cheese"] if is_exact_choice["cheese"] else random.randint(0, settings["cheese"])
    numTopping = settings["topping"] if is_exact_choice["topping"] else random.randint(0, settings["topping"])
    numSauce = settings["sauce"] if is_exact_choice["sauce"] else random.randint(0, settings["sauce"])

    return jsonify({
        "Bread/Base": getOption(1, base),
        "Meat": getOption(numMeat, active_meat),
        "Cheese": getOption(numCheese, active_cheese),
        "Toppings": getOption(numTopping, active_toppings),
        "Sauces": getOption(numSauce, active_sauces)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    serve(app, host="0.0.0.0", port=port)