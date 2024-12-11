import pymongo
import json
from pymongo import MongoClient
from bson import ObjectId
import random

# Update the MongoClient to use the provided connection string
client = MongoClient("mongodb+srv://ihub:ihub@test-portal.lcgyx.mongodb.net/test_portal_db?retryWrites=true&w=majority")
db = client["test_portal_db"]
students_collection = db['students']

# Define options for colleges and departments
colleges = ['snsct', 'snsce', 'sns arts']
departments = ['it', 'cse', 'ece', 'mech', 'eee']

# Generate a list of random names
names = [
    "Madhan", "Karthik", "Preethi", "Suresh", "Anitha", "Vishal", "Divya", "Rajesh",
    "Nithya", "Ravi", "Meera", "Akash", "Sneha", "Ajith", "Priya", "Rahul",
    "Swathi", "Ganesh", "Pooja", "Arun", "Lakshmi", "Hari", "Deepa", "Vikram",
    "Shalini", "Abhishek", "Keerthi", "Rohit", "Monika", "Satish", "Harini", "Sanjay"
]

# Generate dummy data
dummy_data = []

for i in range(1, 10):  # Generate 100 records
    name = random.choice(names)  # Randomly pick a name
    dummy_data.append({
        "name": name,
        "email": f"{name.lower()}{i}@gmail.com",  # Ensure unique emails
        "password": name.lower(),
        "collegename": random.choice(colleges),
        "dept": random.choice(departments),
        "regno": f"713521{random.choice(departments)}{str(i).zfill(3)}"  # Unique regno
    })

# Insert data into the collection
result = students_collection.insert_many(dummy_data)
print(f"Inserted {len(result.inserted_ids)} records into the database.")