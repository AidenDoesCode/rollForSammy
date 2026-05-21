#05/20/2026
#Program Name: rollForSammy



import random

#function to randomly get the choices
def getOption(maxNum, givenList):
    choices = []
    for i in range(maxNum):
        choices.append(random.choice(givenList)) #get random item from the given list
    return choices #return random value of listvalue of list

def main():
    #create and intitialize lists for different componenets of the sandwich
    base = ["White", "Wheat", "Lettuce Wrap"]
    meat = ["Turkey", "Ham", "SalamiCapicola", "Chicken", "Beef",
            "ChickenSalad", "Pork", "Sausage", "Pepperorni", "Bacon", "None"]
    cheese = ["Provolone", "Mozzarella", "Cheddar", "Bleu Cheese", "None"]
    toppings = ["Lettuce", "Tomato", "Onion", "Pickles", "Olives",
                "Banana Peppers", "Gardinara Peppers", "Cucumbers", "Spinach",
                "Avocado", "Garlic Butter", "Egg", "Walnuts", "Cranberries",
                "Italian Seasoning", "Grated Parmesan", "Salt", "Pepper", "None"]
    sauces = ["Mayo", "Mustard", "Honey Mustard", "Ranch", "Chipotle Ranch",
          "Buffalo Sauce", "BBQ", "Caesar", "V&O", "Italian Vin",
          "Spicy Mustard", "Balsamic", "Pepper Oil", "Marinara", "Au Jus", "None"]
    
    #hard code max number of options for each component of the sandwich
    maxBase = 1
    maxMeat = 3
    maxCheese = 2
    maxToppings = 6
    maxSauces = 2

    #generate random number of each component to add to the sandwich
    numMeat = random.randint(0, maxMeat)
    numCheese = random.randint(0, maxCheese)
    numTopping = random.randint(0, maxToppings)
    numSauce = random.randint(0, maxSauces)

    

    #start building the sandwich
    sandwich = [] #list to hold the sandwich components
    
    #add random base to the sandwich
    baseChoice = getOption(maxBase, base)
    meatChoice = getOption(numMeat, meat)
    cheeseChoice = getOption(numCheese, cheese)
    toppingChoice = getOption(numTopping, toppings)
    sauceChoice = getOption(numSauce, sauces)

    #add sandwich list items
    sandwich.append(baseChoice)
    sandwich.append(meatChoice)
    sandwich.append(cheeseChoice)
    sandwich.append(toppingChoice)
    sandwich.append(sauceChoice)

    print (sandwich)
if __name__ == '__main__':
    main()