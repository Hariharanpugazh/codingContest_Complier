import pymongo
import json
from pymongo import MongoClient
from bson import ObjectId

# Update the MongoClient to use the provided connection string
client = MongoClient("mongodb+srv://ihub:ihub@test-portal.lcgyx.mongodb.net/test_portal_db?retryWrites=true&w=majority")
db = client["test_portal_db"]

# Select the collection
questions_collection = db['Questions_Library']

# Load the JSON data
json_data = """
{
    "_id": {
      "$oid": "672dda1832100ee1f4a69fa1"
    },
    "problems": [
      {
        "id": 1,
        "title": "Sum of Two Numbers",
        "role": [
          "Junior Software Developer",
          "Senior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes two numbers as input and returns their sum.",
        "samples": [
          {
            "input": [
              "5",
              "3"
            ],
            "output": "8"
          },
          {
            "input": [
              "10",
              "-5"
            ],
            "output": "5"
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "100",
              "200"
            ],
            "output": "300"
          },
          {
            "input": [
              "-10",
              "-20"
            ],
            "output": "-30"
          }
        ]
      },
      {
        "id": 2,
        "title": "Reverse a String",
        "role": [
          "Junior Software Developer",
          "AI Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes a string as input and returns the string in reverse.",
        "samples": [
          {
            "input": [
              "hello"
            ],
            "output": "olleh"
          },
          {
            "input": [
              "world"
            ],
            "output": "dlrow"
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "hidden"
            ],
            "output": "neddih"
          },
          {
            "input": [
              "reverse"
            ],
            "output": "esrever"
          }
        ]
      },
      {
        "id": 3,
        "title": "Find Maximum in List",
        "role": [
          "Junior Software Developer",
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that takes a list of numbers and returns the maximum number.",
        "samples": [
          {
            "input": [
              4,
              3,
              1,
              9,
              7
            ],
            "output": 9
          },
          {
            "input": [
              4,
              -1,
              -5,
              -3,
              -4
            ],
            "output": -1
          }
        ],
        "hidden_samples": [
          {
            "input": [
              4,
              10,
              20,
              5,
              15
            ],
            "output": 20
          },
          {
            "input": [
              4,
              -10,
              -20,
              -30
            ],
            "output": -10
          }
        ]
      },
      {
        "id": 4,
        "title": "Factorial of a Number",
        "role": [
          "Junior Software Developer",
          "AI Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that calculates the factorial of a given number.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": 120
          },
          {
            "input": [
              3
            ],
            "output": 6
          }
        ],
        "hidden_samples": [
          {
            "input": [
              7
            ],
            "output": 5040
          },
          {
            "input": [
              4
            ],
            "output": 24
          }
        ]
      },
      {
        "id": 5,
        "title": "Count Vowels in a String",
        "role": "Senior Software Developer",
        "level": "easy",
        "problem_statement": "Write a function that takes a string as input and returns the number of vowels in the string.",
        "samples": [
          {
            "input": [
              "example"
            ],
            "output": 3
          },
          {
            "input": [
              "programming"
            ],
            "output": 3
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "hidden test"
            ],
            "output": 3
          },
          {
            "input": [
              "vowel count"
            ],
            "output": 4
          }
        ]
      },
      {
        "id": 6,
        "title": "Check Prime Number",
        "role": [
          "Junior Software Developer",
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that checks if a given number is a prime number.",
        "samples": [
          {
            "input": [
              7
            ],
            "output": true
          },
          {
            "input": [
              10
            ],
            "output": false
          }
        ],
        "hidden_samples": [
          {
            "input": [
              23
            ],
            "output": true
          },
          {
            "input": [
              25
            ],
            "output": false
          }
        ]
      },
      {
        "id": 7,
        "title": "Fibonacci Sequence",
        "role": [
          "Senior Software Developer"
        ],
        "level": "hard",
        "problem_statement": "Write a function that returns the nth Fibonacci number.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": 5
          },
          {
            "input": [
              7
            ],
            "output": 13
          }
        ],
        "hidden_samples": [
          {
            "input": [
              10
            ],
            "output": 55
          },
          {
            "input": [
              15
            ],
            "output": 610
          }
        ]
      },
      {
        "id": 8,
        "title": "Palindrome Check",
        "role": [
          "AI Developer",
          "Senior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that checks if a given string is a palindrome.",
        "samples": [
          {
            "input": [
              "madam"
            ],
            "output": true
          },
          {
            "input": [
              "hello"
            ],
            "output": false
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "level"
            ],
            "output": true
          },
          {
            "input": [
              "world"
            ],
            "output": false
          }
        ]
      },
      {
        "id": 9,
        "title": "Sum of Digits",
        "role": [
          "Junior Software Developer",
          "AI Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that takes an integer and returns the sum of its digits.",
        "samples": [
          {
            "input": [
              123
            ],
            "output": 6
          },
          {
            "input": [
              456
            ],
            "output": 15
          }
        ],
        "hidden_samples": [
          {
            "input": [
              789
            ],
            "output": 24
          },
          {
            "input": [
              101
            ],
            "output": 2
          }
        ]
      },
      {
        "id": 10,
        "title": "Binary to Decimal Conversion",
        "role": [
          "AI Developer",
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that converts a binary string to its decimal equivalent.",
        "samples": [
          {
            "input": [
              "101"
            ],
            "output": 5
          },
          {
            "input": [
              "1101"
            ],
            "output": 13
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "10010"
            ],
            "output": 18
          },
          {
            "input": [
              "11111"
            ],
            "output": 31
          }
        ]
      },
      {
        "id": 11,
        "title": "Sum of Even Numbers",
        "role": [
          "Junior Software Developer",
          "AI Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes a list of numbers as input and returns the sum of all even numbers in the list.",
        "samples": [
          {
            "input": [
              [
                1,
                2,
                3,
                4,
                5,
                6
              ]
            ],
            "output": 12
          },
          {
            "input": [
              [
                10,
                15,
                20,
                25
              ]
            ],
            "output": 30
          }
        ],
        "hidden_samples": [
          {
            "input": [
              [
                4,
                8,
                10,
                15
              ]
            ],
            "output": 22
          },
          {
            "input": [
              [
                12,
                18,
                19,
                21
              ]
            ],
            "output": 30
          }
        ]
      },
      {
        "id": 12,
        "title": "Convert Celsius to Fahrenheit",
        "role": [
          "Junior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that converts Celsius to Fahrenheit using the formula: F = C * 9/5 + 32.",
        "samples": [
          {
            "input": [
              0
            ],
            "output": 32
          },
          {
            "input": [
              100
            ],
            "output": 212
          }
        ],
        "hidden_samples": [
          {
            "input": [
              37
            ],
            "output": 98.6
          },
          {
            "input": [
              50
            ],
            "output": 122
          }
        ]
      },
      {
        "id": 13,
        "title": "Count Words in Sentence",
        "role": [
          "AI Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes a sentence as input and returns the count of words.",
        "samples": [
          {
            "input": [
              "Hello world"
            ],
            "output": 2
          },
          {
            "input": [
              "This is a test sentence"
            ],
            "output": 5
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "OpenAI creates AI tools"
            ],
            "output": 4
          },
          {
            "input": [
              "Count words accurately"
            ],
            "output": 3
          }
        ]
      },
      {
        "id": 14,
        "title": "Square Root Calculation",
        "role": [
          "Junior Software Developer",
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that calculates the square root of a given number without using built-in functions.",
        "samples": [
          {
            "input": [
              4
            ],
            "output": 2
          },
          {
            "input": [
              16
            ],
            "output": 4
          }
        ],
        "hidden_samples": [
          {
            "input": [
              81
            ],
            "output": 9
          },
          {
            "input": [
              25
            ],
            "output": 5
          }
        ]
      },
      {
        "id": 15,
        "title": "String to Uppercase",
        "role": [
          "Junior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes a string as input and returns the string in uppercase.",
        "samples": [
          {
            "input": [
              "hello"
            ],
            "output": "HELLO"
          },
          {
            "input": [
              "world"
            ],
            "output": "WORLD"
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "openai"
            ],
            "output": "OPENAI"
          },
          {
            "input": [
              "developer"
            ],
            "output": "DEVELOPER"
          }
        ]
      },
      {
        "id": 16,
        "title": "Odd Numbers in Range",
        "role": [
          "Junior Software Developer",
          "Senior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes two integers and returns a list of odd numbers within that range.",
        "samples": [
          {
            "input": [
              1,
              10
            ],
            "output": [
              1,
              3,
              5,
              7,
              9
            ]
          },
          {
            "input": [
              4,
              15
            ],
            "output": [
              5,
              7,
              9,
              11,
              13,
              15
            ]
          }
        ],
        "hidden_samples": [
          {
            "input": [
              20,
              30
            ],
            "output": [
              21,
              23,
              25,
              27,
              29
            ]
          },
          {
            "input": [
              11,
              19
            ],
            "output": [
              11,
              13,
              15,
              17,
              19
            ]
          }
        ]
      },
      {
        "id": 17,
        "title": "Generate Multiplication Table",
        "role": [
          "AI Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that generates the multiplication table for a given integer up to 10.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": [
              5,
              10,
              15,
              20,
              25,
              30,
              35,
              40,
              45,
              50
            ]
          },
          {
            "input": [
              3
            ],
            "output": [
              3,
              6,
              9,
              12,
              15,
              18,
              21,
              24,
              27,
              30
            ]
          }
        ],
        "hidden_samples": [
          {
            "input": [
              7
            ],
            "output": [
              7,
              14,
              21,
              28,
              35,
              42,
              49,
              56,
              63,
              70
            ]
          },
          {
            "input": [
              9
            ],
            "output": [
              9,
              18,
              27,
              36,
              45,
              54,
              63,
              72,
              81,
              90
            ]
          }
        ]
      },
      {
        "id": 18,
        "title": "Convert Minutes to Hours and Minutes",
        "role": [
          "Junior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that converts a given number of minutes into hours and minutes.",
        "samples": [
          {
            "input": [
              90
            ],
            "output": "1 hour and 30 minutes"
          },
          {
            "input": [
              150
            ],
            "output": "2 hours and 30 minutes"
          }
        ],
        "hidden_samples": [
          {
            "input": [
              45
            ],
            "output": "0 hours and 45 minutes"
          },
          {
            "input": [
              120
            ],
            "output": "2 hours and 0 minutes"
          }
        ]
      },
      {
        "id": 19,
        "title": "Merge Two Sorted Lists",
        "role": [
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that takes two sorted lists and merges them into one sorted list.",
        "samples": [
          {
            "input": [
              [
                1,
                3,
                5
              ],
              [
                2,
                4,
                6
              ]
            ],
            "output": [
              1,
              2,
              3,
              4,
              5,
              6
            ]
          },
          {
            "input": [
              [
                -1,
                3,
                7
              ],
              [
                -2,
                5,
                8
              ]
            ],
            "output": [
              -2,
              -1,
              3,
              5,
              7,
              8
            ]
          }
        ],
        "hidden_samples": [
          {
            "input": [
              [
                0,
                2,
                4
              ],
              [
                1,
                3,
                5
              ]
            ],
            "output": [
              0,
              1,
              2,
              3,
              4,
              5
            ]
          },
          {
            "input": [
              [
                10,
                20
              ],
              [
                5,
                15
              ]
            ],
            "output": [
              5,
              10,
              15,
              20
            ]
          }
        ]
      },
      {
        "id": 20,
        "title": "Decimal to Binary Conversion",
        "role": [
          "AI Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that converts a decimal number to its binary equivalent as a string.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": "101"
          },
          {
            "input": [
              10
            ],
            "output": "1010"
          }
        ],
        "hidden_samples": [
          {
            "input": [
              15
            ],
            "output": "1111"
          },
          {
            "input": [
              32
            ],
            "output": "100000"
          }
        ]
      },
      {
        "id": 21,
        "title": "Count Characters in String",
        "role": [
          "Junior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that takes a string as input and returns the number of characters in the string.",
        "samples": [
          {
            "input": [
              "hello"
            ],
            "output": 5
          },
          {
            "input": [
              "world!"
            ],
            "output": 6
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "OpenAI"
            ],
            "output": 6
          },
          {
            "input": [
              "test123"
            ],
            "output": 7
          }
        ]
      },
      {
        "id": 22,
        "title": "Check if Palindrome",
        "role": [
          "AI Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that checks if a given string is a palindrome.",
        "samples": [
          {
            "input": [
              "racecar"
            ],
            "output": true
          },
          {
            "input": [
              "hello"
            ],
            "output": false
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "madam"
            ],
            "output": true
          },
          {
            "input": [
              "test"
            ],
            "output": false
          }
        ]
      },
      {
        "id": 23,
        "title": "Factorial of Number",
        "role": [
          "Junior Software Developer"
        ],
        "level": "easy",
        "problem_statement": "Write a function that calculates the factorial of a given number.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": 120
          },
          {
            "input": [
              3
            ],
            "output": 6
          }
        ],
        "hidden_samples": [
          {
            "input": [
              7
            ],
            "output": 5040
          },
          {
            "input": [
              4
            ],
            "output": 24
          }
        ]
      },
      {
        "id": 24,
        "title": "Check for Prime Number",
        "role": [
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that checks if a number is a prime number.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": true
          },
          {
            "input": [
              8
            ],
            "output": false
          }
        ],
        "hidden_samples": [
          {
            "input": [
              13
            ],
            "output": true
          },
          {
            "input": [
              16
            ],
            "output": false
          }
        ]
      },
      {
        "id": 25,
        "title": "Fibonacci Sequence Generator",
        "role": [
          "Junior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that generates the first n numbers in the Fibonacci sequence.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": [
              0,
              1,
              1,
              2,
              3
            ]
          },
          {
            "input": [
              8
            ],
            "output": [
              0,
              1,
              1,
              2,
              3,
              5,
              8,
              13
            ]
          }
        ],
        "hidden_samples": [
          {
            "input": [
              3
            ],
            "output": [
              0,
              1,
              1
            ]
          },
          {
            "input": [
              6
            ],
            "output": [
              0,
              1,
              1,
              2,
              3,
              5
            ]
          }
        ]
      },
      {
        "id": 26,
        "title": "Count Occurrences of Word in Sentence",
        "role": [
          "AI Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that counts how often a specified word appears in a given sentence.",
        "samples": [
          {
            "input": [
              "hello world hello",
              "hello"
            ],
            "output": 2
          },
          {
            "input": [
              "test sentence for test",
              "test"
            ],
            "output": 2
          }
        ],
        "hidden_samples": [
          {
            "input": [
              "repeating words repeating words",
              "words"
            ],
            "output": 2
          },
          {
            "input": [
              "no repetition here",
              "here"
            ],
            "output": 1
          }
        ]
      },
      {
        "id": 27,
        "title": "Generate n Prime Numbers",
        "role": [
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that returns the first n prime numbers.",
        "samples": [
          {
            "input": [
              5
            ],
            "output": [
              2,
              3,
              5,
              7,
              11
            ]
          },
          {
            "input": [
              3
            ],
            "output": [
              2,
              3,
              5
            ]
          }
        ],
        "hidden_samples": [
          {
            "input": [
              8
            ],
            "output": [
              2,
              3,
              5,
              7,
              11,
              13,
              17,
              19
            ]
          },
          {
            "input": [
              10
            ],
            "output": [
              2,
              3,
              5,
              7,
              11,
              13,
              17,
              19,
              23,
              29
            ]
          }
        ]
      },
      {
        "id": 28,
        "title": "Find GCD of Two Numbers",
        "role": [
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that finds the greatest common divisor of two numbers.",
        "samples": [
          {
            "input": [
              24,
              36
            ],
            "output": 12
          },
          {
            "input": [
              101,
              103
            ],
            "output": 1
          }
        ],
        "hidden_samples": [
          {
            "input": [
              15,
              25
            ],
            "output": 5
          },
          {
            "input": [
              18,
              27
            ],
            "output": 9
          }
        ]
      },
      {
        "id": 29,
        "title": "Calculate LCM of Two Numbers",
        "role": [
          "Senior Software Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a function that calculates the least common multiple of two numbers.",
        "samples": [
          {
            "input": [
              4,
              5
            ],
            "output": 20
          },
          {
            "input": [
              7,
              3
            ],
            "output": 21
          }
        ],
        "hidden_samples": [
          {
            "input": [
              15,
              20
            ],
            "output": 60
          },
          {
            "input": [
              9,
              12
            ],
            "output": 36
          }
        ]
      },
      {
        "id": 30,
        "title": "Calculate Factorial Recursively",
        "role": [
          "AI Developer"
        ],
        "level": "medium",
        "problem_statement": "Write a recursive function to calculate the factorial of a given number.",
        "samples": [
          {
            "input": [
              4
            ],
            "output": 24
          },
          {
            "input": [
              5
            ],
            "output": 120
          }
        ],
        "hidden_samples": [
          {
            "input": [
              3
            ],
            "output": 6
          },
          {
            "input": [
              6
            ],
            "output": 720
          }
        ]
      }
    ]
  }
"""

# Parse the JSON data
data = json.loads(json_data)

# Convert the $oid to ObjectId
data["_id"] = ObjectId(data["_id"]["$oid"])

# Insert the document into the collection
questions_collection.insert_one(data)

print("Document inserted successfully.")