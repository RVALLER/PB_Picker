import tkinter as tk
import random
import time


def generate_orbs(canvas):
    global white_circles, gold_circle, white_circles_needing_numbers
    radius = 20

    # Create white circles without numbers
    white_circles = {}
    white_circles_needing_numbers = []
    for _ in range(5):
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)

        circle_id = canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="white"
        )
        dx = random.uniform(-5, 5)  # Increase speed by changing the range
        dy = random.uniform(-5, 5)
        white_circles[circle_id] = (x, y, dx, dy)
        white_circles_needing_numbers.append(circle_id)

    # Create the gold circle without a number
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)

    gold_circle = canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill="#de3f35"
    )
    dx = random.uniform(-5, 5)  # Increase speed by changing the range
    dy = random.uniform(-5, 5)
    white_circles[gold_circle] = (x, y, dx, dy)  # Add gold circle to white_circles

    # Start the animation immediately
    animate_orbs(canvas, time.time())


def animate_orbs(canvas, start_time):
    global white_circles, gold_circle, gold_circle_movement, white_circles_needing_numbers
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time < 4.0:  # Continue animation for 4 seconds
        for circle_id in list(white_circles.keys()):
            x, y, dx, dy = white_circles[circle_id]
            canvas.move(circle_id, dx, dy)
            x1, y1, x2, y2 = canvas.coords(circle_id)
            if x1 < 0 or x2 > WIDTH:
                dx = -dx
            if y1 < 0 or y2 > HEIGHT:
                dy = -dy
            canvas.move(circle_id, dx, dy)
            white_circles[circle_id] = (x, y, dx, dy)

        if gold_circle in white_circles:
            # Update the gold circle's position
            x, y, dx, dy = white_circles[gold_circle]
            canvas.move(gold_circle, dx, dy)
            x1, y1, x2, y2 = canvas.coords(gold_circle)
            if x1 < 0 or x2 > WIDTH:
                dx = -dx
            if y1 < 0 or y2 > HEIGHT:
                dy = -dy
            canvas.move(gold_circle, dx, dy)
            white_circles[gold_circle] = (x, y, dx, dy)

            # Update the gold circle's movement
            gold_dx, gold_dy = gold_circle_movement
            canvas.move(gold_circle, gold_dx, gold_dy)
            x1, y1, x2, y2 = canvas.coords(gold_circle)
            if x1 < 0 or x2 > WIDTH:
                gold_dx = -gold_dx
            if y1 < 0 or y2 > HEIGHT:
                gold_dy = -gold_dy
            canvas.move(gold_circle, gold_dx, gold_dy)
            gold_circle_movement = (gold_dx, gold_dy)
        else:
            # Handle the case where gold_circle is not in white_circles
            pass

        canvas.after(50, animate_orbs, canvas, start_time)  # Continue animation
    else:
        # Conditional check to verify the gold circle is in white_circles
        if gold_circle in white_circles:
            # Continue moving gold circle until numbers are imprinted
            x, y, dx, dy = white_circles[gold_circle]
            canvas.move(gold_circle, dx, dy)
            x1, y1, x2, y2 = canvas.coords(gold_circle)
            if x1 < 0 or x2 > WIDTH:
                dx = -dx
            if y1 < 0 or y2 > HEIGHT:
                dy = -dy
            canvas.move(gold_circle, dx, dy)
            white_circles[gold_circle] = (x, y, dx, dy)

            # Imprint the gold number
            x, y, _dx, _dy = canvas.coords(gold_circle)
            x1, y1, _x2, _y2 = canvas.coords(gold_circle)  # Get the final position of the gold circle
            text_x = (x1 + _x2) / 2  # Calculate the center of the gold circle
            text_y = (y1 + _y2) / 2
            gold_number_text = canvas.create_text(text_x, text_y, text="", font=("Arial", 14))
            canvas.itemconfig(gold_number_text, text=str(random.randint(1, 25)))

            # Remove the gold circle from white_circles
            del white_circles[gold_circle]

        # Call the function to imprint numbers for white circles
        imprint_numbers(canvas)


# Function to imprint numbers on circles
def imprint_numbers(canvas):
    global white_circles, gold_circle, white_circles_needing_numbers
    for circle_id in white_circles_needing_numbers:
        x, y, _dx, _dy = white_circles[circle_id]
        x1, y1, _x2, _y2 = canvas.coords(circle_id)  # Get the final position of the circle
        text_x = (x1 + _x2) / 2  # Calculate the center of the circle
        text_y = (y1 + _y2) / 2
        number_text = canvas.create_text(text_x, text_y, text="", font=("Arial", 14))
        canvas.itemconfig(number_text, text=str(random.randint(1, 70)))

    if gold_circle in white_circles:
        # Imprint the gold number
        x, y, _dx, _dy = canvas.coords(gold_circle)
        x1, y1, _x2, _y2 = canvas.coords(gold_circle)  # Get the final position of the gold circle
        text_x = (x1 + _x2) / 2  # Calculate the center of the gold circle
        text_y = (y1 + _y2) / 2
        gold_number_text = canvas.create_text(text_x, text_y, text="", font=("Arial", 14))
        canvas.itemconfig(gold_number_text, text=str(random.randint(1, 25)))


if __name__ == '__main__':
    # At the beginning of the script
    gold_circle_movement = (random.uniform(-2, 2), random.uniform(-2, 2))

    # Create the main application window
    root = tk.Tk()
    root.title("Speculate Powerball Numbers")

    # Set the canvas dimensions
    WIDTH = 800
    HEIGHT = 600
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#f0d7d1")
    canvas.grid(row=0, column=0, columnspan=2)  # Place the canvas in the first row and span two columns

    # Add a button to generate random circles
    generate_button = tk.Button(root, bg="#cfcdcc", width=20, height=1, text="Generate Winning Numbers",
                                command=lambda: generate_orbs(canvas))
    generate_button.grid(row=1, column=0, padx=(10, 5), pady=10)  # Reduced horizontal padding

    # Add a Clear Canvas Button
    gen_clear = tk.Button(root, bg="#cfcdcc", width=20, height=1, text="Clear Canvas",
                          command=lambda: canvas.delete("all"))
    gen_clear.grid(row=1, column=1, padx=(5, 10), pady=10)  # Reduced horizontal padding

    white_circles = {}  # Store information about white circles
    gold_circle = None  # Store information about the gold circle

    root.mainloop()

    # Call the function to imprint numbers after the mainloop has finished
    imprint_numbers(canvas)
