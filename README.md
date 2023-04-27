# Plants shop

## How to launch web service 
```git clone```

```cd plants_shop_2```

```git submodule update --init```

```docker-compose build```

```docker-compose up```

## Endpoints
```
/plants
/sellers
/plants/<int:plant_id>
/sellers/<int:seller_id>
/plants/<int:plant_id>/sellers
/plants/<int:plant_id>/sellers/<int:seller_id>
```

## Sample data
### Plant:
```
{   
    "id": 10,
    "name": "Jasmine",
    "type": "Flower",
    "sellers": []
}
```
### Seller:
### Add seller without workplace_id
```
{
    "id": 200,
    "name": "Name200",
    "surname": "Surname200"
}
```

#### Add seller with workplace_id:
```
{
    "id": 200,
    "name": "Name200",
    "surname": "Surname200",
    "workplace_id": 3
}
```

#### Add seller with new workplace (adds workplace and generates new workplace_id)
```
{
    "id": 200,
    "name": "Name200",
    "surname": "Surname200",
    "workplace": {   
        "companyName": "IBM",
        "description": "At IBM, we do more than work. We create. We create as technologists, developers, and engineers. We create with our partners. We create with our competitors. If you're searching for ways to make the world work better through technology and infrastructure, software and consulting, then we want to work with you.",
        "industry": "IT Services and IT Consulting",
        "website": "http://www.ibm.com",
        "specialities": [
            "Cloud",
            "Security"
        ]
    }
}
```

## Use Postman to test HTTP methods:
```https://www.postman.com/```

## Or use terminal tool 'curl' to test HTTP methods


