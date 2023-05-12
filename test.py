import random

words = ['apple', 'banana', 'orange', 'pear', 'grape', 'pineapple', 'mango']

random_words = []

for i in range(5):
    word = random.choice(words)
    random_words.append(word)

print(random_words)


