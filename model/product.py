from dataclasses import dataclass

@dataclass
class Product:
    id: int
    product_name: str
    brand_id: int
    category_id: int
    model_year: int
    list_price: float

    def __str__(self):
        return self.product_name

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
