import random

# A list of daily health tips
tips = [
    "Drink plenty of water throughout the day 💧",
    "Take a short walk after meals 🚶",
    "Incorporate fruits and vegetables in every meal 🥦",
    "Get at least 7-8 hours of sleep 😴",
    "Limit screen time and take eye breaks 👀",
    "Stretch your body daily to improve flexibility 🧘",
    "Avoid skipping breakfast – fuel your day right ☀️",
    "Practice mindful eating – enjoy your food 🧠🍴",
]

def get_random_tip():
    return random.choice(tips)
