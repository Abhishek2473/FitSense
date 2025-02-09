import tkinter as tk
import tkinter.font as tkFont
import os
import json
from tkinter import simpledialog
from tkinter import ttk
import customtkinter as ctk
import pushup
import squat
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from ask_trainer import initialize


class App:
    saveData = ""
    ctk.set_default_color_theme("dark-blue")

    def __init__(self, root):
        # setting title
        root.title("FitSense")
        App._root = root
        # setting window size
        App._width = 880
        App._height = 700
        width = App._width
        height = App._height
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        homeFrame = tk.Frame(root, bg="#E6E6FA")
        App._homeFrame = homeFrame
        homeFrame.pack(fill="both", expand=True)

        # Add title with icon
        title_font = tkFont.Font(family='Comic Sans MS', size=48, weight="bold", slant="italic")
        title_label = tk.Label(homeFrame, text="FitSense", font=title_font, bg="#E6E6FA", fg="#FF4500")
        title_label.place(x=App._width / 2 - 150, y=20)

        options = ['Squat', 'Pushup']

        combo = ctk.CTkComboBox(
            master=homeFrame, values=options, height=30, width=200, corner_radius=10, fg_color="#FFFFFF", text_color="#000000")
        combo.place(x=App._width / 2 - 100, y=App._height / 2 - 100)

        combo.set(options[0])
        self.__comboDd__ = combo

        DropDownButton = ctk.CTkButton(master=homeFrame, text="Start Counting reps!",
                                       width=250, height=70, command=self.DropDownButton_command, font=ctk.CTkFont(size=18), corner_radius=10, fg_color="#FFD700", text_color="#000000")
        DropDownButton.place(x=App._width / 2 - 275, y=App._height / 2 - 35)

        TrainerButton = ctk.CTkButton(
            master=homeFrame, text="AI Trainer", width=250, height=70, command=self.TrainerButton_command, corner_radius=10, fg_color="#ADFF2F", text_color="#000000", font=ctk.CTkFont(size=18))
        TrainerButton.place(x=App._width / 2 + 25, y=App._height / 2 - 35)

        GoalLabel = ctk.CTkLabel(
            master=homeFrame, text="Goal (No. of reps):", width=150, height=30,font=ctk.CTkFont(size=18), corner_radius=10, fg_color="#33A1FF", text_color="#000000")
        GoalLabel.place(x=App._width / 2 - 75, y=App._height / 2 + 50)

        GoalEntry = ctk.CTkEntry(master=homeFrame, width=100, height=30,font=ctk.CTkFont(size=18), corner_radius=10, fg_color="#33A1FF", text_color="#000000")
        GoalEntry.place(x=App._width / 2 + 100, y=App._height / 2 + 50)
        GoalEntry.insert(0, 10)

        App._workout_GoalEntry = GoalEntry

    def DropDownButton_command(self):
        print("command")
        goal = App._workout_GoalEntry.get()
        App._goal_val = goal
        exercise = self.__comboDd__.get()
        match exercise:
            case "Pushup":
                pushup.start(goal)
                App._exercise = 0
                self.ShowResultsPage()
                print("Pushups Ended")
            case "Squat":
                squat.start(goal)
                App._exercise = 3
                self.ShowResultsPage()
            case _:
                pass

    def TrainerButton_command(self):
        BG_GRAY = "#ABB2B9"
        BG_COLOR = "#17202A"
        TEXT_COLOR = "#EAECEE"

        FONT = "Helvetica 14"
        FONT_BOLD = "Helvetica 13 bold"

        trainerFrame = tk.Frame(App._root, bg="#E6E6FA")
        App._homeFrame.pack_forget()
        trainerFrame.pack(fill="both", expand=True)
        App._trainerFrame = trainerFrame

        CloseButton = ctk.CTkButton(
            master=trainerFrame, width=100, height=70, command=self.CloseButtonTrainer_command, text="Close", corner_radius=10, fg_color="#FFD700", text_color="#000000", font=ctk.CTkFont(size=18))
        CloseButton.place(x=100, y=600)

        label1 = ctk.CTkLabel(master=trainerFrame, fg_color=BG_COLOR,
                              text="AI Trainer", width=100, height=50, corner_radius=20, text_color="#FF4500")
        label1.place(x=440 - 70/2, y=20, )

        txt = ctk.CTkTextbox(trainerFrame, fg_color=BG_COLOR,
                             width=670, height=450, pady=2, text_color="#FFFFFF")
        txt.place(x=100, y=100)
        App._txt = txt

        send = ctk.CTkButton(trainerFrame, text="Send", width=70, height=70, fg_color="#ADFF2F",
                             command=self.send_command, font=ctk.CTkFont(size=18), text_color="#000000")
        send.place(x=100+620, y=600, )

        e = ctk.CTkEntry(trainerFrame, fg_color="#2C3E50",
                         width=540, height=50, text_color="#FFFFFF")
        e.place(x=180, y=600)
        e.focus()
        App._e = e

        scrollbar = Scrollbar(txt)
        scrollbar.place(relheight=1, relx=0.974)

    def send_command(self):
        send = "You -> " + App._e.get()
        App._txt.insert(tk.END, "\n" + send)

        user_q = App._e.get().lower()

        response = initialize(user_q)

        App._e.delete(0, tk.END)

        App._txt.insert(tk.END, "\n" + "Bot -> " + response)

        pass

    def ShowResultsPage(self):
        resultsFrame = tk.Frame(App._root, bg="#E6E6FA")
        App._homeFrame.pack_forget()
        resultsFrame.pack(fill="both", expand=True)
        App._resultsFrame = resultsFrame

        ResultsLabel = tk.Label(resultsFrame, bg="#E6E6FA", fg="#000000")
        ft = tkFont.Font(family='Helvetica', size=10)
        ResultsLabel["font"] = ft
        ResultsLabel["justify"] = "center"
        ResultsLabel.place(x=440 - 800 / 2, y=20, width=800, height=560)

        with open('results.json', 'r') as f:
            data = json.load(f)

        results = "N/A"
        t_goal = "N/A"
        if len(data[App._exercise]) != 0:
            results = data[App._exercise][len(data[App._exercise]) - 2]
            t_goal = data[App._exercise][len(data[App._exercise]) - 1]

        GoalHeader = tk.Label(ResultsLabel, bg="#E6E6FA", fg="#000000")
        ft = tkFont.Font(family='Helvetica', size=20, weight="bold")
        GoalHeader["font"] = ft
        GoalHeader["justify"] = "left"
        GoalHeader["anchor"] = "w"
        GoalHeader["text"] = "Goal: " + str(t_goal) + " reps."
        GoalHeader.place(x=20, y=20, width=200, height=30)

        ResultsHeader = tk.Label(ResultsLabel, bg="#E6E6FA", fg="#000000")
        ft = tkFont.Font(family='Helvetica', size=20, weight="bold")
        ResultsHeader["font"] = ft
        ResultsHeader["justify"] = "left"
        ResultsHeader["anchor"] = "w"
        ResultsHeader["wraplength"] = 250
        ResultsHeader["text"] = "Results: " + str(results) + " reps."
        ResultsHeader.place(x=20, y=100, width=200, height=30)

        if results <= 0.8 * t_goal:
            message = "Not quite enough- more work is needed!"
        elif results >= 1.2 * t_goal:
            message = "Nice! You exceeded your goal."
        else:
            message = "Nice! You met your goal."

        messageLabel = tk.Label(resultsFrame, bg="#E6E6FA", fg="#000000")
        ft = tkFont.Font(family='Helvetica', size=10)
        messageLabel["font"] = ft
        messageLabel["justify"] = "center"
        messageLabel.place(x=440 - 800 / 2, y=420, width=700, height=100)

        resultsMessage = tk.Label(messageLabel, bg="#E6E6FA", fg="#000000")
        ft = tkFont.Font(family='Helvetica', size=18, weight="bold")
        resultsMessage["font"] = ft
        resultsMessage["justify"] = "left"
        resultsMessage["anchor"] = "w"
        resultsMessage["text"] = message
        resultsMessage.place(x=20, y=20, width=700, height=120)

        CloseButton = ctk.CTkButton(
            master=resultsFrame, width=100, height=70, command=self.CloseButtonResults_command, text="Close", corner_radius=10, fg_color="#FFD700", text_color="#000000", font=ctk.CTkFont(size=18))
        CloseButton.place(x=30, y=App._height - 60)

        results_arr = []
        goals_arr = []

        for i in range(0, len(data[App._exercise])):
            if i % 2 == 0:
                results_arr.append(data[App._exercise][i])
            else:
                goals_arr.append(data[App._exercise][i])

        # Define the maximum number of sessions to display
        max_sessions = 7

        # Slice the arrays to include only the last 'max_sessions' entries
        results_arr = results_arr[-max_sessions:]
        goals_arr = goals_arr[-max_sessions:]

        # Recalculate x-axis to always start from 1
        x_axis = list(range(1, len(results_arr) + 1))

        # Calculate the percentage of goal completed for each session
        y_axis = [results_arr[i] / goals_arr[i] * 100 for i in range(len(results_arr))]

        print(y_axis)
        print(x_axis)

        fig, ax = plt.subplots()
        ax.set_ylim(0, 100)
        ax.set_xlim(0.5, len(x_axis) + 0.5)
        plt.scatter(x_axis, y_axis)
        plt.plot(x_axis, y_axis)
        plt.xlabel("Workout number")
        plt.ylabel("Percent of goal completed")
        plt.grid(True)

        plt.savefig("graph1.png")

        test = ImageTk.PhotoImage(Image.open(
            "graph1.png").resize((450, 400), Image.Resampling.LANCZOS))

        label1 = tk.Label(resultsFrame, image=test, bg="#E6E6FA")
        label1.image = test
        label1.place(x=350, y=40)

    def CloseButtonTrainer_command(self):
        App._trainerFrame.pack_forget()
        App._homeFrame.pack(fill="both", expand=True)

    def CloseButtonResults_command(self):
        App._resultsFrame.pack_forget()
        App._homeFrame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
