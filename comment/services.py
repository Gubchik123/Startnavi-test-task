from django.conf import settings
import google.generativeai as genai


def get_ai_response(prompt):
    """Returns the response to the given prompt."""
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
