# Assignemnmt1 Cost Tracker Project

## How to run it 
 uv run tracker.py 

 ## a sample output
 AI COST TRACKER - TRACK B

Prompt: Explain what a Python dictionary is in simple terms and give one short example.

============================================================
Running gemini...

Provider: Gemini (free tier)
Model: gemini-4-hydrogen

AI Response:

A Python dictionary is a way to store data in key-value pairs—much like a real dictionary where you look up a word (the *key*) to find its definition (the *value*), or a phonebook where you look up a name to find a phone number.

Dictionaries are written using curly braces `{}` and let you quickly look up a value as long as you know its key.

### Example

```python
# Creating a dictionary of a person's details
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Looking up a value using its key
print(person["name"])  # Output: Alice
```

Here, `"name"`, `"age"`, and `"city"` are the keys, and `"Alice"`, `25`, and `"New York"` are their matching values.

Input tokens: 46
Output tokens: 198
Speed: 7.397 seconds
Actual cost: $ 0.00000000
Paid-price equivalent (estimated): $ 0.00077700

============================================================
Running groq...

Provider: Groq (free tier)
Model: openai/gpt-oss-120b

AI Response:

A Python dictionary is a built‑in data type that stores information as key‑value pairs.  
Think of it like a real‑world dictionary: you look up a word (the *key*) and you get its definition (the *value*). In Python, you can use any immutable object (strings, numbers, tuples, etc.) as a key, and any object as the corresponding value.

Key points

| Feature | What it means |
|---------|----------------|
| Unordered (as of Python 3.7 the insertion order is preserved, but you shouldn’t rely on it for algorithmic logic)| The pairs don’t have a fixed position like items in a list. |
| Fast lookup | Accessing a value by its key is usually O(1) time – very quick. |
| Mutable | You can add, change, or delete pairs after the dictionary is created. |
| Unique keys | Each key can appear only once; adding a key that already exists overwrites its old value. |

---

### Simple example

```python
# Create a dictionary that stores a person's basic info
person = {
    "name": "Ada",
    "age": 30,
    "city": "New York"
}

# Access a value by its key
print(person["name"])   # Output: Ada

# Add a new key‑value pair
person["profession"] = "Data Scientist"

# Update an existing value
person["age"] = 31

# Remove a pair
del person["city"]

print(person)
# Output: {'name': 'Ada', 'age': 31, 'profession': 'Data Scientist'}
```

In this snippet:

* `"name"`, `"age"`, and `"city"` are keys.
* `"Ada"`, `30`, and `"New York"` are the corresponding values.
* We can look up, add, modify, or delete entries using the keys.

Input tokens: 86
Output tokens: 436
Speed: 1.327 seconds
Actual cost: $ 0.00000000
Paid-price equivalent (estimated): $ 0.00039518



==========================================================================================
GEMINI vs GROQ - SPEED AND COST
==========================================================================================
Provider              Status      Seconds     Tokens in/out     Actual Cost   
------------------------------------------------------------------------------------------
Gemini (free tier)    success     7.397       46/198            $0.00000000   
Groq (free tier)      success     1.327       86/436            $0.00000000   
==========================================================================================

Results saved successfully to results.json