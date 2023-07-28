import os
from ludwig.api import LudwigModel
import gradio as gr

config = {
    "input_features": [
        {"name": "platform", "type": "category"},
        {"name": "game_genre", "type": "category"},
        {"name": "num_ratings", "type": "numerical"},
        {"name": "star_rating", "type": "numerical"}
    ],
    "output_features": [
        {
            "name": "game_text",
            "type": "text",
            "encoder": {"type": "distilbert", "trainable": True}
        }
    ],
    "trainer": {
        "epochs": 3,
        "learning_rate": 0.00001,
        "optimizer": {"type": "adamw"},
        "use_mixed_precision": True,
        "learning_rate_scheduler": {"decay": "linear", "warmup_fraction": 0.2},
        "batch_size": 32
    }
}

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

model_dir = ''  # replace with your model directory path
model = LudwigModel(config)

if not os.path.exists(model_dir):
    # Train the model if it does not exist
    train_stats = model.train(dataset="items_games_5.csv", gpus=[0, 1])
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
