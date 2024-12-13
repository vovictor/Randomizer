import tkinter as tk
from tkinter import ttk
import random

def group_people():
    """
    Groups people into teams of 4, ensuring at least one female
    but no more than 2 in each group.
    """
    try:
        # Get text from input area and split into lines
        text = input_text.get("1.0", tk.END).strip()
        lines = text.splitlines()

        if len(lines) != 40:
            error_label.config(text="Please enter exactly 40 lines of name and gender.")
            return

        people = []
        for line in lines:
            try:
                name, gender = line.rsplit(maxsplit=1)  # Split at last space
                gender = gender.strip().capitalize()  # Clean up gender
                if gender not in ("Male", "Female"):
                    raise ValueError("Invalid gender format.")
                people.append((name.strip(), gender))
            except ValueError as e:
                error_label.config(text=f"Error parsing line: '{line}'. {e}")
                return

        random.shuffle(people)

        groups = []
        for i in range(0, 40, 4):
            group = people[i:i+4]
            # Count females in the group
            female_count = sum(1 for _, g in group if g == "Female")
            if female_count == 0:
                # Find a female to swap in
                for j in range(i+4, 40):
                    if people[j][1] == "Female":
                        group[0], people[j] = people[j], group[0]  # Swap
                        female_count += 1
                        break
            if female_count > 2:
                # Find males to swap
                for j in range(i+4, 40):
                    if people[j][1] == "Male":
                        # Swap with a female in the group
                        for k in range(4):
                            if group[k][1] == "Female":
                                group[k], people[j] = people[j], group[k]
                                female_count -= 1
                                break
                        if female_count <= 2:
                            break
            groups.append(group)

        # Display the groups in the output area
        output_text.delete("1.0", tk.END)
        for i, group in enumerate(groups):
            output_text.insert(tk.END, f"Group {i+1}:\n")
            for name, gender in group:
                output_text.insert(tk.END, f"  - {name} ({gender})\n")
            output_text.insert(tk.END, "\n")

        error_label.config(text="")  # Clear any previous errors

    except Exception as e:
        error_label.config(text=f"An error occurred: {e}")


# Set up the main application window
root = tk.Tk()
root.title("Group Maker")

# --- Input Frame ---
input_frame = ttk.LabelFrame(root, text="Input (Paste Name and Gender - one pair per line)")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

input_text = tk.Text(input_frame, wrap=tk.WORD, height=20, width=40)
input_text.grid(row=0, column=0, padx=5, pady=5)

# --- Output Frame ---
output_frame = ttk.LabelFrame(root, text="Output")
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

output_text = tk.Text(output_frame, wrap=tk.WORD, height=20, width=40)
output_text.grid(row=0, column=0, padx=5, pady=5)

# --- Button and Error Label ---
group_button = ttk.Button(root, text="Group People", command=group_people)
group_button.grid(row=1, column=0, columnspan=2, pady=10)

error_label = ttk.Label(root, text="", foreground="red")
error_label.grid(row=2, column=0, columnspan=2)

# Make the window resizable
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()