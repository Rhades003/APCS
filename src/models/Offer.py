class Offer:
    def __init__(self, expansion: str, seller: str, quality: str, price: float, quantity: int, bcn: bool = False):
        self.expansion = expansion
        self.seller = seller
        self.quality = quality
        self.price = price
        self.quantity = quantity
        self.bcn = bcn