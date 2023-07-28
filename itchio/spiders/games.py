from scrapy import Request, Spider

class GameSpider(Spider):
    name = "games"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.pages = int(kwargs.get("pages", 40))
        
    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://itch.io/games?page={i}")
         
    def parse(self, response):
        for game in response.css("div.game_cell"):
            yield {
                "title": game.css("a.title::text").get(default=""),        
                "title_url": game.css("a.title::attr(href)").get(default=""),  
                "game_text": game.css("div.game_text::text").get(default=""),  
                "game_genre": game.css("div.game_genre::text").get(default=""),
                "platform": ','.join(set(game.css("div.game_platform span::attr(title)").getall())),
            }
