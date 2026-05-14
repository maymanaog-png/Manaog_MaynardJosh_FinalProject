class Person:
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance
    
    def update_balance(self, amount):
        self.balance += amount
    
    def __str__(self):
        return f"${self.balance:+.2f}"
    
    def to_dict(self):
        return {"name": self.name, "balance": self.balance}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["balance"])