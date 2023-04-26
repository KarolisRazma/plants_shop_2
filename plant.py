class Plant:
    static_plant_id = 1

    def __init__(self, name, plant_type, sellers=None):
        if sellers is None:
            sellers = []
        # automatic id assignment to plant
        self.id = Plant.static_plant_id
        Plant.static_plant_id += 1

        self.name = name
        self.type = plant_type
        self.sellers = sellers

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'sellers': self.sellers_dict()
        }

    def sellers_dict(self):
        return [seller.__dict__() for seller in self.sellers]

    def find_seller(self, seller_id):
        for seller in self.sellers:
            if seller.id == seller_id:
                return seller
        return None
