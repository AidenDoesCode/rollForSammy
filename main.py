from flask import Flask, render_template, jsonify  # <-- Make sure jsonify is here!
from pprint import pprint
from waitress import serve
import random
import os

app = Flask(__name__)

def getOption(maxNum, givenList):
    choices = []
    for i in range(maxNum):
        choices.append(random.choice(givenList))
    return choices

@app.route('/')
def index():
    return render_template('index.html')

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
    
    numMeat = random.randint(0, 3)
    numCheese = random.randint(0, 2)
    numTopping = random.randint(0, 6)
    numSauce = random.randint(0, 2)

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