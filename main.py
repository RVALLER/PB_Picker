import tkinter as tk
import random
import time
from PIL import Image, ImageTk

# Global variables
background_image = None
canvas = None
white_circles = {}
gold_circle = None
white_circles_needing_numbers = []

# Set your desired canvas width and height
WIDTH = 750
HEIGHT = 500

current_drawing_color = "white"
single_balls = []


def generate_orbs(can):
    global white_circles, gold_circle, white_circles_needing_numbers  # Add white_circles_needing_numbers to the
    # global scope
    radius = 20

    white_circles = {}
    white_circles_needing_numbers = []

    unique_white_numbers = set()
    while len(unique_white_numbers) < 5:
        number = random.randint(1, 69)
        unique_white_numbers.add(number)

    unique_white_numbers_list = list(unique_white_numbers)

    for i in range(5):
        x = random.randint(radius, WIDTH - radius)
        y = random.randint(radius, HEIGHT - radius)

        circle_id = can.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="white"
        )
        dx = random.uniform(-5, 5)
        dy = random.uniform(-5, 5)
        white_circles[circle_id] = (x, y, dx, dy)
        white_circles_needing_numbers.append((circle_id, unique_white_numbers_list[i]))

    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)

    gold_circle = can.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill="#de3f35"
    )
    dx = random.uniform(-5, 5)
    dy = random.uniform(-5, 5)
    white_circles[gold_circle] = (x, y, dx, dy)

    animate_orbs(can, time.time())


def clear_canvas():
    canvas.delete("all")
    if background_image:
        canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    white_circles.clear()
    for circle_id, number in white_circles_needing_numbers:
        x1, y1, x2, y2 = canvas.coords(circle_id)
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2
        number_text = canvas.create_text(text_x, text_y, text="", font=("Arial", 14))
        canvas.itemconfig(number_text, text=str(number))


def animate_orbs(can, start_time):
    global white_circles, gold_circle
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time < 2.5:
        for circle_id in list(white_circles.keys()):
            x, y, dx, dy = white_circles[circle_id]
            can.move(circle_id, dx, dy)
            x1, y1, x2, y2 = can.coords(circle_id)

            if x1 < 0 or x2 > WIDTH:
                dx = -dx
            if y1 < 0 or y2 > HEIGHT:
                dy = -dy
            can.move(circle_id, dx, dy)
            white_circles[circle_id] = (x, y, dx, dy)

        if gold_circle in white_circles:
            x, y, dx, dy = white_circles[gold_circle]
            can.move(gold_circle, dx, dy)
            x1, y1, x2, y2 = can.coords(gold_circle)

            if x1 < 0 or x2 > WIDTH:
                dx = -dx
            if y1 < 0 or y2 > HEIGHT:
                dy = -dy
            can.move(gold_circle, dx, dy)
            white_circles[gold_circle] = (x, y, dx, dy)

        can.after(7, animate_orbs, can, start_time)
    else:
        if gold_circle in white_circles:
            x, y, dx, dy = white_circles[gold_circle]
            can.move(gold_circle, dx, dy)
            x1, y1, x2, y2 = can.coords(gold_circle)

            if x1 < 0 or x2 > WIDTH:
                dx = -dx
            if y1 < 0 or y2 > HEIGHT:
                dy = -dy
            can.move(gold_circle, dx, dy)
            white_circles[gold_circle] = (x, y, dx, dy)

            # Imprint the number on the red orb when it stops moving
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            number = random.randint(1, 26)
            number_text = can.create_text(text_x, text_y, text="", font=("Arial", 14))
            can.itemconfig(number_text, text=str(number))

        imprint_numbers(can)


def show_rules():
    rules_text = """
    Powerball Rules:

    1. Choose 5 white numbers from 1 to 69.
    2. Choose 1 red Powerball number from 1 to 26.
    3. Matching all 5 white numbers and the Powerball number wins the jackpot.
    4. Prizes are also awarded for matching fewer numbers.
    """

    popup = tk.Toplevel()
    popup.title("Powerball Rules")

    rules_label = tk.Label(popup, text=rules_text)
    rules_label.pack(padx=20, pady=20)


def show_mock_winners():
    i = random.randint(1, 69)
    ii = random.randint(1, 69)
    iii = random.randint(1, 69)
    iv = random.randint(1, 69)
    v = random.randint(1, 26)
    winners_text = f"""
    Today's Winning Numbers are: 
    {i}, {ii}, {iii}, {iv} and the powerball of {v}
    """
    popup = tk.Toplevel()
    popup.title("Today's Winning Numbers: ")

    rules_label = tk.Label(popup, text=winners_text)
    rules_label.pack(padx=20, pady=20)


def add_single_ball():
    global current_drawing_color
    radius = 20

    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    color = current_drawing_color
    circle_id = canvas.create_oval(
        x - radius,
        y - radius,
        x + radius,
        y + radius,
        fill=color
    )

    dx = random.uniform(-5, 5)
    dy = random.uniform(-5, 5)

    if current_drawing_color == "white":
        number = random.randint(1, 69)
    else:
        number = random.randint(1, 26)

    start_time = time.time()
    single_ball = {'circle_id': circle_id, 'color': color, 'dx': dx, 'dy': dy, 'number': number, 'moving': True,
                   'start_time': start_time}
    single_balls.append(single_ball)

    animate_single_ball(canvas, single_ball)


def animate_single_ball(can, single_ball):
    if single_ball['moving']:
        circle_id = single_ball['circle_id']
        x1, y1, x2, y2 = can.coords(circle_id)

        if x1 < 0 or x2 > WIDTH:
            single_ball['dx'] = -single_ball['dx']
        if y1 < 0 or y2 > HEIGHT:
            single_ball['dy'] = -single_ball['dy']

        can.move(circle_id, single_ball['dx'], single_ball['dy'])

        if time.time() - single_ball['start_time'] >= 4:
            single_ball['moving'] = False

        if not single_ball['moving']:
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            number_text = can.create_text(text_x, text_y, text="", font=("Arial", 14))
            can.itemconfig(number_text, text=str(single_ball['number']))

            # Remove the 'moving' flag to prevent further animation
            single_ball['moving'] = False

    if single_ball['moving']:
        can.after(7, animate_single_ball, can, single_ball)


def imprint_numbers(can):
    for circle_id, number in white_circles_needing_numbers:
        x1, y1, x2, y2 = can.coords(circle_id)
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2
        number_text = can.create_text(text_x, text_y, text="", font=("Arial", 14))
        can.itemconfig(number_text, text=str(number))


def toggle_drawing_color():
    global current_drawing_color
    if current_drawing_color == "white":
        current_drawing_color = "red"
    else:
        current_drawing_color = "white"


if __name__ == '__main__':
    gold_circle_movement = (random.uniform(-2, 2), random.uniform(-2, 2))

    root = tk.Tk()
    root.title("Speculate Powerball Numbers")

    # Set the background color of the root window
    root.configure(bg="#332f31")

    background_image = Image.open("casino.jpg")
    background_photo = ImageTk.PhotoImage(background_image)

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#332f31")
    canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    canvas.grid(row=0, column=0, columnspan=2)

    generate_button = tk.Button(root, width=20, height=1, text="Generate Winning Numbers", bg="#ab827e",
                                command=lambda: generate_orbs(canvas))
    generate_button.grid(row=1, column=0, padx=(10, 5), pady=10)

    show_rules_button = tk.Button(root, width=20, height=1, text="Populate Rules Display", bg="#ab827e",
                                  command=show_rules)
    show_rules_button.grid(row=2, column=0, padx=(10, 5), pady=10)

    show_mock_button = tk.Button(root, width=20, height=1, text="Populate Winners", bg="#ab827e",
                                 command=show_mock_winners)  # Remove the parentheses here
    show_mock_button.grid(row=3, column=0, padx=(10, 5), pady=10)

    gen_clear = tk.Button(root, width=20, height=1, text="Clear Canvas", command=clear_canvas, bg="#ab827e", )
    gen_clear.grid(row=1, column=1, padx=(5, 10), pady=10)

    add_single_button = tk.Button(root, width=20, height=1, text="Add Single Ball", bg="#ab827e",
                                  command=add_single_ball)
    add_single_button.grid(row=2, column=1, padx=(5, 10), pady=10)

    toggle_color_button = tk.Button(root, width=20, height=1, text="Toggle Drawing Color", bg="#ab827e",
                                    command=toggle_drawing_color)
    toggle_color_button.grid(row=3, column=1, padx=(5, 10), pady=10)

    root.mainloop()
