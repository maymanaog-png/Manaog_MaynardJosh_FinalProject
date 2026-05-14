class Expense:
    def __init__(self, description, amount, paid_by, split_with):
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.split_with = split_with
        self.share = amount / len(split_with) if split_with else amount
    
    def apply_to_balances(self, people_dict):
        if self.paid_by in people_dict:
            people_dict[self.paid_by].update_balance(self.amount)
            for person_name in self.split_with:
                if person_name in people_dict:
                    people_dict[person_name].update_balance(-self.share)
    
    def __str__(self):
        return f"{self.description}: ${self.amount:.2f} (by {self.paid_by})"
    
    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "paid_by": self.paid_by,
            "split_with": self.split_with
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)