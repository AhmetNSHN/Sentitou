import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from tkinter import messagebox as msg
from matplotlib.figure import Figure
from matplotlib import patches
from wordcloud import WordCloud
from UserInterface.GlobalFunctions import centeralize_screen, safe_div
from Analyser.NaiveBayes import Predict
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class F_Left(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bd=0, bg="white")

        self.parent = parent
        self.data = ""
        self.analyse_Excel = True  # set false after test
        self.thread = None
        self.document_name = None
        self.canvas_wordcloud = None

        f_left_top = tk.Frame(self, bg="white")
        f_left_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.progress_bar["maximum"] = 1
        self.progress_bar["value"] = 0

        f_left_buttons = ttk.Frame(self)
        f_left_buttons.pack(side=tk.BOTTOM, fill=tk.X)

        self.sc_scrollbox = scrolledtext.ScrolledText(self, width=30, relief="solid", wrap=tk.WORD)
        self.sc_scrollbox.pack(fill=tk.X, side=tk.BOTTOM)

        self.b_analyse = tk.Button(f_left_buttons, text="Analyse", command=self.analyse)
        self.b_analyse.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.b_load = tk.Button(f_left_buttons, text="Open Excel Document", command=self.open_file_explorer)
        self.b_load.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.b_clear = tk.Button(f_left_buttons, text="Reset", command=self.Reset)
        self.b_clear.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def open_file_explorer(self):
        self.document_name = None
        self.sc_scrollbox.configure(state='normal')
        self.sc_scrollbox.delete('1.0', tk.END)
        self.document_name = filedialog.askopenfilename(filetypes=[("Excel File", "*.xlsx")])
        if self.document_name:
            self.sc_scrollbox.insert(tk.INSERT, f"Document: {str(self.document_name)}")
        self.sc_scrollbox.configure(state='disabled')
        self.analyse_Excel = True

    def Reset(self):
        self.sc_scrollbox.configure(state="normal")
        self.sc_scrollbox.delete('1.0', tk.END)
        self.analyse_Excel = False
        self.parent.UpdateCharts([[0, 0, 100], [0, 0, 100], [0, 0, 100], [0, 0, 100], [0, 0, 100], [0, 0, 100]])
        if self.canvas_wordcloud:
            self.canvas_wordcloud.get_tk_widget().destroy()
        self.progress_bar["value"] = 0
        self.document_name = None

    def analyse(self):
        if self.document_name:
            self.b_analyse["state"] = "disabled"
            self.b_clear["state"] = "disabled"
            self.b_load["state"] = "disabled"

            self.thread = Thread(target=self.thread_analyse())
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            msg.showwarning(title="Warning", message="Select Excel document to analyse")

    def thread_analyse(self):
        p1 = Predict(self, self.document_name, self.data)
        s_word_cloud, result, category_count = p1.Calculate()
        dummy_result = [[result[0], 100 - result[0], 0],
                        [result[1], 100 - result[1], 0],
                        [result[2], 100 - result[2], 0],
                        [result[3], 100 - result[3], 0],
                        [result[4], 100 - result[4], 0],
                        [result[5], 100 - result[5], 0]]

        self.parent.UpdateCharts(dummy_result)
        self.draw_wordcloud(s_word_cloud)
        self.sc_scrollbox.configure(state="normal")
        self.sc_scrollbox.insert(tk.END, f"\n\nFrom total of {category_count[5]} Reviews:\n\n"
                                         f"Room was mentioned in {category_count[0]} comments ({int(safe_div(category_count[0], category_count[5])*100)}% of the comments)."
                                         f" with rating {result[0]/10}\n\n"
                                         f"Food was mentioned in {category_count[1]} comments ({int(safe_div(category_count[1], category_count[5])*100)}% of the comments)."
                                         f" with rating {result[1]/10}\n\n"
                                         f"Pool/Sea was mentioned in {category_count[2]} comments ({int(safe_div(category_count[2], category_count[5])*100)}% of the comments)."
                                         f" with rating {result[2]/10}\n\n"
                                         f"Price was mentioned in {category_count[3]} comments ({int(safe_div(category_count[3], category_count[5])*100)}% of the comments)."
                                         f" with rating {result[3]/10}\n\n"
                                         f"Staff was mentioned in {category_count[4]} comments ({int(safe_div(category_count[4], category_count[5])*100)}% of the comments)."
                                         f" with rating {result[4]/10}\n\n")

        self.sc_scrollbox.configure(state="disabled")
        self.progress_bar["value"] = 1

        self.b_analyse["state"] = "normal"
        self.b_clear["state"] = "normal"
        self.b_load["state"] = "normal"

    def draw_wordcloud(self, s_word_cloud):
        if self.canvas_wordcloud:
            self.canvas_wordcloud.get_tk_widget().destroy()
        fig_wordcloud = Figure()
        fig_wordcloud.subplots_adjust(left=0.03, bottom=0.07, right=0.98, top=0.97, wspace=0, hspace=0)
        fig_wordcloud.tight_layout()
        wordcloud = fig_wordcloud.add_subplot(111)
        im_wordcloud = WordCloud(width=500, height=500, background_color="white", max_words=100).generate(s_word_cloud)
        wordcloud.imshow(im_wordcloud)
        wordcloud.axis("off")
        self.canvas_wordcloud = FigureCanvasTkAgg(fig_wordcloud, master=self)
        self.canvas_wordcloud.get_tk_widget().pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.canvas_wordcloud.draw()
        self.canvas_wordcloud.blit()

    def destroy_wordcloud(self):
        self.canvas_wordcloud.get_tk_widget().destroy()


class F_Right(tk.Frame):
    def __init__(self, parent, ratios):
        tk.Frame.__init__(self, parent, bd=0)
        self.fig_donutcharts = Figure(figsize=(8, 8))
        self.fig_donutcharts.tight_layout()
        self.canvas_donutcharts = FigureCanvasTkAgg(self.fig_donutcharts, master=self)
        self.canvas_donutcharts.get_tk_widget().pack(fill=tk.BOTH)
        self.draw_donatcharts(ratios)

    def draw_donatcharts(self, ratios):
        colors = ['#38C477', '#F28268', '#EEEEEE']
        ax1 = self.fig_donutcharts.add_subplot(231)
        ax1.pie(wedgeprops={'width': 0.3}, startangle=90, colors=colors, x=ratios[0])
        ax1.legend(["Positive", "Negative"])
        # ax1.title('Food', fontsize=24, loc='left')
        ax1.text(0, 0, f"{ratios[0][0]/10}", ha='center', va='center', fontsize=40)
        ax1.text(-1.2, -1.2, "Room", ha='center', va='center', fontsize=20)
        # plt.ylim(-3, 3)
        circle = patches.Circle((0, 0), 0.7, color='white')
        ax1.add_artist(circle)

        ax2 = self.fig_donutcharts.add_subplot(232)
        ax2.pie(wedgeprops={'width': 0.3}, startangle=90, colors=colors, x=ratios[1])
        # ax2.title('Food', fontsize=24, loc='left')
        ax2.text(0, 0, f"{ratios[1][0]/10}", ha='center', va='center', fontsize=40)
        ax2.text(-1.2, -1.2, "Food", ha='center', va='center', fontsize=20)
        # plt.ylim(-3, 3)
        circle = patches.Circle((0, 0), 0.7, color='white')
        ax2.add_artist(circle)

        ax3 = self.fig_donutcharts.add_subplot(233)
        ax3.pie(wedgeprops={'width': 0.3}, startangle=90, colors=colors, x=ratios[2])
        # ax3.title('Food', fontsize=24, loc='left')
        ax3.text(0, 0, f"{ratios[2][0]/10}", ha='center', va='center', fontsize=40)
        ax3.text(-1.2, -1.2, "Pool/Sea", ha='center', va='center', fontsize=20)
        # plt.ylim(-3, 3)
        circle = patches.Circle((0, 0), 0.7, color='white')
        ax3.add_artist(circle)

        ax4 = self.fig_donutcharts.add_subplot(234)
        ax4.pie(wedgeprops={'width': 0.3}, startangle=90, colors=colors, x=ratios[3])
        # ax4.title('Food', fontsize=24, loc='left')
        ax4.text(0, 0, f"{ratios[3][0]/10}", ha='center', va='center', fontsize=40)
        ax4.text(-1.2, -1.2, "Price", ha='center', va='center', fontsize=20)
        # plt.ylim(-3, 3)
        circle = patches.Circle((0, 0), 0.7, color='white')
        ax4.add_artist(circle)

        ax5 = self.fig_donutcharts.add_subplot(235)
        ax5.pie(wedgeprops={'width': 0.3}, startangle=90, colors=colors, x=ratios[4])
        # ax5.title('Food', fontsize=24, loc='left')
        ax5.text(0, 0, f"{ratios[4][0]/10}", ha='center', va='center', fontsize=40)
        ax5.text(-1.2, -1.2, "Staff", ha='left', va='center', fontsize=20)
        # plt.ylim(-3, 3)
        circle = patches.Circle((0, 0), 0.7, color='white')
        ax5.add_artist(circle)
        self.fig_donutcharts.tight_layout(pad=0)

        ax6 = self.fig_donutcharts.add_subplot(236)
        ax6.pie(wedgeprops={'width': 0.3}, startangle=90, colors=colors, x=ratios[5])
        # ax6.title('Food', fontsize=24, loc='left')
        ax6.text(0, 0, f"{ratios[5][0]/10}", ha='center', va='center', fontsize=40)
        ax6.text(-1.2, -1.2, "Overall", ha='left', va='center', fontsize=20)
        # plt.ylim(-3, 3)
        circle = patches.Circle((0, 0), 0.7, color='white')
        ax6.add_artist(circle)

        self.canvas_donutcharts.draw()

    def del_donatcharts(self):
        del self.fig_donutcharts


class window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(" Sentitou")
        self.iconphoto(True, tk.PhotoImage(file="UserInterface/icon1.png"))
        self.geometry(centeralize_screen(screen_width=self.winfo_screenwidth(),
                                         screen_height=self.winfo_screenheight(),
                                         window_width=1000,
                                         window_height=600))
        self.columnconfigure(0, weight=1, uniform="x")
        self.columnconfigure(1, weight=3, uniform="x")
        self.rowconfigure(0, weight=1)
        self.grid_propagate(False)

        self.f_right = F_Right(self, [[0, 0, 100], [0, 0, 100], [0, 0, 100], [0, 0, 100], [0, 0, 100], [0, 0, 100]])
        self.f_right.grid(column=1, row=0, sticky="NSEW")

        self.f_left = F_Left(self)
        self.f_left.grid(column=0, row=0, sticky="NSEW")

    def UpdateCharts(self, ratios):
        self.f_right.destroy()
        self.f_right = F_Right(self, ratios)
        self.f_right.grid(column=1, row=0, sticky="NSEW")
        # self.f_right.draw_donatcharts(ratios)


win = window()
win.mainloop()
