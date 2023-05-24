import json, copy, csv, sys
from product import Product
from datetime import datetime
import time


class Penztar:
    def __init__(self, invnetory_file, products_file, nav_export_path) -> None:
        self.products = []
        self.invnetory_file = invnetory_file
        self.products_file = products_file
        self.nav_export_path = nav_export_path
        self.cart = []
        self.out_of_stock_products = 0
        self.total = 0

    def read_inventory(self):
        with open(self.invnetory_file, "r", encoding="utf-8") as file:
            content = csv.DictReader(file)
            for row in content:
                name = row["name"]
                count = row["count"]
                product = Product(name=name, count=count)
                self.products.append(product)

    def read_products(self):
        with open(self.products_file, "r", encoding="utf-8") as file:
            json_content = json.load(file)
            for categotry in json_content:
                # [{'name': 'öngyújtó', 'price': 309}, {'name': 'zsepi', 'price': 499}]
                data_line = json_content[categotry]
                for sub_data in data_line:
                    item_name = sub_data["name"]
                    item_price = sub_data["price"]
                    for product in self.products:
                        product_name = product.get_name
                        if product_name == item_name:
                            product.set_type(categotry)
                            product.set_price(item_price)

        # print(list(map(lambda x: print(x), self.products)))

    def show_available_items(self):
        print("\n========================================="
              "======\nAvailable items:\n------------------"
              "-----------------------------")
        counter = 1
        temp_data = {}
        self.out_of_stock_products = 0
        for product in self.products:
            name = product.get_name
            price = product.get_price
            count = product.get_count
            prod_id = product.get_id

            if int(count) > 1:
                print(f"{counter:>4}.) {name:>15}".ljust(30),f"{count} db, {price} Ft".ljust(15))
                temp_data[counter] = name
                counter += 1
            else:
                self.out_of_stock_products += 1
                print(f"{name:>22}", f"\t\tOUT OF STOCK".ljust(30))
            # counter += 1
        my_space = " "
        print(f"{(len(self.products) + 1) - self.out_of_stock_products:>4}.){my_space:<12}Quit")

        self._main_loop(temp_data)

    def _main_loop(self, temp_data):
        while True:
            choice = input("---------------------------------------"
                           "--------\nChoose a product...")
            if not choice.isdigit():
                print("Type number only...")
                continue
            choice = int(choice)
            if choice < 1 or choice > (len(self.products) + 1) - self.out_of_stock_products:
                print("Type a valid number...")
                continue
            if choice == (len(self.products) + 1) - self.out_of_stock_products:
                print("Quitting...")

                # PRINT PRODUCTS RECIPE
                print("\n=================================\nRECIPE"
                      "\n----------------------------------------------")
                for product in self.cart:
                    name = product.get_name
                    price = product.get_price
                    purchased = product.get_purchased
                    subtotal = price * int(purchased)
                    self.total += subtotal
                    print(f"{name}, {purchased}x, {price} Ft - subtotal: {subtotal}")
                print(f"TOTAL: {self.total} Ft")
                print("----------------------------------------------")
                # print(list(map(lambda x: print(f"{x.get_name}, {x.get_count}x - {x.get_price} Ft, subtotal: "), self.cart)))

                # SAVE NAV EXPORT
                self._save_nav_json()

                # SAVE NEW INVENTORY
                self._save_new_inventory()
                quit()

            chosen_item = temp_data[choice]
            print(f"\n======================\nYou choosed: {chosen_item}"
                  "\n======================")
            
            while True:
                amount_to_buy = input("\n======================================\n"
                                      "How much would you like to buy? ")
                if not amount_to_buy.isdigit():
                    print("Type number only...")
                    continue
                amount_to_buy = int(amount_to_buy)
                if amount_to_buy <= 0:
                    print("Type a valid number...")
                    continue

                print(f"You bought {amount_to_buy}x from {chosen_item}"
                      "\n======================================")
                in_cart = False
                for product in self.products:
                    product_name = product.get_name
                    if product_name == chosen_item:
                        new_product = copy.deepcopy(product)
                        new_product.set_purchased(amount_to_buy)
                        for cart_product in self.cart:
                            if cart_product.get_name == product_name:
                                in_cart = True
                                current_purchased_amount = cart_product.get_purchased
                                new_purchased_amount = current_purchased_amount + amount_to_buy
                                cart_product.set_purchased(new_purchased_amount)
                                current_count = product.get_count
                                new_count = current_count - amount_to_buy
                                product.set_count(new_count)
                                print(product.get_count)
                        if not in_cart:
                            self.cart.append(new_product)
                            current_count = product.get_count
                            new_count = int(current_count) - amount_to_buy
                            product.set_count(new_count)
                
                # print(list(map(lambda x: print(f"{x.get_name}, {x.get_count}x"), self.cart)))
                input("Press a key to continue...")
                self.show_available_items()
                break

    def _save_nav_json(self):
        to_save_json = {
                    "register": "AP00700194",
                    "sum": self.total,
                }
        for product in self.cart:
            product_type = product.get_type
            product_name = product.get_name
            product_purchased = product.get_purchased
            if product_type in to_save_json:
                to_save_json[product_type].append({"name": product_name,
                                                            "amount": product_purchased})
            else:
                to_save_json[product_type] = [{"name": product_name,
                                                       "amount": product_purchased}]
                        

        to_save_json["petrol"] = []

        print("Exporting Nav doc...")

        export_date = datetime.now().strftime("%Y-%M-%d")
        export_hour = datetime.now().strftime("%H-%m-%S")
        export_path = f"{self.nav_export_path}nav_export_{export_date}-{export_hour}.json"
        with open(export_path, "w", encoding="utf-8") as file:
            json_save = json.dumps(to_save_json, ensure_ascii=False)
            file.write(json_save)
        print("Nav doc exported...")

    def _save_new_inventory(self):
        headers = ["name", "count"]
        new_inv_items = []
        for product in self.products:
            product_name = product.get_name
            product_count = product.get_count
            new_inv_dict = {
                        "name": product_name,
                        "count": product_count
                    }
            new_inv_items.append(new_inv_dict)
        with open("new_stock.csv", "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(new_inv_items)

class Stock:
    def __init__(self, stock_file, invnetory_file) -> None:
        self.stock_file = stock_file
        self.invnetory_file = invnetory_file
        self.inventory = self.read_file(self.invnetory_file)
        self.new_inventory = self.read_file(self.stock_file)

    def start_stock(self):
        print(self.inventory)
        print(self.new_inventory)
        self.compare()

    def compare(self):
        print()
        for i in range(len(self.inventory)):
            inv_item = self.inventory[i]
            new_inv_item = self.new_inventory[i]

            inv_item_name = inv_item["name"]
            new_inv_item_name = new_inv_item["name"]
            inv_item_count = int(inv_item["count"])
            new_inv_item_count = int(new_inv_item["count"])

            if inv_item_name == new_inv_item_name:
                diff = abs(inv_item_count - new_inv_item_count)
                if new_inv_item_count < 0:
                    print(f"{inv_item_name:<20} -{diff}!")

                if new_inv_item_count > inv_item_count:
                    print(f"{inv_item_name:<20} +{diff}!")
                if new_inv_item_count < inv_item_count and new_inv_item_count >= 0:
                    print(f"{inv_item_name:<20} {diff}")

    def read_file(self, file_to_read: str) -> list:
        data = []
        with open(file_to_read, "r", encoding="utf-8") as file:
            content = csv.DictReader(file)
            for row in content:
                storage = {
                    "name": "",
                    "count": 0
                }
                name = row["name"]
                count = row["count"]
                storage["name"] = name
                storage["count"] = count

                data.append(storage)
                # product = Product(name=name, count=count)
                # storage.append(product)
        return data

if __name__ == '__main__':
    invnetory_file = "inventory.csv"
    if len(sys.argv) == 3 and sys.argv[1] == "-l":
        stock_file = sys.argv[2]
        # stock_file = "new_stock.csv"
        stock = Stock(stock_file, invnetory_file)
        stock.start_stock()

    else:
        products_file = "products.json"
        nav_export_path = "nav_exports/"
        penztar = Penztar(invnetory_file, products_file, nav_export_path)
        penztar.read_inventory()
        penztar.read_products()
        penztar.show_available_items()
