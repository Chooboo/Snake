class Variables:

    def __init__(self, data):
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.food = data["board"]["food"]
        self.you_health = data["you"]["health"]
        self.you_id = data["you"]["id"]
        self.you_body = data["you"]["body"]
        self.you_x = self.you_body[0]["x"]
        self.you_y = self.you_body[0]["y"]
        self.snakes = data["board"]["snakes"]
        self.board = None