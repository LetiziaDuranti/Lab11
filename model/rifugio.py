from dataclasses import dataclass


@dataclass(frozen=True)
class Rifugio:
    id: int
    nome: str
    localita: str
    altitudine: int
    capienza: int
    aperto: bool

    # Per permettere l'ordinamento (es. per popolare il dropdown)
    def __lt__(self, other):
        return self.nome < other.nome

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        # Quando stampato (es. print(rifugio) o f"{rifugio}"), restituisce solo il nome e località
        return f"Rifugio {self.nome} ({self.localita})"