'''
    this python file will be a monolith for a e-commerce shopping cart
    the main entities will include: products, cart
'''
from collections import defaultdict
from types import MappingProxyType
from datetime import datetime
import uuid 

# -------------------- UTILITIES -------------------- #
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

# -------------------- Product Entity -------------------- #
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
    @staticmethod
    def generate_product_object(user_input_name:any, user_input_price:any) -> Products:
        if not Validator.is_non_empty_string(user_input_name):
            raise Exception('The name that was inputted was not a string.')

        if not Validator.is_float(user_input_price):
            raise Exception('The price inputted was not a float.')

        product_name = user_input_name
        product_price = user_input_price

        return Products(product_name, product_price)

# -------------------- CART ENTITY -------------------- #
class Cart:
    def __init__(self):
        self.__cart_id = 0
        self.__cart = defaultdict(int)

    def get_cart(self) -> MappingProxyType: # Creates a read only view of map.
        return MappingProxyType(self.__cart)

    def add_to_cart(self, product:Product, qty:int):
        self.__cart[product] += qty

    def remove_from_cart(self, product:Product, qty:int):
        if Validator.valid_qty_to_remove(self.__cart[product], qty):
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

    def format_recipt(self) -> List[str]:
        lines = []
        total_cost_of_cart = 0
        for product,qty in self.__cart:
            total_cost_for_product = product.get_price() * qty
            lines.append(f"{product.get_name()}: {qty} x ${product.get_price():.2f} = ${total_cost_for_product:.2f}")
            total_cost_of_cart += total_cost_for_product
        lines.append(f"Total cost of cart: {total_cost_of_cart:.2f}")
        return lines

# -------------------- ORDER ENTITY -------------------- #

class OrderStatus(Enum):
    DRAFT =                 "DRAFT"   # not sure if i need this
    PROCESSING_PAYMENT =    "PROCESSING_PAYMENT"
    FAILED_PAYMENT =        "FAILED_PAYMENT"
    PAID =                  "PAID"
    PENDING_SHIPPING =      "PENDING_SHIPPING"
    SHIPPED =               "SHIPPED"
    DELIVERED =             "DELIVERED"
    CANCELLED =             "CANCELLED" # can only be reached prior to payment being completed 
    REFUNDED =              "REFUNDED"  # can only be reached after payment has been made

# Havn't considered if customer is paying but cart ran out of certain products.
class OrderStatusPolicy:
    _allowed = {
            OrderStatus.DEFAULT:                {OrderStatus.PROCESSING_PAYMENT}
            OrderStatus.PROCESSING_PAYMENT:     {OrderStatus.FAILED_PAYMENT, OrderStatus.PAID, OrderStatus.CANCELLED},
            OrderStatus.FAILED_PAYMENT:         {OrderStatus.PROCESSING_PAYMENT, OrderStatus.CANCELLED},
            OrderStatus.PAID:                   {OrderStatus.PENDING_SHIPPING, OrderStatus.REFUNDED}, 
            OrderStatus.PENDING_SHIPPING:       {OrderStatus.SHIPPED, OrderStatus.REFUNDED},
            OrderStatus.SHIPPED:                {OrderStatus.DELIVERED, OrderStatus.REFUNDED},
            OrderStatus.DELIVERED:              {OrderStatus.REFUNDED},
            OrderStatus.CANCELLED:              set(), # Theres a collection, but it's empty set. Versus None would mean we didn't define rules for this set.
            OrderStatus.REFUNDED:               set()
            }

    @classmethod
    def can_transition_to(cls, current: OrderStatus, new: OrderStatus) -> bool:
        return new in cls._allowed.get(current, set())

# need to consider when a Cart is finalized and Order is created?
# once a user clicks checkout? - once a payment is initiated? 
class Order:
    def __init__(self, cart: dict()): # have to check if cart is dict() or dict(int)
        self.__order_id = uuid.uuid4()
        self.__customer_id = uuid.uuid4()
        self.__purchased_items = cart # the Cart object that was passed should be an immutable snapshot of the Order
        self.__datetime = datetime.now()
        self.__order_status: OrderStatus = OrderStatus.DRAFT # Initialize order_status with UNKNOWN as default
    
    @property
    def status(self) -> OrderStatus:
        return self.__order_status

    def change_order_status(self, new_status: OrderStatus) -> None: # Have to consider whether I want stict OrderStatus type or str
        # new_status = OrderStatus[] # not sure if i need this
        if not OrderStatePolicy.can_transition_to(self.__order_status, new_status):
            raise ValueError(f"Cannot go from {self.__order_status} to {new_status}")
        self.__order_status = new_status

    def get_datetime(self) -> datetime:
        return self.__datetime

    def get_purchased_items(self) -> dict():
        return MappingProxyType(self.__purchased_items)

# -------------------- TEMP ENTRY POINT -------------------- # 
def main():
    # start function

if __name__ = __main__:
    main()
