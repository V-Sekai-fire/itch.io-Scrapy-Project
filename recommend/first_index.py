# MIT License

# Copyright (c) 2023-present K. S. Ernest (iFire) Lee

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import marqo
import csv

mq = marqo.Client(url='http://127.0.0.1:8882')

database_name = "itch-search"

with open("items_games_5.csv", mode='r') as infile:
    reader = csv.DictReader(infile, skipinitialspace=True)
    games = [r for r in reader]

entries = []
length_of_input = len(games)

for i in range(length_of_input):
    c = games[i]
    entry = {
        "author": c["author"], 
        "game_genre": c["game_genre"],
        "game_text": c["game_text"],
        "num_ratings": c["num_ratings"],
        "platform": c["platform"],
        "star_rating": c["star_rating"],
        "title": c["title"],
        "title_url": c["title_url"]
    }
    entries.append(entry)

searchable_attributes = ["author", "game_genre", "game_text", "num_ratings", "platform", "star_rating", "title", "title_url"]

mq.index(database_name).add_documents(entries, device="cpu", client_batch_size=40, tensor_fields=searchable_attributes)

results = mq.index(database_name).search(
    q="List a visual novel.", searchable_attributes=searchable_attributes
)

print(results)
