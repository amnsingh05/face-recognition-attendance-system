import csv
import bcrypt

users = [
    {
        "username": "admin",
        "password": "1234",
        "role": "Administrator",
        "security_question": "What is your favorite color?",
        "security_answer": "blue"
    },
    {
        "username": "teacher1",
        "password": "teacher123",
        "role": "Teacher",
        "security_question": "What city were you born in?",
        "security_answer": "delhi"
    },
    {
        "username": "staff1",
        "password": "staff123",
        "role": "Staff",
        "security_question": "What is your pet’s name?",
        "security_answer": "tiger"
    }
]

with open("users.csv", "w", newline="") as file:
    fieldnames = ["username", "password", "role", "security_question", "security_answer"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for user in users:
        hashed_pw = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        writer.writerow({
            "username": user["username"],
            "password": hashed_pw,
            "role": user["role"],
            "security_question": user["security_question"],
            "security_answer": user["security_answer"].lower()
        })

print("✅ users.csv created successfully with encrypted passwords!")
