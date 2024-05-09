import json

def load_menu_from_file(file_path):
    with open(file_path, 'r') as file:
        menu_data = json.load(file)
    return menu_data

# Load menu data from the provided JSON file
menu_data = load_menu_from_file('menu.json')

def get_meal_by_id(meal_id):
    for meal in menu_data["meals"]:
        if meal["id"] == meal_id:
            # Get the ingredients with their options from the menu data
            ingredients_with_options = []
            for ingredient in meal["ingredients"]:
                ingredient_name = ingredient["name"]
                ingredient_data = next(
                    (ing for ing in menu_data["ingredients"] if ing["name"].lower() == ingredient_name.lower()),
                    None,
                )
                if ingredient_data:
                    ingredient_with_options = {
                        "name": ingredient_name,
                        "groups": ingredient_data["groups"],
                        "options": ingredient_data["options"],
                    }
                    ingredients_with_options.append(ingredient_with_options)
            # Replace the original ingredients with options
            meal["ingredients"] = ingredients_with_options
            return meal
    return None

def filter_meals(is_vegetarian, is_vegan):
    all_meals = menu_data['meals']
    
    if not is_vegetarian and not is_vegan:
        return all_meals  # Return all meals if neither is_vegetarian nor is_vegan
    
    filtered_meals = []
    for meal in all_meals:
        if is_vegetarian and not is_vegan:
            if is_vegetarian_meal(meal):
                filtered_meals.append(meal)
        elif is_vegan:
            if is_vegan_meal(meal):
                filtered_meals.append(meal)
    
    return filtered_meals

def is_vegetarian_meal(meal):
    for ingredient in meal['ingredients']:
        if not is_vegetarian_ingredient(ingredient):
            return False
    return True

def is_vegetarian_ingredient(ingredient):
    for option in menu_data['ingredients']:
        if option['name'] == ingredient['name']:
            for group in option['groups']:
                if group.lower() == 'vegetarian':
                    return True
    return False

def is_vegan_meal(meal):
    for ingredient in meal['ingredients']:
        if not is_vegan_ingredient(ingredient):
            return False
    return True

def is_vegan_ingredient(ingredient):
    for option in menu_data['ingredients']:
        if option['name'] == ingredient['name']:
            for group in option['groups']:
                if group.lower() == 'vegan':
                    return True
    return False
