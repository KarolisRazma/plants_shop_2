import plant as p
import seller as s


class PlantShop:

    def __init__(self):
        # Initial Data
        plant1 = p.Plant("Rose", "Flower")
        plant2 = p.Plant("Oak", "Tree")
        plant3 = p.Plant("Sunflower", "Flower")

        seller1 = s.Seller("Name1", "Surname1")
        seller2 = s.Seller("Name2", "Surname2")
        seller3 = s.Seller("Name3", "Surname3")

        seller1.workplace_id = 1
        seller3.workplace_id = 3

        # Fields
        self.plants = [plant1, plant2, plant3]
        self.sellers = [seller1, seller2, seller3]

        # Add sellers to plants
        self.add_seller_to_plant(plant_id=1, seller_id=1)
        self.add_seller_to_plant(plant_id=1, seller_id=2)
        self.add_seller_to_plant(plant_id=2, seller_id=2)

    # Add to seller to Plant object field of type list "sellers"
    def add_seller_to_plant(self, plant_id, seller_id):
        plant = self.get_plant_by_id(plant_id)
        seller = self.get_seller_by_id(seller_id)
        plant.sellers.append(seller)

    # Standard getters
    def get_plant_by_id(self, plant_id):
        for plant in self.plants:
            if plant.id == plant_id:
                return plant
        return None

    def get_seller_by_id(self, seller_id):
        for seller in self.sellers:
            if seller.id == seller_id:
                return seller
        return None

    # Create dictionary methods
    def make_plants_dict(self):
        plants_dict = []
        for plant in self.plants:
            plants_dict.append(plant.__dict__())
        return plants_dict

    def make_sellers_dict(self):
        sellers_dict = []
        for seller in self.sellers:
            sellers_dict.append(seller.__dict__())
        return sellers_dict

    # Dictionary getters
    def get_plant_dict_by_id(self, plant_id):
        plants_dict = self.make_plants_dict()
        for plant in plants_dict:
            if plant['id'] == plant_id:
                return plant

    def get_seller_dict_by_id(self, seller_id):
        sellers_dict = self.make_sellers_dict()
        for seller in sellers_dict:
            if seller['id'] == seller_id:
                return seller

    # From dictionary sellers to Seller objects list
    @staticmethod
    def from_dict_to_sellers_objects(sellers_dict):
        sellers_objs = []
        for seller in sellers_dict:
            seller_obj = s.Seller(seller['name'], seller['surname'], is_generating_id=False)
            seller_obj.id = seller['id']
            sellers_objs.append(seller_obj)
        return sellers_objs
