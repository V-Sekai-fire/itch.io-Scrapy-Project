from scrapy import Request, Spider


class GameSpider(Spider):
    name = "games"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 10))

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://itch.io/games?page={i}")

    def parse(self, response):
        for game in response.css("div.game_cell"):
            yield {
                "title": game.css("a.title::text").get(),
                "title_url": game.css("a.title::attr(href)").get(),
                "game_text": game.css("div.game_text::text").get(),
                "game_genre": game.css("div.game_genre::text").get(),
                "author": game.css("div.game_author a::text").get(),    
                "price": game.css("div.price::text").get(),      
                "synopsis": game.css("div.synopsis::text").get(),    
                "rating": game.css("div.rating::text").get(),    
                "reviewers": game.css("div.reviewers::text").get(),            
            }