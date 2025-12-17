import lorem

# Total words you want
TOTAL_WORDS = 20000
file_path = "lorem_20000.txt"

words = []
while len(words) < TOTAL_WORDS:
    words.extend(lorem.paragraph().split())

# Keep only the first 20,000 words
words = words[:TOTAL_WORDS]

# Join them into a single string
text = " ".join(words)

# Save to file
with open(file_path, "w") as f:
    f.write(text)

print(f"✅ Generated {TOTAL_WORDS} words of lorem ipsum in '{file_path}'")

