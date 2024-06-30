 ## Features

### load_menu_from_file(file_path)

- This function takes a file path as input and reads the content of a JSON file located at that path.
- It loads the menu data from the JSON file and returns it.

### select_random_meal()

- This function selects a random meal from the loaded menu data.
- It returns a randomly chosen meal from the menu.

### generate_random_quality(ingredient)

- This function generates a random quality level for a given ingredient.
- It returns a randomly chosen quality level ('low', 'medium', or 'high').

### calculate_quality(meal_id, ingredient_qualities, numeric=False)

- This function calculates the overall quality of a meal based on the quality of its ingredients.
- It takes three parameters: meal_id (the ID of the meal), ingredient_qualities (a dictionary containing the quality of each ingredient), and numeric (a boolean indicating whether to return the numeric quality score or not).
- It calculates the quality score for each ingredient, then computes the overall quality score for the meal.
- If numeric is True, it returns the numeric quality score; otherwise, it returns a mapping of the score to a textual quality level.

### calculate_price(meal_id, ingredient_qualities)

- This function calculates the total cost of a meal based on the prices of its ingredients.
- It takes two parameters: meal_id (the ID of the meal) and ingredient_qualities (a dictionary containing the quality of each ingredient).
- It calculates the cost of each ingredient based on its quality level and quantity, then sums up the costs to get the total price of the meal.

### find_highest_quality_meal(budget, is_vegetarian=False, is_vegan=False)

- This function finds the highest-quality meal within a given budget, considering optional filters for vegetarian and vegan meals.
- It iterates through all meals, calculates the quality scores and prices for each combination of ingredients, and selects the meal with the highest quality score that fits within the budget.

### find_highest_quality_meal_of_meal(meal_id, budget, is_vegetarian=False, is_vegan=False)

- This function finds the highest-quality meal of a specific meal ID within a given budget, considering optional filters for vegetarian and vegan meals.
- It follows a similar process to find_highest_quality_meal, but focuses only on the specified meal ID.

### generate_quality_combinations(ingredient_names)
- This function generates all possible combinations of quality levels for a given list of ingredient names.
- It creates combinations of 'low', 'medium', and 'high' quality levels for each ingredient.

### RequestHandler class

- This class defines a custom request handler for the HTTP server.
- It handles GET and POST requests for different endpoints like '/getMeal', '/search', '/listMeals', '/quality', '/random', '/price', '/findHighest', and '/findHighestOfMeal'.

### get_meal_by_id(meal_id)

- This function retrieves meal data by its ID from the loaded menu data.
- It returns the meal data including ingredients and their options.

### filter_meals(is_vegetarian, is_vegan)

- This function filters meals based on whether they are vegetarian, vegan, or both.
- It returns a list of meals that match the filter criteria.

### is_vegetarian_meal(meal)
- This function checks if a meal is vegetarian by examining its ingredients.
- It returns True if all ingredients are vegetarian, False otherwise.

### is_vegetarian_ingredient(ingredient)
- This function checks if an ingredient is vegetarian by examining its groups.
- It returns True if the ingredient is vegetarian, False otherwise.

### is_vegan_meal(meal)
This function checks if a meal is vegan by examining its ingredients.
It returns True if all ingredients are vegan, False otherwise.

### is_vegan_ingredient(ingredient)
- This function checks if an ingredient is vegan by examining its groups.
- It returns True if the ingredient is vegan, False otherwise.

### run(server_class=HTTPServer, handler_class=RequestHandler, port=8080)
- This function starts the HTTP server using the provided server class, request handler class, and port number.
- It listens for incoming HTTP requests and handles them using the specified request handler.


## How to Use

- Download the repo as a zip file. 
- Run the server.py file and enter the parameters you want to query into the terminal.

## Example Usage


### Listing the Menu

```bash
$ curl http://localhost:8080/listMeals
```

Example JSON output:
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/1.png)


### Getting an Item from Menu

```bash
$ curl http://localhost:8080/getMeal?id=2
```

Example JSON output:
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/2.png)

### Quality Calculation With Ingredient Qualities

Example JSON output:
```bash
$ curl -d "meal_id=3&Chicken=medium" -X POST http://localhost:8080/quality
{"quality": {"quality_scores": 25.0, "ingredient_quality": {"Chicken": 20, "Vegetables": 30}}}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/3.png)

If there is no ingredient with the given ID in the entered parameters, it will give an error message

```bash
$ curl -d "meal_id=3&Chicken=medium&Rice=medium&Wine=low" -X POST http://localhost:8080/quality
{"error": "The following ingredients are not part of meal 3: Rice, Wine"}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/3.1.png)


### Price Calculation With Ingredient Qualities

```bash
$ curl -d "meal_id=3&Chicken=low" -X POST http://localhost:8080/price  
{"price": 2.36}%
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/4.png)

If there is no ingredient with the given ID in the entered parameters, it will give an error message

```bash
$ curl -d "meal_id=3&Chicken=low&Tofu=medium" -X POST http://localhost:8080/price
{"error": "The following ingredients are not part of meal 3: Tofu"}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/4.1.png)


### I'm Feeling Lucky

```bash
$ curl -d "budget=3.5" -X POST http://localhost:8080/random
{"id": 8, "name": "Vegetarian stir-fry with tofu", "price": 2.1, "quality_score": 23, "ingredients": [{"name": "Tofu", "quality": "high"}, {"name": "Rice", "quality": "high"}, {"name": "Vegetables", "quality": "low"}]}

$ curl -d "budget=3.5" -X POST http://localhost:8080/random
{"id": 9, "name": "Fruit salad with mixed berries and yogurt", "price": 1.64, "quality_score": 10, "ingredients": [{"name": "Mixed berries", "quality": "low"}, {"name": "Yogurt", "quality": "low"}]}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/5.png)


If no menu is found within the given budget, it will give an error message.

```bash
$ curl -d "budget=0.5" -X POST http://localhost:8080/random
{"error": "No menu suitable for your budget was found"}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/5.1.png)

### Searching For a Meal

```bash
$ curl http://localhost:8080/search\?query\=milk
[]

$ curl http://localhost:8080/search\?query\=beef
[{"id": 4, "name": "Beef stir-fry with rice", "ingredients": ["Beef", "Rice", "Vegetables"]}]
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/6.png)

### Finding the Highest Quality Meal For Given Budget

```bash
$ curl -d "budget=3.5&is_vegetarian=false&is_vegan=false" -X POST http://localhost:8080/findHighest
{"menu_id": 8, "menu_name": "Vegetarian stir-fry with tofu", "price": 3.2, "quality_score": 30.0, "ingredients": {"Tofu": "High", "Rice": "High", "Vegetables": "High"}}

$ curl -d "budget=0.91&is_vegetarian=false&is_vegan=false" -X POST http://localhost:8080/findHighest
{"menu_id": 1, "menu_name": "Rice and chicken bowl", "price": 0.8, "quality_score": 20.0, "ingredients": {"Rice": "High", "Chicken": "Low"}}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/7.png)

If no menu is found within the given budget, it will give an error message.

```bash
$ curl -d "budget=0.5&is_vegetarian=false&is_vegan=false" -X POST http://localhost:8080/findHighest
{"error": "No suitable meal found within the budget"}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/7.1.png)

### Finding the Highest Quality Version of a Meal For Given Budget

```bash
$ curl -d "budget=3.4&meal_id=2&is_vegan=false" -X POST http://localhost:8080/findHighestOfMeal
{"id": 2, "name": "Pasta with marinara sauce and vegetables", "price": 2.97, "quality_score": 23.333333333333332, "ingredients": {"Pasta": "High", "Marinara sauce": "Low", "Vegetables": "High"}}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/8.png)

If it cannot find a suitable meal within the budget for the specified meal ID, it will give an error message.

```bash
$ curl -d "budget=2.4&meal_id=7&is_vegan=false" -X POST http://localhost:8080/findHighestOfMeal
{"error": "No suitable meal found within the budget for the specified meal ID"}
```
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/8.1.png)


## THERE IS AN ERROR IN THE DATA SET

![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/9.png)
![alt text](https://github.com/iamyusufgoktas/Yusuf-Goktas-otsimo-internship-task-2024/blob/main/images/9.1.png)

When calculating the price, it defaults "Pork chops" to "high" quality. To change this, we either need to convert "PORK" to "Pork chops" in the ingredients section or write "Pork chops" as "Pork" in the meal section.
