import json
import random
import itertools
from menu_utils import *

# Function to load menu data from the JSON file
def load_menu_from_file(file_path):
    with open(file_path, 'r') as file:
        menu_data = json.load(file)
    return menu_data

# Load menu data from the provided JSON file
menu_data = load_menu_from_file('menu.json')

# Define quality scores
quality_scores = {'low': 10, 'medium': 20, 'high': 30}

# Function to select a random meal from the menu data
def select_random_meal():
    return random.choice(menu_data["meals"])

# Function to generate random quality parameters for ingredients
def generate_random_quality(ingredient):
    quality_levels = ['low', 'medium', 'high']
    return random.choice(quality_levels)

# Function to calculate the overall quality of a meal
# Define a mapping of numerical scores to quality levels
quality_level_mapping = {10: 'Low', 20: 'Medium', 30: 'High'}

# Modify the function to calculate the overall quality of a meal
def calculate_quality(meal_id, ingredient_qualities, numeric=False):
    meal = next((m for m in menu_data['meals'] if m['id'] == meal_id), None)

    if meal is None or 'ingredients' not in meal:
        print("Error: Meal not found or meal data is incomplete.")
        return None

    ingredient_scores = {}  # Dictionary to store quality scores of each ingredient
    total_score = 0
    num_ingredients = len(meal['ingredients'])

    for ingredient in meal['ingredients']:
        ingredient_name = ingredient['name']
        quality_level = ingredient_qualities.get(ingredient_name, 'high')
        score = quality_scores.get(quality_level, 0)  # Use quality_scores to map quality levels to scores
        ingredient_scores[ingredient_name] = score if numeric else quality_level_mapping.get(score, 'Unknown')  # Map score to quality level text if not numeric
        total_score += score

    overall_quality = total_score / num_ingredients if num_ingredients > 0 else 0
    
    # Adjust the output structure
    result = {
        'quality_scores': overall_quality,  # Always return numeric value for quality score
        'ingredient_quality': ingredient_scores
    }
    
    return result

# Function to calculate the total cost of a meal
def calculate_price(meal_id, ingredient_qualities):
    meal = next((m for m in menu_data['meals'] if m['id'] == meal_id), None)

    if meal is None or 'ingredients' not in meal:
        print("Error: Meal not found or meal data is incomplete.")
        return None

    total_price = 0

    for ingredient in meal['ingredients']:
        ingredient_name = ingredient['name']
        quality_level = ingredient_qualities.get(ingredient_name, 'high')

        ingredient_data = next((ing for ing in menu_data['ingredients'] if ing['name'].lower() == ingredient_name.lower()), None)
        if ingredient_data is None:
            continue

        quality_option = next((option for option in ingredient_data['options'] if option['quality'] == quality_level), None)
        if quality_option is None:
            continue

        unit_price = quality_option['price']

        # Check if 'quantity' key exists in the ingredient dictionary
        if 'quantity' in ingredient:
            quantity = ingredient['quantity']
        else:
            # If 'quantity' key is missing, print an error message
            print(f"Error: Quantity for ingredient '{ingredient_name}' is missing. RESTART SERVER!!!")
            return None

        # Calculate additional cost based on quality level
        additional_cost = 0.05 if quality_level == 'medium' else 0.10 if quality_level == 'low' else 0

        # Calculate ingredient cost
        ingredient_cost = (quantity / 1000) * unit_price

        # Add ingredient cost to the total price
        total_price += ingredient_cost + additional_cost

    print(f"DEBUG: Total price before rounding: {total_price}")
    total_price = round(total_price, 5)
    print(f"DEBUG: Total price after rounding: {total_price}")

    return total_price

def find_highest_quality_meal(budget, is_vegetarian=False, is_vegan=False):
    highest_quality_meal = None
    highest_quality_score = -1
    highest_quality_price = -1
    highest_quality_ingredients = None
    
    for meal in menu_data['meals']:
        if (not is_vegetarian or is_vegetarian_meal(meal)) and (not is_vegan or is_vegan_meal(meal)):
            # Generate all possible combinations of ingredient qualities
            ingredient_names = [ingredient['name'] for ingredient in meal['ingredients']]
            quality_combinations = generate_quality_combinations(ingredient_names)
            
            for quality_combination in quality_combinations:
                # Calculate the total price of the meal
                total_price = calculate_price(meal['id'], quality_combination)
                
                # Calculate the quality score for the combination
                quality_result = calculate_quality(meal['id'], quality_combination)
                overall_quality = quality_result['quality_scores']
                
                # Check if the meal fits within the budget and has higher quality score
                if total_price <= budget and overall_quality > highest_quality_score:
                    highest_quality_meal = meal
                    highest_quality_score = overall_quality
                    highest_quality_price = total_price
                    highest_quality_ingredients = quality_result['ingredient_quality']
                # If the current meal has the same quality but higher price, update the highest quality meal
                elif total_price <= budget and overall_quality == highest_quality_score and total_price > highest_quality_price:
                    highest_quality_meal = meal
                    highest_quality_score = overall_quality
                    highest_quality_price = total_price
                    highest_quality_ingredients = quality_result['ingredient_quality']
    
    if highest_quality_meal:
        return {
            'id': highest_quality_meal['id'],
            'ingredients': highest_quality_ingredients,
            'price': highest_quality_price,
            'quality_score': highest_quality_score
        }
    else:
        return None

def find_highest_quality_meal_of_meal(meal_id, budget, is_vegetarian=False, is_vegan=False):
    highest_quality_meal = None
    highest_quality_score = -1
    highest_quality_price = -1
    highest_quality_ingredients = None
    
    meal = next((m for m in menu_data['meals'] if m['id'] == meal_id), None)
    if meal is None:
        return None  # Return None if the provided meal ID does not exist
    
    # Generate all possible combinations of ingredient qualities for the specified meal
    ingredient_names = [ingredient['name'] for ingredient in meal['ingredients']]
    quality_combinations = generate_quality_combinations(ingredient_names)
    
    for quality_combination in quality_combinations:
        # Calculate the total price of the meal
        total_price = calculate_price(meal['id'], quality_combination)
        print("Total price:", total_price)
        
        # Calculate the quality score for the combination
        quality_result = calculate_quality(meal['id'], quality_combination)
        overall_quality = quality_result['quality_scores']
        
        # Check if the meal fits within the budget and has higher quality score
        if total_price <= budget and overall_quality > highest_quality_score:
            highest_quality_meal = meal
            highest_quality_score = overall_quality
            highest_quality_price = total_price
            highest_quality_ingredients = quality_result['ingredient_quality']
        # If the current meal has the same quality but higher price, update the highest quality meal
        elif total_price <= budget and overall_quality == highest_quality_score and total_price > highest_quality_price:
            highest_quality_meal = meal
            highest_quality_score = overall_quality
            highest_quality_price = total_price
            highest_quality_ingredients = quality_result['ingredient_quality']
    
    if highest_quality_meal:
        return {
            'id': highest_quality_meal['id'],
            'name': highest_quality_meal['name'],
            'price': highest_quality_price,
            'quality_score': highest_quality_score,
            'ingredients': highest_quality_ingredients
        }
    else:
        return None


# Function to generate all possible combinations of ingredient qualities
def generate_quality_combinations(ingredient_names):
    quality_levels = ['low', 'medium', 'high']
    quality_combinations = []

    # Generate all possible combinations of quality levels for the given ingredients
    for combo in itertools.product(quality_levels, repeat=len(ingredient_names)):
        quality_combinations.append(dict(zip(ingredient_names, combo)))

    return quality_combinations
