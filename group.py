from person import Person
from expense import Expense

class Group:
    def __init__(self):
        self.people = {}
        self.expenses = []
    
    def add_person(self, name):
        if name not in self.people:
            self.people[name] = Person(name)
            print(f" Added {name}")
        else:
            print(f"  {name} already exists")
    
    def add_expense(self, description, amount, paid_by, split_with=None):
        if paid_by not in self.people:
            print(f" {paid_by} not in group")
            return
        
        split_list = split_with or list(self.people.keys())
        expense = Expense(description, amount, paid_by, split_list)
        expense.apply_to_balances(self.people)
        self.expenses.append(expense)
        print(f" Added: {expense}")
    
    def show_balances(self):
        print("\n BALANCES:")
        print("-" * 40)
        for person in sorted(self.people.values(), key=lambda p: p.balance, reverse=True):
            status = "owes" if person.balance < 0 else "is owed"
            print(f"{person.name:12} {person} ({status} ${abs(person.balance):.2f})")
    
    def settle_debts(self):
        print("\n🔄 SETTLEMENT:")
        print("-" * 40)
        people_list = sorted(self.people.values(), key=lambda p: p.balance, reverse=True)
        i, j = 0, len(people_list) - 1
        
        while i < j:
            debtor = people_list[j]
            creditor = people_list[i]
            if debtor.balance >= 0 or creditor.balance <= 0:
                break
            transfer = min(abs(debtor.balance), creditor.balance)
            print(f"{creditor.name} ← ${transfer:.2f} ← {debtor.name}")
            creditor.update_balance(-transfer)
            debtor.update_balance(transfer)
            i += 1 if creditor.balance <= 0 else 0
            j -= 1 if debtor.balance >= 0 else 0
    
    def to_dict(self):
        return {
            "people": {name: p.to_dict() for name, p in self.people.items()},
            "expenses": [e.to_dict() for e in self.expenses]
        }
    
    @classmethod
    def from_dict(cls, data):
        group = cls()
        for name, person_data in data["people"].items():
            group.people[name] = Person.from_dict(person_data)
        for expense_data in data["expenses"]:
            expense = Expense.from_dict(expense_data)
            expense.apply_to_balances(group.people)
            group.expenses.append(expense)
        return group