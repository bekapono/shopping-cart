'''
    this python file will be a monolith for a e-commerce shopping cart
    the main entities will include: products, cart
'''

class Validator:
    @staticmethod
    def is_non_empty_string(input:any) -> bool:
        return isinstance(input,str) and len(input) > 0
    
    @staticmethod
    def is_float(input:any) -> bool:
        return isinstance(input,float)

class Products:
    def __init__(self, name:str, price:float):
        self.__id = 0 # placeholder until import uuid package
        self.__name = name 
        self.__price = price 
        # for now i'll just be working with product name and price.

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

class GenerateProducts:

    @classmethod
    def generate_product_object(self, user_input_name:any, user_input_price:any) -> Products:
        if not Validator.is_non_empty_string(user_input_name):
            raise Exception('The name that was inputted was not a string.')

        if not Validator.is_float(user_input_price):
            raise Exception('The price inputted was not a float.')

        product_name = user_input_name
        product_price = user_input_price

        return Products(product_name, product_price)

# start function
name = "Soda"
price = 12.01

item1 = GenerateProducts()
item1 = GenerateProducts.generate_product_object(name,price)
print('item1: ', item1.get_name(), item1.get_price())

item2 = GenerateProducts.generate_product_object(12.01, 12.01)
item3 = GenerateProducts.generate_product_object("Rice", "Rice")
