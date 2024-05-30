class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self) -> str:
        entries_str = ""

        # add title
        padding = "*" * int((30 - len(self.name)) / 2)
        title = f"{padding}{self.name}{padding}\n"
        entries_str += title

        # add entries
        for entry in self.ledger:
            description = entry["description"][:23]
            amount = f"{entry['amount']:.2f}"  # .2f = round float to two decimal places
            line = f"{description}{amount:>{30 - len(description)}}\n"
            entries_str += line

        # add net

        net = f"Total: {self.get_balance()}"
        entries_str += net

        return entries_str

    def deposit(self, amount, description=""):
        entry = {"amount": amount, "description": description}
        self.ledger.append(entry)

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            entry = {"amount": 0 - amount, "description": description}
            self.ledger.append(entry)
            return True
        return False

    def get_balance(self):
        ledger_amounts = [entry["amount"] for entry in self.ledger]
        net = sum(ledger_amounts)
        return net

    def transfer(self, amount, partner):
        if self.withdraw(amount, f"Transfer to {partner.name}"):
            partner.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        ledger_amounts = [entry["amount"] for entry in self.ledger]
        net = sum(ledger_amounts)
        if amount > net:
            return False
        else:
            return True


food = Category("food")
food.deposit(50, "for veges")
food.withdraw(10, "veges")

clothing = Category("clothing")
clothing.deposit(30, "for shirts")
clothing.withdraw(10, "shirts")

food.transfer(10, clothing)


def create_spend_chart(categories):
    bar_str = ""

    # add title
    title = "Percentage spent by category\n"
    bar_str += title

    # add chart
    # x axis values
    # percentage of withdrawls from total withdrawls
    # I think their design considers withdrawls as a result of transfers as spent money
    withdrawls = []
    total_withdrawls = 0

    for category in categories:
        category_withdrawls = 0

        for entry in category.ledger:
            if entry["amount"] < 0:
                category_withdrawls += entry["amount"]

        withdrawls.append((category.name, category_withdrawls))
        total_withdrawls += category_withdrawls

    withdrawl_percentages = [  # convert to %
        (category[0], category[1] / total_withdrawls * 100) for category in withdrawls
    ]

    # y axis
    y_axis = list(range(0, 101, 10))

    # nested for loop
    # round down and compare x // y != 0
    # ex:
    # flt = 33.33333
    # value = 40
    # print(flt // value)

    # add divider

    # add labels

    return bar_str


create_spend_chart([food, clothing])