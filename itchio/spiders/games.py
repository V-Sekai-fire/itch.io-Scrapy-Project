from scrapy import Request, Spider

class GameSpider(Spider):
    name = "games"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 1000))

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://itch.io/games/top-rated?page={i}")

    def parse(self, response):
        for game in response.css("div.game_cell"):
            rating = game.css("div.game_rating")
            star_value = rating.css("div.star_value span.screenreader_only::text").get()
            star_value = float(star_value.split()[1]) / 5 # Currently out of 5
            star_value = round(float(star_value), 2)
            num_ratings = rating.css("span.rating_count::text").get()
            num_ratings = num_ratings.replace('(', '').replace(',', '')
            author = game.css("div.game_author a::text").get()
            yield {
                "title": game.css("a.title::text").get(default=""),
                "title_url": game.css("a.title::attr(href)").get(default=""),
                "author": author,
                "game_text": game.css("div.game_text::text").get(default=""),
                "game_genre": game.css("div.game_genre::text").get(default=""),
                "platform": ",".join(
                    set(game.css("div.game_platform span::attr(title)").getall())
                ),
                "star_rating": star_value,
                "num_ratings": num_ratings,
            }
