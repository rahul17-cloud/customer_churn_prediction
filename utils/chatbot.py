import google.generativeai as genai


genai.configure(api_key="AIzaSyC9NhPdu8-S8osXgRcMpa_ejQ1EhldMX1g")


model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")  

def get_gemini_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
