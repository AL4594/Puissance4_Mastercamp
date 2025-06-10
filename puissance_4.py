import time
import copy

class state():
    def __init__(self, grille=None, joueur="1"):
        if grille is None:
            self.grille = [[' ' for _ in range(12)] for _ in range(6)]
        elif any(
                any(grille[ligne][col] != ' ' and any(grille[l][col] == ' ' for l in range(ligne + 1, 6))
                    for ligne in range(6))
                for col in range(12)
        ):
            print("Grille invalide : pions flottants détectés. Une grille vide sera utilisée.")
            self.grille = [[' ' for _ in range(12)] for _ in range(6)]
        else:
            self.grille = grille
        self.joueur = joueur

    def Terminal_test(self) -> bool:
        return self.gagnant() is not None or all(self.grille[0][col] != ' ' for col in range(len(self.grille[0])))

    def Utility(self, joueur_vise: str) -> int:
        gagnant = self.gagnant()
        if gagnant == joueur_vise:
            return 100000
        elif gagnant and gagnant != joueur_vise:
            return -100000
        else:
            return self.heuristic(joueur_vise)

    def Actions(self, joueur: str) -> list[int]:
        return [col for col in range(len(self.grille[0])) if self.grille[0][col] == ' ']

    def Result(self, col_choice: int, joueur: str) -> "state":
        if self.Terminal_test():
            print("the game is over")
            return None
        if self.grille[0][col_choice] != ' ':
            print("the column is full invalid choice")
            return None
        # on doit check quelle est la ligne la plus basse dans laquelle la piece va tomber dans la colonne choisie et retourner le state apres avoir changé
        lowest_line=next(i for i in range(5,-1,-1) if self.grille[i][col_choice] == ' ')
        grille= copy.deepcopy(self.grille)
        grille[lowest_line][col_choice]=joueur
        return state(grille=grille, joueur=self.Adversaire(joueur))


    def gagnant(self):
        lignes = len(self.grille)
        colonnes = len(self.grille[0])
        for row in range(lignes):
            for col in range(colonnes):
                if self.grille[row][col] == ' ':
                    continue
                joueur = self.grille[row][col]
                if col <= colonnes - 4 and all(self.grille[row][col + i] == joueur for i in range(4)):
                    return joueur
                if row <= lignes - 4 and all(self.grille[row + i][col] == joueur for i in range(4)):
                    return joueur
                if row >= 3 and col <= colonnes - 4 and all(self.grille[row - i][col + i] == joueur for i in range(4)):
                    return joueur
                if row <= lignes - 4 and col <= colonnes - 4 and all(
                        self.grille[row + i][col + i] == joueur for i in range(4)):
                    return joueur
        return None

    def heuristic(self, joueur_vise: str) -> int:
        lignes = len(self.grille)
        colonnes = len(self.grille[0])
        score = 0
        adversaire = self.Adversaire(joueur_vise)

        def eval_line(line):
            count_j = line.count(joueur_vise)
            count_a  = line.count(adversaire)
            if count_j > 0 and count_a == 0:
                return 10 ** count_j
            elif count_a > 0 and count_j == 0:
                return -(10 ** count_a)
            return 0

        for row in range(lignes):
            for col in range(colonnes - 3):
                ligne = [self.grille[row][col + i] for i in range(4)]
                score += eval_line(ligne)

        for col in range(colonnes):
            for row in range(lignes - 3):
                colonne = [self.grille[row + i][col] for i in range(4)]
                score += eval_line(colonne)

        for row in range(3, lignes):
            for col in range(colonnes - 3):
                diag1 = [self.grille[row - i][col + i] for i in range(4)]
                score += eval_line(diag1)

        for row in range(lignes - 3):
            for col in range(colonnes - 3):
                diag2 = [self.grille[row + i][col + i] for i in range(4)]
                score += eval_line(diag2)

        return score

    def Display(self):
        print("\n  " + " ".join(str(i) for i in range(12)))
        for row in self.grille:
            print(" |" + "|".join(self.rendu(cell) for cell in row) + "|")

    def rendu(self, cell: str) -> str:
        if cell == '1':
            return 'X'
        elif cell == '-1':
            return 'O'
        else:
            return ' '

    def Adversaire(self, joueur: str) -> str:
        return "-1" if joueur == "1" else "1"

    def Gagnant(self):
        return self.gagnant()


MAX_DEPTH = 5

def IA_decision(s:"state"):
    def max_value(s: "state", alpha: float, beta: float, depth: int) -> int:
        if s.Terminal_test() or depth == 0:
            return s.Utility(joueur_vise=s.joueur)
        v = float('-inf')
        for action in s.Actions(s.joueur):
            v = max(v, min_value(s.Result(action, s.joueur), alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v


    def min_value(s: "state", alpha: float, beta: float, depth: int) -> int:
        if s.Terminal_test() or depth == 0:
            return s.Utility(joueur_vise=s.joueur)
        v = float('inf')
        for action in s.Actions(s.joueur):
            v = min(v, max_value(s.Result(action, s.joueur), alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


    def alphabeta_decision(s: "state"):
        best_score = float('-inf')
        best_action = None
        alpha = float('-inf')
        beta = float('inf')
        for action in s.Actions(s.joueur):
            value = min_value(s.Result(action, s.joueur), alpha, beta, MAX_DEPTH - 1)
            if value > best_score:
                best_score = value
                best_action = action
            alpha = max(alpha, best_score)
        return best_action
    return(alphabeta_decision(s))


def jouer():
    ok=False
    while ok==False:
        current_mode = input("Choisissez le mode de jeu : (a pour IA vs IA, b pour joueur vs IA, i pour IA vs joueur) : ").lower()
        if current_mode == 'a':
            print("\n--- Mode IA vs IA ---")
            ia1_player = "1"
            ia2_player = "-1"
            s = state(joueur=ia1_player)
            ok=True
        elif current_mode == 'b':
            joueur_humain = "1" if current_mode == 'j' else "-1"
            joueur_ia = "-1" if joueur_humain == "1" else "1"
            s = state(joueur=joueur_humain if current_mode == 'j' else joueur_ia)
            ok=True
        else:
            print("réponse invalide réessayez")


    nb_tours = 0
    s.Display()

    while not s.Terminal_test():
        print(f"\nTour du joueur {'X' if s.joueur == '1' else 'O'}")

        if current_mode == 'a':
            print(f"IA {'X' if s.joueur == '1' else 'O'} réfléchit...")
            start = time.time()
            action = IA_decision(s)
            end = time.time()
            print(f"IA {'X' if s.joueur == '1' else 'O'} a joué la colonne {action} en {end - start:.2f} secondes")
            s = s.Result(action, s.joueur)
        elif s.joueur == joueur_humain:
            valid = False
            while not valid:
                try:
                    col = int(input("Entrez la colonne (0-11) : "))
                    if col in s.Actions(s.joueur):
                        s = s.Result(col, s.joueur)
                        valid = True
                    else:
                        print("Colonne pleine ou invalide.")
                except ValueError:
                    print("Veuillez entrer un entier entre 0 et 11.")
        else:
            print("IA réfléchit...")
            start = time.time()
            action = IA_decision(s)
            end = time.time()
            print(f"L'IA a joué la colonne {action} en {end - start:.2f} secondes")
            s = s.Result(action, s.joueur)

        s.Display()
        nb_tours += 1

    gagnant = s.Gagnant()
    if gagnant:
        print(f"\nLe joueur {'X' if gagnant == '1' else 'O'} a gagné !")
    else:
        print("\nMatch nul.")

    print("Fin de la partie.")


def main():
    """s=state()
        s.display()
        print(s.Actions(joueur="1"))"""

    """s2=state(grille = [
    ['-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1'],
    ['1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1'],
    [' ', ' ', ' ', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' '],
    ['-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1'],
    ['1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1'],
    ['-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1', '-1', '1'],
    ]
    )"""

    """s3 = state(grille=[
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '-1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', '-1', '-1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['1', '-1', '1', '1', '-1', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]
    )
    print(s3.Terminal_test(), s3.Actions(joueur="-1"))
    s3.Result(col_choice=2, joueur="1").Display()"""

    jouer()


if __name__ == '__main__':
    main()
