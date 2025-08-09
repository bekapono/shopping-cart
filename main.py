'''
    this python file will be a monolith for a e-commerce shopping cart
    the main entities will include: products, cart
'''
from collections import defaultdict
from types import MappingProxyType
from datetime import datetime
from typing import Optional, List, Dict, Protocol
from enum import Enum
from abc import ABC, abstractmethod
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
    def invalid_qty_to_remove(in_cart_qty:int, qty_to_remove:int) -> bool:
        return in_cart_qty < qty_to_remove

# -------------------- Product Entity -------------------- #
'''
        Need to look up freezing class state so fields are immutable.
        Also added __eq__ and __hash__ for for comparison check and hash tables have to match 
        - products class is going to be a temp class that will be deleted later, since This
        should really be a repo. with a paired up ProductsService to communicate with it.
'''
class Products:
    def __init__(self, name:str, price:float):
        self.__id = uuid.uuid4() # placeholder until import uuid package
        self.__name = name 
        self.__price = price 
        # for now i'll just be working with product name and price.
    
    @property 
    def id(self) -> uuid.UUID:
        return self.__id 

    @property 
    def name(self) -> str:
        return self.__name # strings is immutable for python
     
    @property
    def price(self) -> float:
        return self.__price # float is immutable for python

    # Equality & hash based only on immutable id 
    def __eq__(self, other):
        if not isinstance(other, Products):
            return NotImplmented
        return self.__id == other.__id

    def __hash__(self):
        return hash(self.__id)

class ProductRepository(ABC):

    @abstractmethod
    def get_by_id(self, product_id:uuid) -> Optional[Products]:
        pass

    @abstractmethod
    def add(self, product:Products) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[Products]:
        pass

# This Factory Method seems more useful as a FRONT-END def.
# rather than a def for the BACK-END.
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
        self.__cart_id = uuid.uuid4()
        self.__cart = defaultdict(int)

    def get_cart(self) -> MappingProxyType: # Creates a read only view of map.
        return MappingProxyType(self.__cart)

    def add_to_cart(self, product:Products, qty:int):
        self.__cart[product] += qty

    def remove_from_cart(self, product:Products, qty:int):
        if Validator.invalid_qty_to_remove(self.__cart[product], qty):
            raise Exception('Invalid quantity amount.')
        self.__cart[product] -= qty

class CalculateCart:
    def __init__(self, cart:Cart):
        self.__cart = cart
    
    @property
    def total_cost(self):
        __total = 0 
        for product, qty in self.__cart.items():
            __total += self.__cart[product].price * self.__cart[product].qty

        return __total

class Receipt:
    def __init__(self, cart:Cart):
        self.__cart = cart

    def format_receipt(self) -> List[str]:
        lines = []
        total_cost_of_cart = 0
        for product,qty in self.__cart.items():
            total_cost_for_product = product.get_price() * qty
            lines.append(f"{product.get_name()}: {qty} x ${product.get_price():.2f} = ${total_cost_for_product:.2f}")
            total_cost_of_cart += total_cost_for_product
        lines.append(f"Total cost of cart: {total_cost_of_cart:.2f}")
        return lines

# -------------------- ORDER ENTITY -------------------- #
class OrderRepository:
    # TEMP IN MEMORY REPO FOR ORDER CRUD
    pass 

class OrderDTO:
    # map from repo -> service 
    pass 


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
            OrderStatus.DRAFT:                {OrderStatus.PROCESSING_PAYMENT}, # Dont need to allow CANCELLED since write to repo wont happen at this point.
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
    def __init__(self, cart_snapshot: Dict[Products, int]): # have to check if cart is dict() or dict(int)
        self.__order_id = uuid.uuid4()
        self.__customer_id = uuid.uuid4()
        self.__purchased_items = cart_snapshot # the Cart object that was passed should be an immutable snapshot of the Order
        self.__datetime = datetime.now()
        self.__order_status: OrderStatus = OrderStatus.DRAFT # Initialize order_status with UNKNOWN as default
    
    @property
    def status(self) -> OrderStatus:
        return self.__order_status

    def change_order_status(self, new_status: OrderStatus) -> None: # Have to consider whether I want stict OrderStatus type or str
        # new_status = OrderStatus[] # not sure if i need this
        if not OrderStatusPolicy.can_transition_to(self.__order_status, new_status):
            raise ValueError(f"Cannot go from {self.__order_status} to {new_status}")
        self.__order_status = new_status

    def get_datetime(self) -> datetime:
        return self.__datetime

    def get_purchased_items(self) -> dict():
        return dict(self.__purchased_items)

# --------------- OTHERS --------------- #

class PaymentService:
    # third party service 
    # did payment go through yes or no?
    # payment service should know the total and order_id how about products?
    pass

class Reservation:
    def __init__(self):
        self.__id = uuid.uuid4()
    
    @property
    def reservation_id(self) -> uuid:
        return self.__id


# purpose that holds the items from the import debugpy, platform
class ProductReservationService:
    '''
        SRP: handles the reserve, release, commit status of products
    '''
    def __init__(self, time_to_live_exiration_time: int, product_repo: ProductRepository): # not sure if I want to pass in ttl during app build, or pass it in later.
        pass

    def reserve(self, cart):
        # Check if all products could be reserved 
        # if yes, 
        return Reservation.reservation_id # it should initialize the object with uuid and return the uuid 

    def release(self):
        pass

    def commit(self):
        # should persist the inventory changes
        pass

 
class CheckoutService:
    '''
        SRP: handles the process from requesting to purchase to delivered.
        - is the binding method between cart <-> order.
        - receive the cart and persists it to a dict()
        - creates and Order object and passes cart_dict
        - checks and reserve products
        - changes orderstatus to payment 
        - calls method to process payment 
    '''
    # concept - dependecy injection : constructor injection 
    # the services are infrastrure dependencies
    def __init__(
            self,
            reservation_service:ProductReservationService,
            payment_service:PaymentService,
            order_repo:OrderRepository,
        ):
        self.__reservation_service = reservation_service
        self.__payment_service = payment_service
        self.__order_repo = order_repo

    def checkout(self, cart, customer_info):
        # validate cart, snapshot items/total_cost_of_cart
        # reserve -> create order -> pay -> commit/release -> update status 

        # to validate cart we need to check in the repository if the products exists
        if not self.__reservation_service.reserve(cart): # temp solution forcing dict(cart)
            raise Exception('Not all products could be reserved')

        # then if exists we need to create an Order object
        order = Order(dict(cart))
        
        # call PaymentService
        order.change_order_status(OrderStatus.PROCESSING_PAYMENT)

        if not self.payment_service.process_payment(customer_info):
            order.change_order_status(FAILED_PAYMENT)
            raise Exception('Payment not successful.')

        order.change_order_status(OrderStatus.PAID)
        self.__reservation_service.commit(self.__reservation_service.reservation_id) # temp solution where do I store the temp reservation 
        order.change_order_status(OrderStatus.PENDING_SHIPPING)
        # FUTURE ENHANCEMENT - NotificationService to send email with receipt 
        # done



# -------------------- TEMP ENTRY POINT -------------------- # 
def main():
    # 1. Create products
    # 2. Add products to cart
    # 3. Display cart
    # 4. checkout
    # 5. Simulation
    # 6. Print receipt

if __name__ == "__main__":
    main()
