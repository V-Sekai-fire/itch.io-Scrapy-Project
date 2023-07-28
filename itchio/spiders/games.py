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
        for game in response.xpath(".//div[@class='game_cell']"):
            yield {
                "title": game.xpath(".//a[@class='title']/text()").get(),
                "title_url": game.xpath(".//a[@class='title']/@href").get(),
                "game_text": game.xpath(".//div[@class='game_text']/text()").get(),
                "game_genre": game.xpath(".//div[@class='game_genre']/text()").get(),
                "author": game.xpath(".//div[@class='game_author']/a/text()").get(),
                "price": game.xpath(".//div[@class='price']/text()").get(),
                "synopsis": game.xpath(".//div[@class='synopsis']/text()").get(),
                "rating": game.xpath(".//div[@class='rating']/text()").get(),
                "reviewers": game.xpath(".//div[@class='reviewers']/text()").get(),
            }