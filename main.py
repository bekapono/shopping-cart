'''
    this python file will be a monolith for a e-commerce shopping cart
    the main entities will include: products, cart
'''
from collections import defaultdict
from types import MappingProxyType


class Validator:
    @staticmethod
    def is_non_empty_string(input:any) -> bool:
        return isinstance(input,str) and len(input) > 0

    
    @staticmethod
    def is_float(input:any) -> bool:
        return isinstance(input,float)

    @staticmethod
    def valid_qty_to_remove(in_cart_qty:int, qty_to_remove:int) -> bool:
        return in_cart_qty >= qty_to_remove

class Products:
    def __init__(self, name:str, price:float):
        self.__id = 0 # placeholder until import uuid package
        self.__name = name 
        self.__price = price 
        # for now i'll just be working with product name and price.

    def get_name(self) -> str:
        return self.__name # strings is immutable for python

    def get_price(self) -> float:
        return self.__price # float is immutable for python

class GenerateProductsObject:

    @classmethod
    def generate_product_object(self, user_input_name:any, user_input_price:any) -> Products:
        if not Validator.is_non_empty_string(user_input_name):
            raise Exception('The name that was inputted was not a string.')

        if not Validator.is_float(user_input_price):
            raise Exception('The price inputted was not a float.')

        product_name = user_input_name
        product_price = user_input_price

        return Products(product_name, product_price)

class Cart:
    def __init__(self):
        self.__cart_id = 0
        self.__cart = defaultdict(int)

    def get_cart(self) -> MappingProxyType: # Creates a read only view of map.
        return MappingProxyType(self.__cart)

    def add_to_cart(self, product:Product, qty:int):
        self.__cart[product] += qty

    def remove_from_cart(self, product:Product, qty:int):
        if valid_qty_to_remove(self.__cart[product], qty):
            raise Exception('Invalid quantity amount.')
        self.__cart[product] -= qty

class CalculateCart:
    def __init__(self, cart:Cart):
        self.__cart = cart
    
    @property
    def total_cost(self):
        __total = 0 
        for product in self.cart:
            __total += self.cart[product]

        return __total

class Receipt:
    def __init__(self, cart:Cart):
        self.__cart = cart

    def display_recipt(self):
        for product in self.cart:



# start function
name = "Soda"
price = 12.01

item1 = GenerateProducts()
item1 = GenerateProducts.generate_product_object(name,price)
print('item1: ', item1.get_name(), item1.get_price())

item2 = GenerateProducts.generate_product_object(12.01, 12.01)
item3 = GenerateProducts.generate_product_object("Rice", "Rice")
