class Seller:
    static_seller_id = 1

    def __init__(self, seller_name, seller_surname, is_generating_id=True):
        if is_generating_id:
            # automatic id assignment to seller
            self.id = Seller.static_seller_id
            Seller.static_seller_id += 1
        else:
            # id will be declared manually
            self.id = None

        self.name = seller_name
        self.surname = seller_surname
        self.workplace_id = None

        # Store it as a dict
        self.workplace = None

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'workplace_id': self.workplace_id
        }

    # def set_workplace(self, workplace_id):
    #     url = f'http://workplace:80/workplaces/{workplace_id}'
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         workplace_data = response.json()
    #         self.workplace_id = workplace_id
    #         self.workplace = workplace_data
    #         return True
    #     else:
    #         return False
