from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from menu_utils import *
from menu_functions import *

# Server request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse request path and query parameters
        url_parts = urlparse(self.path)
        query_params = parse_qs(url_parts.query)
        
        if url_parts.path == '/getMeal':
            # Check if 'id' parameter exists
            if 'id' in query_params:
                meal_id = int(query_params['id'][0])
                meal = get_meal_by_id(meal_id)
                if meal:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(meal).encode('utf-8'))
                else:
                    self.send_error(404, 'Meal not found')
            else:
                self.send_error(400, 'Missing parameter: id')
                
        elif url_parts.path == '/search':
            # Check if 'query' parameter exists
            if 'query' in query_params:
                search_query = query_params['query'][0].lower()  # Convert search query to lowercase for case-insensitive search
                matching_meals = []

                for meal in menu_data['meals']:
                    if search_query in meal['name'].lower():  # Check if search query is contained in meal name
                        matching_meals.append({
                            'id': meal['id'],
                            'name': meal['name'],
                            'ingredients': [ingredient['name'] for ingredient in meal['ingredients']]
                        })

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(matching_meals).encode('utf-8'))
            else:
                self.send_error(400, 'Missing parameter: query')

                
        elif url_parts.path == '/listMeals':
            is_vegetarian = query_params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = query_params.get('is_vegan', ['false'])[0].lower() == 'true'

            meals = filter_meals(is_vegetarian, is_vegan)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(meals).encode('utf-8'))
            
        elif url_parts.path == '/quality':
            self.send_error(405, 'Method Not Allowed')  # Respond with Method Not Allowed for GET requests to /quality
        else:
            self.send_error(404, 'Endpoint not found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        if self.path == '/quality':
            meal_id = int(params.get('meal_id', [-1])[0])
            ingredient_qualities = {k: v[0] for k, v in params.items() if k != 'meal_id'}

            meal = next((m for m in menu_data['meals'] if m['id'] == meal_id), None)
            if meal is None:
                error_message = f"Meal with ID {meal_id} not found"
                print(error_message)
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': error_message}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # Check if all provided ingredients match the ingredients of the meal
                mismatched_ingredients = [ing for ing in ingredient_qualities.keys() if ing not in [i['name'] for i in meal['ingredients']]]
                if mismatched_ingredients:
                    error_message = f"The following ingredients are not part of meal {meal_id}: {', '.join(mismatched_ingredients)}"
                    print(error_message)
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'error': error_message}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    quality = calculate_quality(meal_id, ingredient_qualities, numeric=True)  # Use numerical representation
                    if quality is not None:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'quality': quality}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    else:
                        error_message = "Invalid request or calculation error"
                        print(error_message)
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'error': error_message}
                        self.wfile.write(json.dumps(response).encode('utf-8'))

                
        elif self.path == '/random':
            budget = float(params.get('budget', [float('inf')])[0])

            # List of meals within the budget
            affordable_meals = []

            # Iterate through meals to find those within the budget
            for _ in range(100):  # Try a maximum of 100 times to find a suitable meal
                selected_meal = select_random_meal()

                # Generate random quality parameters for ingredients
                ingredients_with_quality = []
                for ingredient in selected_meal['ingredients']:
                    quality = generate_random_quality(ingredient)
                    ingredients_with_quality.append({'name': ingredient['name'], 'quality': quality})

                # Calculate the total price of the meal
                total_price = calculate_price(selected_meal['id'], {ingredient['name']: ingredient['quality'] for ingredient in ingredients_with_quality})

                if total_price <= budget:
                    affordable_meals.append({
                        'id': selected_meal['id'],
                        'name': selected_meal['name'],
                        'price': total_price,
                        'quality_score': sum(quality_scores[ingredient['quality']] for ingredient in ingredients_with_quality) // len(ingredients_with_quality),
                        'ingredients': ingredients_with_quality
                    })

            if affordable_meals:
                # Select a random meal from the affordable ones
                selected_meal = random.choice(affordable_meals)

                # Prepare the response
                response = {
                    'id': selected_meal['id'],
                    'name': selected_meal['name'],
                    'price': selected_meal['price'],
                    'quality_score': selected_meal['quality_score'],
                    'ingredients': selected_meal['ingredients']
                }

                # Send the response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # If no suitable menu was found, return an error message
                response = {
                    'error': 'No menu suitable for your budget was found'
                }
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path == '/price':
            meal_id = int(params.get('meal_id', [-1])[0])
            ingredient_qualities = {k: v[0] for k, v in params.items() if k != 'meal_id'}

            meal = next((m for m in menu_data['meals'] if m['id'] == meal_id), None)
            if meal is None:
                error_message = f"Meal with ID {meal_id} not found"
                print(error_message)
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'error': error_message}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # Check if all provided ingredients match the ingredients of the meal
                mismatched_ingredients = [ing for ing in ingredient_qualities.keys() if ing not in [i['name'] for i in meal['ingredients']]]
                if mismatched_ingredients:
                    error_message = f"The following ingredients are not part of meal {meal_id}: {', '.join(mismatched_ingredients)}"
                    print(error_message)
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'error': error_message}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    price = calculate_price(meal_id, ingredient_qualities)
                    if price is not None:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'price': price}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    else:
                        error_message = "Invalid request or calculation error"
                        print(error_message)
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'error': error_message}
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                
        elif self.path == '/findHighest':
            budget = float(params.get('budget', [0])[0])
            is_vegetarian = params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = params.get('is_vegan', ['false'])[0].lower() == 'true'

            # Find the highest-quality meal
            highest_quality_meal_info = find_highest_quality_meal(budget, is_vegetarian, is_vegan)

            if highest_quality_meal_info:
                meal_id = highest_quality_meal_info.get('id')
                if meal_id:
                    # Get the meal name for the given meal ID
                    meal_name = next((meal['name'] for meal in menu_data['meals'] if meal['id'] == meal_id), None)
                    if meal_name:
                        response = {
                            'menu_id': meal_id,
                            'menu_name': meal_name,
                            'price': highest_quality_meal_info['price'],
                            'quality_score': highest_quality_meal_info['quality_score'],
                            'ingredients': highest_quality_meal_info['ingredients']
                        }

                        # Send response
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                    else:
                        # Menu name not found for the given menu ID
                        response = {
                            'error': 'Menu name not found for the given menu ID'
                        }
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    # No meal ID found in the highest_quality_meal_info
                    response = {
                        'error': 'No meal ID found in the highest_quality_meal_info'
                    }
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # No suitable meal found within the budget
                response = {
                    'error': 'No suitable meal found within the budget'
                }
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/findHighestOfMeal':
            meal_id = int(params.get('meal_id', [-1])[0])
            budget = float(params.get('budget', [0])[0])
            is_vegetarian = params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = params.get('is_vegan', ['false'])[0].lower() == 'true'

            # Find the highest-quality meal of the specified meal ID
            highest_quality_meal_info = find_highest_quality_meal_of_meal(meal_id, budget, is_vegetarian, is_vegan)

            if highest_quality_meal_info:
                response = {
                    'id': highest_quality_meal_info['id'],
                    'name': highest_quality_meal_info['name'],
                    'price': highest_quality_meal_info['price'],
                    'quality_score': highest_quality_meal_info['quality_score'],
                    'ingredients': highest_quality_meal_info['ingredients']
                }

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                response = {
                    'error': 'No suitable meal found within the budget for the specified meal ID'
                }
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

        else:
            self.send_error(404, 'Endpoint not found')
