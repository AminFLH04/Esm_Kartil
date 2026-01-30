import customtkinter as ctk
from tkinter import messagebox
import random
import math

# داده‌های پایه
LETTERS = {
    'الف': 1, 'ب': 1, 'پ': 2, 'ت': 2, 'ث': 3, 'ج': 3, 'چ': 3, 'ح': 3, 'خ': 3,
    'د': 1, 'ذ': 3, 'ر': 2, 'ز': 2, 'ژ': 3, 'س': 1, 'ش': 1, 'ص': 3, 'ض': 3,
    'ط': 3, 'ظ': 3, 'ع': 3, 'غ': 3, 'ف': 2, 'ق': 3, 'ک': 1, 'گ': 3, 'ل': 1,
    'م': 1, 'ن': 1, 'و': 2, 'ه': 1, 'ی': 2
}

TOPICS = {
    'اسم پسر': 1, 'اسم دختر': 1, 'شهر': 2, 'کشور': 2, 'رنگ': 1, 'غذا': 1,
    'ماشین': 2, 'گل': 3, 'حیوان': 1, 'میوه': 1, 'شغل': 2, 'اشیا': 1,
    'اعضای بدن': 2, 'مکان تاریخی': 3, 'اسم کمپانی': 3, 'نام پرنده': 3,
    'نام ورزشکار': 2, 'نام بازیگر': 2, 'نام خواننده': 2, 'ورزش': 2,
    'فیلم و سریال': 2, 'نام نویسنده': 3, 'نام کتاب': 3
}

class AnimatedButton(ctk.CTkButton):
    """دکمه با انیمیشن هاور"""
    def __init__(self, *args, **kwargs):
        self.original_y = kwargs.pop('original_y', 0)
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event):
        self.configure(cursor="hand2")
        
    def on_leave(self, event):
        self.configure(cursor="")

class KartilGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎴 بازی اسم کارتیل")
        self.root.geometry("1400x850")
        
        # تنظیم تم
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.players = []
        self.game_mode = None
        self.mode_value = 0
        self.is_answering = False
        self.active_player = None
        self.remaining_game_time = 0
        self.countdown_after_id = None
        self.pulse_after_id = None
        
        # کانتینر اصلی
        self.main_container = ctk.CTkFrame(self.root, fg_color="#0a0e27")
        self.main_container.pack(expand=True, fill='both')
        
        # Canvas برای پس‌زمینه ثابت
        self.bg_canvas = ctk.CTkCanvas(
            self.main_container,
            bg="#0a0e27", # رنگ پایه بسیار تیره
            highlightthickness=0
        )
        self.bg_canvas.place(relwidth=1, relheight=1)
        
        # طراحی پس‌زمینه ثابت
        self.design_static_background()
        
        self.show_main_menu()

    def design_static_background(self):
        """طراحی یک پس‌زمینه انتزاعی و مدرن ثابت روی Canvas"""
        self.bg_canvas.delete("all")
        
        w, h = 2000, 1200
        color1, color2, color3 = "#0F172A", "#1E1B4B", "#111827"

        self.bg_canvas.create_polygon(0, 0, w*0.6, 0, w*0.4, h*0.5, 0, h*0.8, fill=color1, outline="")
        self.bg_canvas.create_polygon(w, h, w*0.3, h, w*0.5, h*0.4, w, h*0.2, fill=color2, outline="")
        self.bg_canvas.create_polygon(w*0.2, h, w*0.8, 0, w*0.95, 0, w*0.35, h, fill=color3, outline="")

        # اگر خط پایین باز هم خطا داد، کلاً حذفش کن چون Canvas اولین ویجتی است که ساخته شده و زیر بقیه می‌ماند
        try:
            self.bg_canvas.lower("all") 
        except:
            pass
        
    def clear_screen(self):
        self.root.unbind("<Return>")
        for widget in self.main_container.winfo_children():
            if widget != self.bg_canvas:
                widget.destroy()

    def create_glowing_button(self, parent, text, command, width=220, height=55, color="#6366F1"):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn = AnimatedButton(
            frame,
            text=text,
            command=command,
            width=width,
            height=height,
            corner_radius=20,
            font=ctk.CTkFont(family="B Nazanin", size=20, weight="bold"),
            fg_color=color,
            hover_color=self.lighten_color(color),
            border_width=0,
            text_color="#FFFFFF"
        )
        btn.pack(padx=3, pady=3)
        return frame
    
    def lighten_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_glass_card(self, parent, title, value, stars, gradient_colors):
        outer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # تعریف ابعاد ثابت برای کارت
        CARD_WIDTH = 280
        CARD_HEIGHT = 380
        
        card = ctk.CTkFrame(
            outer_frame,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            corner_radius=25,
            fg_color=gradient_colors[0],
            border_width=3,
            border_color=gradient_colors[1]
        )
        card.pack(padx=4, pady=4)
        
        # جلوگیری از تغییر اندازه کارت توسط محتویات داخلی
        card.pack_propagate(False)
        
        # بخش ستاره‌ها
        stars_frame = ctk.CTkFrame(card, fg_color="transparent")
        stars_frame.pack(pady=(30, 10))
        star_label = ctk.CTkLabel(
            stars_frame, 
            text="", 
            font=ctk.CTkFont(size=24), 
            text_color="#FFD700"
        )
        star_label.pack()
        
        # عنوان (حرف یا موضوع)
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="B Nazanin", size=20, weight="bold"),
            text_color="#E0E7FF"
        )
        title_label.pack(pady=10)
        
        # مقدار اصلی (خودِ حرف یا نام موضوع)
        # استفاده از wraplength برای اینکه اگر متن موضوع طولانی بود، به خط بعد برود و کارت را خراب نکند
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family="B Titr", size=50, weight="bold"),
            text_color="#FFFFFF",
            wraplength=240  # عرض متن حداکثر ۲۴۰ پیکسل باشد
        )
        value_label.pack(expand=True, pady=20, padx=20)
        
        return outer_frame, card, star_label, value_label

    def add_back_button(self, command):
        back_btn = ctk.CTkButton(
            self.main_container,
            text="◄ بازگشت",
            command=command,
            width=130,
            height=45,
            corner_radius=15,
            font=ctk.CTkFont(family="B Nazanin", size=16, weight="bold"),
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=2,
            border_color="#475569"
        )
        back_btn.place(x=25, y=25)

    def show_instructions(self):
        text = (
            "🎯 راهنمای بازی اسم کارتیل\n\n"
            "۱. ابتدا تنظیمات بازیکنان و مود بازی را انجام دهید.\n\n"
            "۲. هر کارت دارای امتیاز (ستاره) مشخصی است.\n\n"
            "۳. کلید Enter برای تعویض کارت یا تایید پاسخ.\n\n"
            "۴. در صورت تساوی، تمام برندگان اعلام می‌شوند.\n\n"
            "موفق باشید! 🎊"
        )
        messagebox.showinfo("آموزش بازی", text)

    def show_main_menu(self):
        self.clear_screen()
        info_btn = ctk.CTkButton(
            self.main_container,
            text="❓",
            command=self.show_instructions,
            width=50,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#1e293b",
            hover_color="#3B82F6",
            border_width=2,
            border_color="#475569"
        )
        info_btn.place(x=25, y=25)
        
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        title_frame.pack(pady=(0, 30))
        
        title = ctk.CTkLabel(
            title_frame,
            text="🎴 اسم کارتیل 🎴",
            font=ctk.CTkFont(family="B Titr", size=90, weight="bold"),
            text_color="#818CF8"
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            center_frame,
            text="✨ بازی فکری و سرگرم‌کننده ✨",
            font=ctk.CTkFont(family="B Nazanin", size=24),
            text_color="#A5B4FC"
        )
        subtitle.pack(pady=(0, 60))
        
        start_btn_frame = self.create_glowing_button(
            center_frame,
            "▶ شروع بازی",
            self.setup_players_count,
            width=280,
            height=70,
            color="#6366F1"
        )
        start_btn_frame.pack()
        self.root.bind("<Return>", lambda e: self.setup_players_count())

    def setup_players_count(self):
        self.clear_screen()
        self.add_back_button(self.show_main_menu)
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(
            center_frame,
            text="👥 تعداد بازیکنان",
            font=ctk.CTkFont(family="B Nazanin", size=40, weight="bold"),
            text_color="#E0E7FF"
        )
        title.pack(pady=(0, 40))
        
        input_container = ctk.CTkFrame(
            center_frame,
            fg_color="#1e293b",
            corner_radius=20,
            border_width=3,
            border_color="#6366F1"
        )
        input_container.pack(pady=30)
        
        entry_count = ctk.CTkEntry(
            input_container,
            width=250,
            height=60,
            justify='center',
            font=ctk.CTkFont(size=28, weight="bold"),
            corner_radius=15,
            border_width=0,
            fg_color="#0f172a",
            text_color="#FFFFFF"
        )
        entry_count.pack(padx=20, pady=20)
        entry_count.focus_set()
        
        def proceed():
            try:
                value = entry_count.get().strip()
                if not value: raise ValueError("ورودی خالی است")
                count = int(value)
                if count < 1: raise ValueError("عدد باید حداقل 1 باشد")
                self.get_players_info(count)
            except ValueError:
                messagebox.showerror("خطا", "لطفاً یک عدد معتبر وارد کنید")
        
        next_btn_frame = self.create_glowing_button(
            center_frame, "ادامه ◄", proceed, width=250, height=60, color="#8B5CF6"
        )
        next_btn_frame.pack(pady=20)
        self.root.bind("<Return>", lambda e: proceed())

    def get_players_info(self, count):
        self.clear_screen()
        self.add_back_button(self.setup_players_count)
        title = ctk.CTkLabel(
            self.main_container,
            text="📝 اطلاعات بازیکنان",
            font=ctk.CTkFont(family="B Titr", size=45, weight="bold"),
            text_color="#818CF8"
        )
        title.pack(pady=35)
        
        scroll_container = ctk.CTkFrame(
            self.main_container, fg_color="#1e293b", corner_radius=25, border_width=2, border_color="#475569"
        )
        scroll_container.pack(pady=20, padx=60, fill='both', expand=True)
        
        scroll_frame = ctk.CTkScrollableFrame(
            scroll_container, width=900, height=450, corner_radius=20, fg_color="transparent"
        )
        scroll_frame.pack(pady=15, padx=15, fill='both', expand=True)
        
        entries = []
        for i in range(count):
            player_frame = ctk.CTkFrame(scroll_frame, corner_radius=18, fg_color="#0f172a", border_width=2, border_color="#334155")
            player_frame.pack(fill='x', pady=10, padx=15)
            
            num_container = ctk.CTkFrame(player_frame, fg_color="#6366F1", corner_radius=50, width=50, height=50)
            num_container.pack(side='right', padx=15, pady=15)
            ctk.CTkLabel(num_container, text=str(i+1), font=ctk.CTkFont(size=20, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")
            
            name_ent = ctk.CTkEntry(player_frame, placeholder_text="نام بازیکن", width=280, height=45, corner_radius=12)
            name_ent.pack(side='right', padx=10, pady=15)
            ctk.CTkLabel(player_frame, text="⌨️ کلید:", font=ctk.CTkFont(family="B Nazanin", size=16)).pack(side='right', padx=8)
            key_ent = ctk.CTkEntry(player_frame, placeholder_text="a", width=80, height=45, corner_radius=12, justify='center')
            key_ent.pack(side='right', padx=15, pady=15)
            entries.append((name_ent, key_ent))
        
        def save_and_next():
            self.players = []
            used_keys = set()
            for n, k in entries:
                name, key = n.get().strip(), k.get().strip().lower()
                if not name or not key:
                    messagebox.showwarning("خطا", "همه فیلدها را پر کنید")
                    return
                if key in used_keys:
                    messagebox.showwarning("خطا", "کلیدها تکراری هستند")
                    return
                used_keys.add(key)
                self.players.append({'name': name, 'key': key, 'score': 0})
            self.choose_mode()
        
        confirm_btn_frame = self.create_glowing_button(self.main_container, "✓ تایید و ادامه", save_and_next, color="#10B981")
        confirm_btn_frame.pack(pady=25)
        self.root.bind("<Return>", lambda e: save_and_next())

    def choose_mode(self):
        self.clear_screen()
        self.add_back_button(lambda: self.get_players_info(len(self.players)))
        center_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(center_frame, text="🎮 انتخاب مود بازی", font=ctk.CTkFont(family="B Titr", size=50, weight="bold"), text_color="#818CF8").pack(pady=(0, 80))
        
        def set_mode(m):
            self.game_mode = m
            self.clear_screen()
            self.add_back_button(self.choose_mode)
            center = ctk.CTkFrame(self.main_container, fg_color="transparent")
            center.place(relx=0.5, rely=0.5, anchor="center")
            
            prompt = "⏱️ زمان بازی (ثانیه):" if m == 'time' else "🏆 امتیاز هدف:"
            ctk.CTkLabel(center, text=prompt, font=ctk.CTkFont(family="B Nazanin", size=35, weight="bold")).pack(pady=(0, 40))
            
            val_ent = ctk.CTkEntry(center, width=250, height=60, justify='center', font=ctk.CTkFont(size=28, weight="bold"))
            val_ent.pack(pady=30)
            val_ent.focus_set()
            
            def final_start():
                try:
                    self.mode_value = int(val_ent.get().strip())
                    if self.game_mode == 'time': self.remaining_game_time = self.mode_value
                    self.start_game_ui()
                except ValueError: messagebox.showerror("خطا", "عدد معتبر وارد کنید")
            
            self.create_glowing_button(center, "🎯 شروع بازی", final_start, color="#EC4899" if m == 'time' else "#10B981").pack(pady=30)
            self.root.bind("<Return>", lambda e: final_start())

        self.create_glowing_button(center_frame, "⏱️ مود تایمی", lambda: set_mode('time'), color="#EC4899", width=350, height=90).pack(pady=18)
        self.create_glowing_button(center_frame, "🏆 مود امتیازی", lambda: set_mode('score'), color="#10B981", width=350, height=90).pack(pady=18)

    def start_game_ui(self):
        self.clear_screen()
        self.root.bind("<Key>", self.handle_keypress)
        
        self.top_bar = ctk.CTkFrame(self.main_container, height=70, fg_color="#1e293b")
        self.top_bar.pack(fill='x')
        self.lbl_info = ctk.CTkLabel(self.top_bar, text="", font=ctk.CTkFont(family="B Nazanin", size=22, weight="bold"))
        self.lbl_info.pack(pady=20)
        self.add_back_button(self.show_main_menu)
        
        self.game_body = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.game_body.pack(fill='both', expand=True, padx=25, pady=25)
        
        self.score_sidebar = ctk.CTkFrame(self.game_body, width=280, fg_color="#1e293b", border_width=3, border_color="#475569")
        self.score_sidebar.pack(side='right', fill='both', padx=(15, 0))
        self.score_sidebar.pack_propagate(False)
        ctk.CTkLabel(self.score_sidebar, text="🏆 جدول امتیازات", font=ctk.CTkFont(family="B Titr", size=24, weight="bold"), text_color="#818CF8").pack(pady=20)
        
        self.score_list_frame = ctk.CTkScrollableFrame(self.score_sidebar, fg_color="transparent")
        self.score_list_frame.pack(fill='both', expand=True, padx=12, pady=(0, 15))
        
        self.card_area = ctk.CTkFrame(self.game_body, fg_color="transparent")
        self.card_area.pack(side='left', fill='both', expand=True)
        self.create_glowing_button(self.card_area, "🎴 کارت جدید", self.next_round, color="#10B981").pack(pady=25)
        
        cards_container = ctk.CTkFrame(self.card_area, fg_color="transparent")
        cards_container.pack(expand=True)
        
        self.letter_card_outer, self.letter_card_widget, self.letter_star_label, self.letter_value_label = self.create_glass_card(cards_container, "🔤 حرف", "؟", 0, ("#7C3AED", "#A78BFA"))
        self.letter_card_outer.pack(side='left', padx=35)
        
        self.topic_card_outer, self.topic_card_widget, self.topic_star_label, self.topic_value_label = self.create_glass_card(cards_container, "📋 موضوع", "؟", 0, ("#0EA5E9", "#38BDF8"))
        self.topic_card_outer.pack(side='left', padx=35)
        
        self.countdown_label = ctk.CTkLabel(self.card_area, text="", font=ctk.CTkFont(size=56, weight="bold"), text_color="#F87171")
        self.countdown_label.pack(side='bottom', pady=50)
        
        self.update_score_display()
        if self.game_mode == 'time': self.tick_game_timer()

    def next_round(self):
        if self.is_answering: return
        self.current_letter = random.choice(list(LETTERS.keys()))
        self.current_topic = random.choice(list(TOPICS.keys()))
        self.letter_value_label.configure(text=self.current_letter)
        self.letter_star_label.configure(text="⭐" * LETTERS[self.current_letter])
        self.topic_value_label.configure(text=self.current_topic)
        self.topic_star_label.configure(text="⭐" * TOPICS[self.current_topic])
        self.countdown_label.configure(text="")

    def handle_keypress(self, event):
        if self.is_answering and event.keysym == "Return":
            if self.countdown_after_id: self.root.after_cancel(self.countdown_after_id)
            self.show_answer_dialog()
            return
        if not self.is_answering:
            if event.keysym == "Return": self.next_round(); return
            for p in self.players:
                if p['key'] == event.char.lower(): self.start_answer_phase(p); break

    def start_answer_phase(self, player):
        self.is_answering = True
        self.active_player = player
        self.remaining_seconds = 5
        self.process_countdown()

    def process_countdown(self):
        if self.remaining_seconds > 0:
            self.countdown_label.configure(text=f"⏱️ {self.active_player['name']}: {self.remaining_seconds}")
            self.remaining_seconds -= 1
            self.countdown_after_id = self.root.after(1000, self.process_countdown)
        else: self.show_answer_dialog()

    def show_answer_dialog(self):
        res = messagebox.askyesno("بررسی پاسخ", f"آیا {self.active_player['name']} درست پاسخ داد؟")
        points = LETTERS.get(self.current_letter, 0) + TOPICS.get(self.current_topic, 0)
        if res: self.active_player['score'] += points
        else: self.active_player['score'] -= points
        self.is_answering = False
        self.update_score_display()
        if not self.is_game_over(): self.next_round()
        else: self.end_game()

    def is_game_over(self):
        if self.game_mode == 'score': return any(p['score'] >= self.mode_value for p in self.players)
        return False

    def update_score_display(self):
        for widget in self.score_list_frame.winfo_children(): widget.destroy()
        sorted_players = sorted(self.players, key=lambda x: x['score'], reverse=True)
        for i, p in enumerate(sorted_players):
            bg = "#6366F1" if i == 0 else "#0f172a"
            player_frame = ctk.CTkFrame(self.score_list_frame, corner_radius=15, fg_color=bg)
            player_frame.pack(fill='x', pady=6)
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
            ctk.CTkLabel(player_frame, text=medal, font=ctk.CTkFont(size=18, weight="bold")).pack(side='left', padx=10, pady=12)
            ctk.CTkLabel(player_frame, text=p['name'], font=ctk.CTkFont(family="B Nazanin", size=16, weight="bold")).pack(side='right', padx=12, pady=12)
            ctk.CTkLabel(player_frame, text=str(p['score']), font=ctk.CTkFont(size=20, weight="bold")).pack(side='left', padx=12, pady=12)

    def tick_game_timer(self):
        if self.game_mode == 'time' and self.remaining_game_time > 0:
            m, s = divmod(self.remaining_game_time, 60)
            self.lbl_info.configure(text=f"⏰ زمان باقی‌مانده: {m:02d}:{s:02d}")
            self.remaining_game_time -= 1
            self.root.after(1000, self.tick_game_timer)
        elif self.game_mode == 'time': self.end_game()

    def end_game(self):
        self.root.unbind("<Key>")
        max_score = max(p['score'] for p in self.players)
        winners = [p['name'] for p in self.players if p['score'] == max_score]
        messagebox.showinfo("🎉 پایان بازی! 🎉", f"🏆 برنده(ها) با امتیاز {max_score}:\n\n{' و '.join(winners)}")
        self.show_main_menu()

if __name__ == "__main__":
    root = ctk.CTk()
    game = KartilGame(root)
    root.mainloop()