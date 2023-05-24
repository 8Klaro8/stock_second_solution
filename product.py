class Product:
    id = 0
    def __init__(self, name=None, price=None, count=None, type=None) -> None:
        self.__name = name
        self.__price = price
        self.__count = count
        self.__type = type
        self.__purchased = 0
        self.__product_id = Product.id
        self.increase_id()

    def increase_id(self):
        Product.id += 1

    @property
    def get_id(self):
        return self.__product_id
    @property
    def get_purchased(self):
        return self.__purchased
    def set_purchased(self, purchased):
        self.__purchased = purchased
    @property
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    @property
    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price
    @property
    def get_count(self):
        return self.__count
    def set_count(self, count):
        self.__count = count
    @property
    def get_type(self):
        return self.__type
    def set_type(self, type):
        self.__type = type

    def __str__(self):
        return f"\n===============================\n" \
                f"NAME:{self.get_name}\nPRICE:{self.get_price}" \
                f"\nCOUNT:{self.get_count}\nTYPE:{self.get_type}" \
                f"\nPRODUCT_ID: {self.__product_id}\nPURCHASED: {self.get_purchased}"\
                f"\n===============================\n"

