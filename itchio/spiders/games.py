from scrapy import Request, Spider

class GameSpider(Spider):
    name = "games"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs) 
        self.pages = int(kwargs.get("pages", 40))
        
    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://itch.io/games?page={i}")
         
    # https://itch.io/games/top-rated
    def parse(self, response):
            for game in response.css("div.game_cell"):
                yield {
                    "title": game.css("a.title::text").get(),        
                    "title_url": game.css("a.title::attr(href)").get(),  
                    "game_text": game.css("div.game_text::text").get(),  
                    "game_genre": game.css("div.game_genre::text").get(),         
                    "synopsis": game.css("div.synopsis::text").get(),
                    "platform": ','.join(game.css("div.game_platform span::attr(title)").getall()),
                    "input_methods": ','.join(game.css("div.game_platform span::attr(title)").getall()),      
                    "tags": '|'.join(game.css("div.game_text::text").re(r'#(\w+)'))
            }
                