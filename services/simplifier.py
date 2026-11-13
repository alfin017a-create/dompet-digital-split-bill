# Kontribusi modul oleh Jonathan Jovin (251110105)
from models.group import Group

class DebtSimplifier:
    def __init__(self, group: Group):
        self._group = group

    def simplify_debts(self) -> list:
        members = self._group.get_members()
        if not members:
            return []
        
        split = self._group.calculate_flat_split()
        balances = {m.get_username(): 0.0 for m in members}
        
        for exp in self._group._expenses:
            payer_name = exp.get_payer().get_username()
            amount = exp.get_amount()
            balances[payer_name] += amount
            
            per_person = split.get(payer_name, 0.0)
            for m in members:
                balances[m.get_username()] -= per_person

        summary = []
        for name, bal in balances.items():
            if bal < 0:
                summary.append(f"• {name} harus membayar utang sebesar Rp{abs(bal):,.2f}")
            elif bal > 0:
                summary.append(f"• {name} berhak menerima piutang sebesar Rp{bal:,.2f}")
            else:
                summary.append(f"• {name} lunas (tidak ada utang/piutang)")
                
        return summary
