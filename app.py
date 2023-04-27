import plant as pl
import seller as sl
import plants_shop as p_shop
import workplace as wp
from flask import Flask, request, jsonify

app = Flask(__name__)

plant_shop = p_shop.PlantShop()


# ENDPOINTS
# /plants
# /sellers
# /plants/<int:plant_id>
# /sellers/<int:seller_id>
# /plants/<int:plant_id>/sellers
# /plants/<int:plant_id>/sellers/<int:seller_id>


# HTTP GET method functions
@app.get('/plants')
def show_plants():
    plants = plant_shop.make_plants_dict()
    if not plants:
        return jsonify({'message': 'No plants found'}), 404
    return jsonify(plants), 200


@app.get('/sellers')
def show_sellers():
    sellers = plant_shop.make_sellers_dict()
    if not sellers:
        return jsonify({'message': 'No sellers found'}), 404
    return jsonify(sellers), 200


@app.get('/plants/<int:plant_id>')
def show_specific_plant(plant_id):
    plant = plant_shop.get_plant_by_id(plant_id)
    if plant is None:
        return jsonify({'message': 'Plant not found'}), 404

    plant_dict = plant_shop.get_plant_dict_by_id(plant_id=plant_id)
    return jsonify(plant_dict), 200


@app.get('/sellers/<int:seller_id>')
def show_specific_seller(seller_id):
    seller = plant_shop.get_seller_by_id(seller_id)
    if seller is None:
        return jsonify({'message': 'Seller not found'}), 404

    # If seller has no workplace
    if seller.workplace_id is None:
        return jsonify(seller.__dict__()), 200

    # Try to receive a workplace from other service
    workplace = wp.get_workplace(seller.workplace_id)

    if workplace is None:
        # Should never happen
        return jsonify({'message': 'Workplace not found'}), 404

    # If error occured while trying to get response from workplace service
    # if 'error' in workplace:
    #     return jsonify(workplace), 503
        # return jsonify(seller.__dict__()), 200

    response = {
        'id': seller.id,
        'name': seller.name,
        'surname': seller.surname,
        'workplace_id': seller.workplace_id,
        'workplace': workplace,
    }
    return jsonify(response), 200


@app.get('/plants/<int:plant_id>/sellers')
def show_plant_sellers(plant_id):
    plant = plant_shop.get_plant_by_id(plant_id)
    if plant is None:
        return jsonify({'message': 'Plant not found'}), 404

    plant_dict = plant_shop.get_plant_dict_by_id(plant_id=plant_id)
    sellers_dict = plant_dict.get('sellers', [])
    return jsonify(sellers_dict), 200


@app.get('/plants/<int:plant_id>/sellers/<int:seller_id>')
def show_plant_specific_seller(plant_id, seller_id):
    # Check if plant and seller exists
    plant = plant_shop.get_plant_by_id(plant_id)
    if plant is None:
        return jsonify({'message': 'Plant not found'}), 404

    seller = plant_shop.get_seller_by_id(seller_id)
    if seller is None:
        return jsonify({'message': 'Seller not found'}), 404

    # Return json
    plant_dict = plant_shop.get_plant_dict_by_id(plant_id=plant_id)
    sellers_dict = plant_dict['sellers']
    for seller in sellers_dict:
        if seller['id'] == seller_id:

            # Regain object from instead of dict
            seller = plant_shop.get_seller_by_id(seller_id)

            # If seller has no workplace
            if seller.workplace_id is None:
                return jsonify(seller.__dict__()), 200

            # Try to receive a workplace from other service
            workplace = wp.get_workplace(seller.workplace_id)

            if workplace is None:
                # Should never happen
                return jsonify({'message': 'Workplace not found'}), 404

            # If error occured while trying to get response from workplace service
            # if 'error' in workplace:
            #     return jsonify(workplace), 503
                # return jsonify(seller.__dict__()), 200

            response = {
                'id': seller.id,
                'name': seller.name,
                'surname': seller.surname,
                'workplace_id': seller.workplace_id,
                'workplace': workplace,
            }
            return jsonify(response), 200

    return jsonify({'message': 'Seller not found for this plant'}), 404


# HTTP POST method functions
@app.post('/plants')
def add_plant():
    data = request.get_json()
    if len(data) == 4 and 'id' in data:
        del data['id']

    # Check if json is correct
    if len(data) != 3 or 'name' not in data or 'type' not in data or 'sellers' not in data:
        message = "Bad request, incorrect plant object given"
        return jsonify({"Failure": message}), 400

    # Check if sellers exists in plant_shop.sellers
    seller_ids = {seller.id for seller in plant_shop.sellers}
    if not all(seller['id'] in seller_ids for seller in data['sellers']):
        message = "Seller is not found in plant_shop"
        return jsonify({"Failure": message}), 404

    # Append new plant to the list
    sellers_list = plant_shop.from_dict_to_sellers_objects(data['sellers'])
    new_plant = pl.Plant(data['name'], data['type'], sellers_list)
    plant_shop.plants.append(new_plant)

    # Return a JSON response containing information about the newly created plant
    response_data = {
        'id': new_plant.id,
        'name': new_plant.name,
        'type': new_plant.type,
        'sellers': new_plant.sellers_dict()
    }
    return jsonify(response_data), 201, {"location": f"/plants/{new_plant.id}"}


@app.post('/sellers')
def add_seller():
    # 1 option: add seller by name/surname (workplace_id automatically null and id sets automatically)
    # 2 option: add seller by name/surname and json has id (same as 1, ignore id)
    # 3 option add seller by name/surname/wp_id (id sets automatically, workplace field set by function)
    # 4 option same as option, just ignore id
    # 5 option add seller by name/surname and workplace as new resource (fields from workplace service)
    # 6 option same as 5, ignore id

    data = request.get_json()
    # Remove seller id from request body
    if 'id' in data:
        del data['id']

    # Check if JSON object contains the required fields
    # 'name' and 'surname' always must be in request body
    if not all(field in data for field in ['name', 'surname']):
        return jsonify({'error': 'Name and surname fields are required.'}), 400

    # Create new seller
    new_seller = sl.Seller(data['name'], data['surname'])

    # If only name/surname given
    if len(data) == 2:
        # Seller can be appended immediatily
        plant_shop.sellers.append(new_seller)
        response_data = {
            'id': new_seller.id,
            'name': new_seller.name,
            'surname': new_seller.surname
        }
        return jsonify(response_data), 201, {"location": f"/sellers/{new_seller.id}"}

    # If 'workplace_id' is found in request body
    if len(data) == 3 and 'workplace_id' in data:
        workplace = wp.get_workplace(data['workplace_id'])

        # Check if workplace exists with given id
        if workplace is None:
            return jsonify({"error": "Workplace not found by given id"}), 404

        # If error occured while trying to get response from workplace service
        if 'error' in workplace:
            return jsonify(workplace), 503

        # Set workplace id
        new_seller.workplace_id = data['workplace_id']
        plant_shop.sellers.append(new_seller)
        response_data = {
            'id': new_seller.id,
            'name': new_seller.name,
            'surname': new_seller.surname,
            'workplace_id': new_seller.workplace_id
        }
        return jsonify(response_data), 201, {"location": f"/sellers/{new_seller.id}"}

    # If 'workplace' is found in request body
    if len(data) == 3 and 'workplace' in data:

        # Check if 'workplace' is dict
        if type(data['workplace']) is not dict:
            return jsonify({'error': 'Field workplace is not dictionary type'}), 400

        # Check if JSON object contains the required fields
        if not all(field in data['workplace'] for field in ['companyName', 'description',
                                                            'industry', 'website', 'specialities']):
            return jsonify({'error': 'Some fields are missing to create new workplace'}), 400

        # data['workplace'] must be made exactly from 5 keys
        if len(data['workplace']) == 5:
            new_workplace = wp.create_workplace(data['workplace'])

            if new_workplace is None:
                # Should never happen
                return jsonify({'message': 'Workplace cant be created'}), 400

            # If error occured while trying to get response from workplace service
            if 'error' in new_workplace:
                return jsonify(new_workplace), 503

            # Set workplace id to new seller
            new_seller.workplace_id = new_workplace['_id']

            # Make response
            plant_shop.sellers.append(new_seller)
            response_data = {
                'id': new_seller.id,
                'name': new_seller.name,
                'surname': new_seller.surname,
                'workplace_id': new_seller.workplace_id,
                'workplace': new_workplace
            }
            return jsonify(response_data), 201, {"location": f"/sellers/{new_seller.id}"}
        else:
            return jsonify({'error': 'Wrong json, not required additional fields found'}), 400


@app.post('/plants/<int:plant_id>/sellers')
def add_seller_to_plant(plant_id):
    data = request.get_json()

    plant = plant_shop.get_plant_by_id(plant_id)
    # Check if plant exists
    if not plant:
        message = "Plant not found"
        return jsonify({"error": message}), 404

    # Check if data is valid
    if not all(key in data for key in ('id', 'name', 'surname')):
        message = "Bad request, incorrect seller object given"
        return jsonify({"error": message}), 400

    # Check if seller exists in plant's sellers list
    if plant.find_seller(data['id']):
        message = "Bad request, seller already exists on plant's sellers list with given id"
        return jsonify({"error": message}), 400

    # Check if seller exists in plant_shop.sellers
    seller = plant_shop.get_seller_by_id(data['id'])

    # If no workplace id provided in request body:
    if len(data) == 3:
        if not seller or seller.name != data['name'] or seller.surname != data['surname']:
            message = "Seller not found"
            return jsonify({"error": message}), 404
    elif len(data) == 4:
        if not seller or seller.name != data['name'] or seller.surname != data['surname']\
                or seller.workplace_id != data['workplace_id']:
            message = "Seller not found"
            return jsonify({"error": message}), 404
    else:
        message = "Request body json is not correct, more fields than required"
        return jsonify({"error": message}), 400

    # Add seller to plant's sellers list
    plant.sellers.append(seller)
    return jsonify(seller.__dict__()), 201, {"location": f"/sellers/{seller.id}"}


# HTTP PUT method functions
@app.put('/plants/<int:plant_id>')
def update_plant(plant_id):
    data = request.get_json()

    # Check if id is provided in json
    # And check if id in json is matching with id from argument plant_id
    if len(data) == 4 and 'id' in data:
        if data['id'] != plant_id:
            message = "Bad request, ids are not matching"
            return jsonify({"error": message}), 400
        del data['id']

    # Validation
    if len(data) != 3 or 'name' not in data or 'type' not in data or 'sellers' not in data:
        message = "Bad request, incorrect plant object given"
        return jsonify({"error": message}), 400

    # Check if sellers exists in plant_shop.sellers
    seller_ids = {seller.id for seller in plant_shop.sellers}
    if not all(seller['id'] in seller_ids for seller in data['sellers']):
        message = "Seller is not found in plant_shop"
        return jsonify({"Failure": message}), 404

    # Get plant by id
    plant = plant_shop.get_plant_by_id(plant_id)

    # Convert to sellers dict list to sellers objects list
    sellers_objs = plant_shop.from_dict_to_sellers_objects(data['sellers'])

    # If new plant is added
    if plant is None:
        # Append new plant to the list
        new_plant = pl.Plant(data['name'], data['type'], sellers_objs)
        new_plant.id = plant_id
        plant_shop.plants.append(new_plant)
        # If id in endpoint was higher than current static plant id
        if new_plant.id > pl.Plant.static_plant_id:
            pl.Plant.static_plant_id = new_plant.id + 1
        return jsonify(data), 201, {"location": f"/plants/{plant_id}"}

    else:
        # Update existing plant
        plant.name = data['name']
        plant.type = data['type']
        plant.sellers = sellers_objs
        return jsonify(data), 200, {"location": f"/plants/{plant_id}"}


@app.put('/sellers/<int:seller_id>')
def update_seller(seller_id):
    data = request.get_json()

    # Remove seller id from request body
    if 'id' in data:
        if data['id'] != seller_id:
            message = "Bad request, ids are not matching"
            return jsonify({"error": message}), 400
        del data['id']

    # Validation
    if len(data) != 3 or 'name' not in data or 'surname' not in data or 'workplace_id' not in data:
        message = "Bad request, incorrect seller object given"
        return jsonify({"error": message}), 400

    # Get seller by id
    seller = plant_shop.get_seller_by_id(seller_id)

    # Deal with workplace id
    if data['workplace_id'] is not None:
        # Workplace service stuff
        workplace = wp.get_workplace(data['workplace_id'])

        # Check if workplace exists with given id
        if workplace is None:
            return jsonify({"error": "Workplace not found by given id"}), 404

        # If error occured while trying to get response from workplace service
        if 'error' in workplace:
            return jsonify(workplace), 503
        workplace_id = data['workplace_id']
    else:
        workplace_id = None

    # If new seller is added
    if seller is None:
        # Append new seller to the list
        new_seller = sl.Seller(data['name'], data['surname'])
        new_seller.id = seller_id

        # Update workplace id
        new_seller.workplace_id = workplace_id

        plant_shop.sellers.append(new_seller)
        # If id in endpoint was higher than current static seller id
        if new_seller.id > sl.Seller.static_seller_id:
            sl.Seller.static_seller_id = new_seller.id + 1
        return jsonify(data), 201, {"location": f"/sellers/{seller_id}"}

    else:
        # Update existing seller
        seller.name = data['name']
        seller.surname = data['surname']
        # Update workplace id
        seller.workplace_id = workplace_id
        return jsonify(data), 200, {"location": f"/sellers/{seller_id}"}


@app.put('/plants/<int:plant_id>/sellers/<int:seller_id>')
def update_plant_seller(plant_id, seller_id):
    data = request.get_json()

    # Remove seller id from request body
    if 'id' in data:
        if data['id'] != seller_id:
            message = "Bad request, seller ids are not matching"
            return jsonify({"error": message}), 400
        del data['id']

    # Get plant
    plant = plant_shop.get_plant_by_id(plant_id)

    # Check if plant exists
    if plant is None:
        message = "Plant is not found"
        return jsonify({"error": message}), 404

    # Get seller from plant's sellers
    seller = plant.find_seller(seller_id)

    # Check if seller exists in plant's sellers list
    if seller is None:
        message = "Seller is not found in plant_shop"
        return jsonify({"error": message}), 404

    if len(data) != 3 or 'name' not in data or 'surname' not in data or 'workplace_id' not in data:
        message = "Bad request, incorrect seller object given"
        return jsonify({"error": message}), 400

    # Deal with workplace id
    if data['workplace_id'] is not None:
        # Workplace service stuff
        workplace = wp.get_workplace(data['workplace_id'])

        # Check if workplace exists with given id
        if workplace is None:
            return jsonify({"error": "Workplace not found by given id"}), 404

        # If error occured while trying to get response from workplace service
        if 'error' in workplace:
            return jsonify(workplace), 503
        workplace_id = data['workplace_id']
    else:
        workplace_id = None

    # Update seller in plant's sellers list
    seller.name = data['name']
    seller.surname = data['surname']
    seller.workplace_id = workplace_id
    return jsonify(data), 200, {"location": f"/plants/{plant_id}/sellers/{seller_id}"}


# HTTP Delete method functions
@app.delete('/plants/<int:plant_id>')
def delete_plant(plant_id):
    plant = plant_shop.get_plant_by_id(plant_id)
    if plant is None:
        message = "Plant is not found"
        return jsonify({"error": message}), 404

    plant_shop.plants.remove(plant)
    message = "Plant deleted successfully"
    return jsonify({"success": message}), 204, {"location": f"/plants/{plant_id}"}


@app.delete('/sellers/<int:seller_id>')
def delete_seller(seller_id):
    seller = plant_shop.get_seller_by_id(seller_id)
    if seller is None:
        message = "Seller is not found"
        return jsonify({"error": message}), 404

    # Delete this seller from plants sellers list
    for plant in plant_shop.plants:
        if plant.find_seller(seller.id) is not None:
            plant.sellers.remove(seller)

    plant_shop.sellers.remove(seller)
    message = "Seller deleted successfully"
    return jsonify({"success": message}), 204, {"location": f"/sellers/{seller_id}"}


@app.delete('/plants/<int:plant_id>/sellers/<int:seller_id>')
def delete_plant_seller(plant_id, seller_id):
    # Find plant in plant_shop
    plant = plant_shop.get_plant_by_id(plant_id)
    if plant is None:
        message = "Plant is not found"
        return jsonify({"error": message}), 404

    # Find seller in plant's sellers list
    seller = plant.find_seller(seller_id)
    if seller is None:
        message = "Seller is not found"
        return jsonify({"error": message}), 404

    # Remove seller from plant's sellers list
    plant.sellers.remove(seller)
    message = "Seller deleted successfully from plant's sellers list"
    return jsonify({"success": message}), 204, {"location": f"/plants/{plant_id}/sellers/{seller_id}"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
