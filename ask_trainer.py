from api_key import API_KEY  # Import API key from external file
from groq import Groq

# Initialize Groq client with API key
client = Groq(api_key=API_KEY)


def getResponse(user_prompt):
    """Query the Groq model with the given user prompt."""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=1,
            max_tokens=1024
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error querying the model: {e}"

def initialize(question):
    """Generate a response as a personal trainer answering fitness questions."""
    user_prompt = (
        "You are to act as my personal trainer. I will ask you a question about fitness and exercise, "
        "and you will respond with a helpful answer. If my question is not about fitness and exercise, "
        "you will respond with 'As your personal trainer, I can only answer your fitness-related questions.' "
        "Limit your response to 2 to 3 sentences. The question is: " + question
    )

    workout_suggestion = getResponse(user_prompt)
    return workout_suggestion
