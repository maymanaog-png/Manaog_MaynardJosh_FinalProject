class Person:
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance
    
    def update_balance(self, amount):
        self.balance += amount
    
    def __str__(self):
        status = "owes" if self.balance < 0 else "is owed"
        return f"{self.name:10} ${self.balance:+.2f} ({status} ${abs(self.balance):.2f})"

class Expense:
    def __init__(self, desc, amount, paid_by, split_with):
        self.desc = desc
        self.amount = amount
        self.paid_by = paid_by
        self.split_with = split_with
        self.share = amount / len(split_with) if split_with else amount
    
    def apply(self, people):
        if self.paid_by in people:
            people[self.paid_by].update_balance(self.amount)
        for name in self.split_with:
            if name in people:
                people[name].update_balance(-self.share)
    
    def __str__(self):
        return f"{self.desc}: ${self.amount:.2f} (paid by {self.paid_by})"

class Group:
    def __init__(self):
        self.people = {}
        self.expenses = []
    
    def add_person(self, name):
        if name not in self.people:
            self.people[name] = Person(name)
            print(f" Added {name}")
            return True
        print(f" {name} exists")
        return False
    
    def add_expense(self, desc, amount, paid_by, split_with=None):
        if paid_by not in self.people:
            print(f" {paid_by} not found!")
            return
        split = split_with or list(self.people.keys())
        exp = Expense(desc, amount, paid_by, split)
        exp.apply(self.people)
        self.expenses.append(exp)
        print(f" {exp}")
    
    def show_balances(self):
        print("\n BALANCES:")
        print("-" * 45)
        if not self.people:
            print("No people yet!")
            return
        for person in sorted(self.people.values(), key=lambda p: p.balance, reverse=True):
            print(person)
    
    def settle(self):
        print("\n SETTLEMENT PLAN:")
        print("-" * 45)
        people_list = sorted(self.people.values(), key=lambda p: p.balance, reverse=True)
        i, j = 0, len(people_list) - 1
        
        while i < j:
            debtor = people_list[j]
            creditor = people_list[i]
            if debtor.balance >= 0 or creditor.balance <= 0: break
            transfer = min(abs(debtor.balance), creditor.balance)
            print(f"{creditor.name} ← ${transfer:.2f} ← {debtor.name}")
            creditor.update_balance(-transfer)
            debtor.update_balance(transfer)
            i += 1 if creditor.balance <= 0 else 0
            j -= 1 if debtor.balance >= 0 else 0

def save_data(group, filename="expenses.json"):
    import json
    data = {
        "people": {n: {"name": p.name, "balance": p.balance} for n, p in group.people.items()},
        "expenses": [{"desc": e.desc, "amount": e.amount, "paid_by": e.paid_by, "split": e.split_with} for e in group.expenses]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("SAVED!")

def load_data():
    import json, os
    if not os.path.exists("expenses.json"): return None
    with open("expenses.json") as f:
        data = json.load(f)
    group = Group()
    for name, pdata in data["people"].items():
        group.people[name] = Person(pdata["name"], pdata["balance"])
    return group

# MAIN PROGRAM
print("EXPENSE SPLITTER LOADED!")
group = load_data() or Group()

while True:
    print("\n" + "="*50)
    print("EXPENSE SPLITTER")
    print("1. Add Person    2. Add Expense")
    print("3. Balances      4. Settle Debts") 
    print("5. Save/Exit     6. SAMPLE DEMO")
    print("0. Exit")
    print("="*50)
    
    choice = input("Choice: ").strip()
    print()
    
    if choice == "6":
        group = Group()
        group.add_person("Alice")
        group.add_person("Bob")
        group.add_person("Charlie")
        group.add_expense("Dinner", 60, "Alice")
        group.add_expense("Groceries", 30, "Bob")
        print("SAMPLE LOADED!")
        input("Press ENTER...")
        
    elif choice == "1":
        name = input("Name: ").strip()
        group.add_person(name)
        input("Press ENTER...")
        
    elif choice == "2":
        print("Expense:")
        desc = input("  Description: ")
        try:
            amt = float(input("  Amount: $"))
            paid = input("  Paid by: ")
            splt = input("  Split (comma/Enter=all): ")
            split_list = [x.strip() for x in splt.split(",")] if splt else None
            group.add_expense(desc, amt, paid, split_list)
        except:
            print("Bad amount!")
        input("Press ENTER...")
        
    elif choice == "3":
        group.show_balances()
        input("Press ENTER...")
        
    elif choice == "4":
        group.settle()
        group.show_balances()
        input("Press ENTER...")
        
    elif choice == "5":
        save_data(group)
        print("Goodbye!")
        break
        
    elif choice == "0":
        print("Bye!")
        break
        
    else:
        print("Type 0-6!")
        input("Press ENTER...")