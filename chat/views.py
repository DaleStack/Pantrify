from django.shortcuts import render
from django.conf import settings
import google.generativeai as genai
import re

def is_likely_ingredient_list(text):
    return bool(re.search(r"[a-zA-Z]", text)) and not re.match(r".*\d+\s*[\+\-\*/]", text)

def recipe(request):
    if request.method == "POST":
        ingredients = request.POST.get("ingredients", "").strip()

        if not ingredients:
            return render(request, "chat/recipe.html", {
                "error": "Please enter some ingredients."
            })

        if not is_likely_ingredient_list(ingredients):
            return render(request, "chat/recipe.html", {
                "error": "Please enter a valid list of ingredients, not a math problem or general question."
            })

        # Strict prompt
        prompt = (
            "You are a recipe generator. Only respond with a recipe using the provided ingredients. "
            "If the input is unrelated to cooking, reply with: "
            "'Please enter valid ingredients to generate a recipe.'\n"
            f"Ingredients: {ingredients}"
        )

        try:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)

            recipe_text = response.text if hasattr(response, 'text') else str(response)

            return render(request, "chat/recipe.html", {
                "recipe": recipe_text,
                "ingredients": ingredients
            })
        except Exception as e:
            return render(request, "chat/recipe.html", {
                "error": "Failed to generate recipe. Please try again later.",
                "debug": str(e)
            })

    return render(request, "chat/recipe.html")
