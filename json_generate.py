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
            temperature=0,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""

        return response_text

    except Exception as e:
        return f"Error querying the model: {e}"


def create():
    """Reads input from input.txt, generates a workout plan, and writes to output.json."""
    with open('input.txt', 'r') as f:
        my_dict = {key: int(value) for line in f for key, value in [line.strip().split(': ')]}

    print(my_dict)

    goal_dict = {
        1: "cardio",
        2: "muscle toning",
        3: "ab development",
        4: "bicep muscle development",
        5: "leg muscle development",
        6: "general muscle development"
    }
    experience_dict = {
        1: "no experience",
        2: "some experience",
        3: "extensive experience"
    }
    gym_dict = {
        1: "the gym",
        2: "home"
    }
    exer = {1: "jumping jacks", 2: "squat", 3: "situp", 4: "pushups"}
    exer_list = ", ".join(exer.values())

    user_prompt = (
        f"Can you please generate a week, with {my_dict['days_per_week']} days workout plan for someone whose weight is "
        f"{my_dict['weight']} kgs, has a height of {my_dict['height']} inches, and whose goal for the workout is "
        f"{goal_dict[my_dict['goal']]}. They have {experience_dict[my_dict['experience']]} experience and can only do the following exercises: {exer_list}. "
        f"{my_dict['time_available']} hours available per day to workout, and will do the workouts at "
        f"{gym_dict[my_dict['location']]}. Please specify the day of the week by name. At the end, provide "
        f"guidance on what types of food to eat and what types of food to avoid. Format everything as a JSON dict file "
        f"with the keys: 'workout_plan', 'food_to_eat', and 'food_to_avoid'. Give only json file in output, remove every other text, only json json json"
    )

    print(user_prompt)
    workout_suggestion = getResponse(user_prompt)
    print(workout_suggestion)

    with open("output.json", "w") as f:
        f.write(workout_suggestion)

