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

import os
from ludwig.api import LudwigModel
import gradio as gr
import yaml

config_str = """
model_type: llm
base_model: openlm-research/open_llama_3b_v2
input_features:
  - name: star_rating
    type: text
  - name: game_genre
    type: text
  - name: platform
    type: text
  - name: num_ratings
    type: text
output_features:
  - name: game_text
    type: text
quantization:
  bits: 4
adapter:
  type: lora
trainer:
  type: finetune
  learning_rate: 0.0003
  batch_size: 1
  gradient_accumulation_steps: 8
  epochs: 3
  learning_rate_scheduler:
    warmup_fraction: 0.01
backend:
  type: local
"""

config = yaml.safe_load(config_str)


import os
from ludwig.api import LudwigModel
import gradio as gr

# Define the enumeration lists
platform_options = [
    "<UNK>",
    "Download for Linux,Download for macOS,Download for Windows",
    "Download for Windows",
    "Download for macOS,Download for Windows",
    "Download for Linux,Download for macOS,Download for Android,Download for Windows",
    "Download for Linux,Download for Windows",
    "Download for Android,Download for Windows",
    "Download for Android,Download for macOS,Download for Windows",
    "Download for Android",
    "Download for Linux,Download for Android,Download for Windows",
    "Download for macOS",
    "Download for Linux,Download for macOS",
    "Download for Linux,Download for macOS,Download for Android"
]

game_genre_options = [
    "<UNK>",
    "Visual Novel",
    "Adventure",
    "Interactive Fiction",
    "Puzzle",
    "Action",
    "Platformer",
    "Role Playing",
    "Simulation",
    "Strategy",
    "Shooter",
    "Survival",
    "Rhythm",
    "Educational",
    "Card Game",
    "Fighting",
    "Racing",
    "Sports"
]

model_dir = 'results/api_experiment_run_12/model'
import logging
model = LudwigModel(config=config, logging_level=logging.INFO)

if not os.path.exists(model_dir):
    # Train the model if it does not exist
    train_stats = model.train(dataset="items_games_5.csv") # trust_remote_code=True
else:
    # Load the model and run Gradio if the model exists
    model.load(model_dir)
    
    def predict(platform, game_genre, num_ratings, star_rating):
        return model.predict({
            "platform": platform,
            "game_genre": game_genre,
            "num_ratings": num_ratings,
            "star_rating": star_rating
        })
    
    # Use these lists in the Gradio Interface
    iface = gr.Interface(
        fn=predict, 
        inputs=[
            gr.inputs.Dropdown(platform_options, label="Platform"), 
            gr.inputs.Dropdown(game_genre_options, label="Game Genre"), 
            gr.inputs.Slider(minimum=0, maximum=10000, default=5000, label="Number of Ratings"),    
            gr.inputs.Slider(minimum=0, maximum=1, step=0.01, default=0.5, label="Star Rating"),
        ], 
        outputs="text"
    )
    iface.launch()
