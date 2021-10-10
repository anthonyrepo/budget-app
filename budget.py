class Category:
    def __init__(self, category):
        self.ledger = []
        self.category = category

    def deposit(self, amount, description = ''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = ''):        
        if self.check_funds(amount):
            self.ledger.append({"amount": amount * -1, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance = balance + item["amount"]

        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.ledger.append({"amount": amount * -1, "description": 'Transfer to {}'.format(category.category)})
            category.deposit(amount, 'Transfer from {}'.format(self.category))
            return True
        else:
            return False
    
    def check_funds(self, amount):
        balance = 0
        for item in self.ledger:
            balance = balance + item["amount"]

        if amount > balance:
            return False
        else:
            return True

    def __str__(self):
        title_line = self.category.center(30, '*') + '\n'
        
        expenses = ''
        for item in self.ledger:
            line = item["description"][:23]

            amount = str("{:.2f}".format(item["amount"]))[:7]
            line = line + ''.center(30 - len(line) - len(amount)) + amount + '\n'

            expenses = expenses + line

        total = 'Total: {}'.format("{:.2f}".format(self.get_balance()))

        return title_line + expenses + total

def create_spend_chart(categories):
    money_spent = dict()

    for category in categories:
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                money_spent[category.category] = money_spent.get(category.category, 0) + (transaction["amount"] * -1)

    total = 0
    for item in money_spent.values():
        total = total + item

    for key in money_spent:
        percentage = (money_spent[key] * 100)/total
        money_spent[key] = percentage

    for key in money_spent:
        rounded_percentage = (money_spent[key] // 10) * 10
        money_spent[key] = rounded_percentage

    y_axis = ['100', '90', '80', '70', '60', '50', '40', '30', '20', '10', '0']
    graph = ''

    graph_name = 'Percentage spent by category' + '\n'

    for number in y_axis:
        graph_line = number.rjust(3) + '| '
        for item in money_spent:
            if money_spent[item] >= int(number):
                graph_line = graph_line + 'o  '
            else:
                graph_line = graph_line + '   '

        graph = graph + graph_line + '\n'

    bar_line = '    ' + ''.center(len(money_spent) * 3 + 1, '-') + '\n'

    longest_label = 0
    for key in money_spent:
        if len(key) > longest_label:
            longest_label = len(str(key))

    labels = []
    for key in money_spent.keys():
        labels.append(key.ljust(longest_label))

    x_axis = ''
    for i in range(longest_label):
        x_axis_line = '     '
        
        for label in labels:
            x_axis_line = x_axis_line + label[i].ljust(3)

        x_axis = x_axis + x_axis_line + '\n'

    x_axis = x_axis[:-1]

    return graph_name + graph + bar_line + x_axis