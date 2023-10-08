import tkinter as tk
import random


def generate_orbs(canvas):
    radius = 20

    # Generate a list of non-repeating random numbers from 1 to 70 (9 numbers)
    white_numbers = random.sample(range(1, 71), 5)

    # Generate a single random number for the gold ball from 1 to 25
    gold_number = None

    while gold_number is None or gold_number in white_numbers:
        gold_number = random.randint(1, 25)

    # Display 9 white numbers on white circles
    for number_select in white_numbers:
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)

        circle_make = canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="white"
        )

        canvas.create_text(x, y, text=str(number_select), font=("Arial", 14))

    # Display the gold number on a yellow circle
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)

    circle_make = canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill="goldenrod"
    )

    canvas.create_text(x, y, text=str(gold_number), font=("Arial", 14))


def generate_random_circles(canvas):
    generate_orbs(canvas)


if __name__ == '__main__':
    # Create the main application window
    root = tk.Tk()
    root.title("Speculate Powerball Numbers")

    # Set the canvas dimensions
    WIDTH = 800
    HEIGHT = 600
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#99b7d1")
    canvas.grid(row=0, column=0, columnspan=2)  # Place the canvas in the first row and span two columns

    # Add a button to generate random circles
    generate_button = tk.Button(root, bg="#9599a6", width=20, height=1, text="Generate Winning Numbers",
                                command=lambda: generate_random_circles(canvas))
    generate_button.grid(row=1, column=0, padx=(10, 5), pady=10)  # Reduced horizontal padding

    # Add a Clear Canvas Button
    gen_clear = tk.Button(root, bg="#9599a6", width=20, height=1, text="Clear Canvas",
                          command=lambda: canvas.delete("all"))
    gen_clear.grid(row=1, column=1, padx=(5, 10), pady=10)  # Reduced horizontal padding

    root.mainloop()
