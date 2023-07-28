from scrapy import Request, Spider

class GameSpider(Spider):
    name = "games"
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs) 
        self.pages = int(kwargs.get("pages", 10))
        
    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(f"https://itch.io/games/top-rated?page={i}")
            
    def parse(self, response):
        for game in response.css("div.game_cell"):
            yield {
                "title": game.css("a.title::text").get() or "",
                "title_url": game.css("a.title::attr(href)").get() or "",
                "game_text": game.css("div.game_text::text").get() or "",
                "game_genre": game.css("div.game_genre::text").get() or "",
                "author": game.css("div.game_author a::text").get() or "", 
                "price": game.css("div.price::text").get() or "",
                "synopsis": game.css("div.synopsis::text").get() or "",
                "rating": game.css("div.rating::text").get() or "",
                "reviewers": game.css("div.reviewers::text").get() or 0,
                "platform": game.css("div.game_platform span::attr(title)").getall() or [],
                "input_methods": game.css("div.game_platform span::attr(title)").getall() or [],
                "tags": game.css("div.game_text::text").re(r'#(\w+)') or [],
                "collection_title": game.css(".collection_title a::text").getall() or [],
                "collection_author": game.css(".collection_author a::text").getall() or []
            }