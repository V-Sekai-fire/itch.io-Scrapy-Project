from ludwig.api import LudwigModel

config = {
    "input_features": [
        {
            "name": "platform",
            "type": "category",
        },
        {
            "name": "game_genre",
            "type": "category",
        },
        {
            "name": "num_ratings",
            "type": "numerical",
        },
        {
            "name": "star_rating",
            "type": "numerical",
        }
    ],
    "output_features": [
        {
            "name": "game_text",
            "type": "text",
            "encoder": {
                "type": "auto_transformer",
                "pretrained_model_name_or_path": "bigscience/bloom-3b",
                "trainable": True,
            },
        },
    ],
    "trainer": {"learning_rate": 0.00001, "epochs": 3},
}

model = LudwigModel(config)

train_stats = model.train(dataset="items_games_4.csv")
