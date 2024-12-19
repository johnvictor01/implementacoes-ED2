import tkinter as tk
from tkinter import messagebox, ttk
import csv
from time import process_time
listarecentes = []

class Node:
    def __init__(self, problem, solution):
        self.problem = problem
        self.solution = solution
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, problem, solution):
        new_node = Node(problem, solution)
        new_node.next = self.head
        self.head = new_node

    def search_and_transpose(self, problem):
        if self.head:
            if self.head.problem == problem:
                return self.head
            prev = None
            current = self.head
            while current and current.problem != problem:
                prev = current
                current = current.next
            if not current:
                return None
            if prev:
                prev.next = current.next
                current.next = self.head
                self.head = current
                return current
        else:
            return None

    def treeFirstProblem(self):
        global listarecentes 
        current = self.head
        for i in range(3):
            listarecentes.append(current.problem)
            current =  current.next
        return 0

class SudokuApp:
    def __init__(self, root, linked_list):
        self.root = root
        self.linked_list = linked_list
        self.problem_vars = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.solution_vars = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.cpu_time = tk.StringVar(value="Tempo de CPU: 0.000000s")
        self.operations = tk.StringVar(value="Operações: 0")
        self.mostView1 = tk.StringVar(value=".")
        self.mostView2 = tk.StringVar(value=".")
        self.mostView3 = tk.StringVar(value=".")
        self.operations_count = 0
        self.create_widgets()


    def create_widgets(self):
        # Barra de pesquisa
        search_frame = tk.Frame(self.root, pady=10)
        search_frame.pack(fill=tk.X)
        tk.Label(search_frame, text="Problema Sudoku:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 14))
        self.search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        tk.Button(search_frame, text="Procurar", command=self.search_problem, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Tabela do problema
        tk.Label(self.root, text="Problema", font=("Arial", 16, "bold")).pack(pady=5)
        problem_frame = tk.Frame(self.root)
        problem_frame.pack()
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(problem_frame, textvariable=self.problem_vars[i][j], width=2, font=("Arial", 14), justify="center", relief="groove")
                entry.grid(row=i, column=j, padx=2, pady=2)

        # Tabela da solução
        tk.Label(self.root, text="Solução", font=("Arial", 16, "bold")).pack(pady=10)
        solution_frame = tk.Frame(self.root)
        solution_frame.pack()
        for i in range(9):
            for j in range(9):
                label = tk.Label(solution_frame, textvariable=self.solution_vars[i][j], width=2, font=("Arial", 14), relief="solid", bg="white", fg="black", justify="center")
                label.grid(row=i, column=j, padx=2, pady=2)

        # Informações de CPU e operações
        info_frame = tk.Frame(self.root, pady=10)
        info_frame.pack(fill=tk.X)
        tk.Label(info_frame, textvariable=self.cpu_time, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, textvariable=self.operations, font=("Arial", 12)).pack(side=tk.RIGHT, padx=10)

          # Informações de CPU e operações
        info_frame2 = tk.Frame(self.root, pady=10)
        info_frame2.pack(fill=tk.X)
        tk.Label(info_frame2, textvariable=self.mostView1, font=("Arial", 12)).grid(row=0)
        tk.Label(info_frame2, textvariable=self.mostView2, font=("Arial", 12)).grid(row=1)
        tk.Label(info_frame2, textvariable=self.mostView3, font=("Arial", 12)).grid(row=2)
        


    def search_problem(self):
        search_key = self.search_entry.get()
        linked_list.treeFirstProblem()
        if not search_key.isdigit():
            messagebox.showerror("Erro", "O problema deve conter apenas números.")
            return

        self.operations_count += 1
        start_time = process_time()
        result = self.linked_list.search_and_transpose(search_key)
        end_time = process_time()

        if result:
            self.load_problem(result.problem)
            self.load_solution(result.solution)
        else:
            messagebox.showinfo("Não encontrado", "O problema não foi encontrado na lista.")

        # Atualizar as informações de CPU e operações

        self.cpu_time.set(f"Tempo de CPU: {end_time - start_time:.7f}s")
        self.operations.set(f"Operações: {self.operations_count}")


        self.mostView1.set(f"Problema: {listarecentes[0]}")
        self.mostView2.set(f"Problema: {listarecentes[1]}")
        self.mostView3.set(f"Problema: {listarecentes[2]}")

    def load_problem(self, problem):
        for i in range(9):
            for j in range(9):
                self.problem_vars[i][j].set(problem[i * 9 + j] if problem[i * 9 + j] != "0" else "")

    def load_solution(self, solution):
        for i in range(9):
            for j in range(9):
                self.solution_vars[i][j].set(solution[i * 9 + j])


def center_window(root):
    root.update_idletasks()
    width = 400
    height = 600
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

linked_list = LinkedList()


def main():
    # Inicializar a lista encadeada
    counter = 0
    start_time = process_time()

    # Carregar o arquivo CSV
    with open('data\\sudoku.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            problem, solution = row[0], row[1]
            linked_list.insert(problem, solution)
            counter += 1
            if counter % 1_000_000 == 0:
                print(f"\n{counter} inserções concluídas!")
    end_time = process_time()
    print(f"\n\nTempo de CPU para carregar a lista encadeada: {end_time - start_time:.6f} segundos")

    # Iniciar a interface gráfica
    root = tk.Tk()
    root.title("Sudoku Viewer")
    center_window(root)
    app = SudokuApp(root, linked_list)
    root.mainloop()


if __name__ == "__main__":
    main()
    