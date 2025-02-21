import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
from datetime import datetime
import json
import os
import re
import random
import pytesseract
from PIL import Image
import webbrowser

class FishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Tracker by S1maBY_ for Russian Fishing 4")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Указываем путь к Tesseract (раскомментируйте и укажите свой путь, если нужно)
        # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        # Загрузка списка рыб и цен из файла
        self.load_fish_prices()
        
        # Список для хранения улова
        self.catch_list = []
        
        # Флаг для управления сканированием
        self.scanning = False
        
        # Интервал сканирования по умолчанию (в миллисекундах)
        self.scan_interval = 100
        
        # Создание интерфейса
        self.create_widgets()
        
    def load_fish_prices(self):
        if os.path.exists("fish_prices.json"):
            with open("fish_prices.json", "r", encoding="utf-8") as f:
                self.fish_prices = json.load(f)
        else:
            fish_list = [
                "Акула гигантская", "Акула гренландская полярная", "Акула плащеносная", 
                "Акула сельдевая атлантическая", "Амур белый", "Амур чёрный", "Белоглазка", 
                "Белорыбица", "Белуга каспийская", "Белуга черноморская", "Бельдюга европейская", 
                "Берш", "Буффало большеротый", "Буффало чёрный", "Валёк", "Вобла", "Вырезуб", 
                "Вьюн", "Гимантолоф атлантический", "Голавль", "Голец Дрягина", "Голец Куорский", 
                "Голец Леванидова", "Голец арктический", "Голец сибирский-усач", "Гольян", 
                "Гольян озёрный", "Горбуша", "Гребешок исландский", "Густера", "Дрейссена речная", 
                "Елец", "Елец сибирский", "Ерш", "Ерш-носарь", "Жерех", "Зубатка полосатая", 
                "Зубатка пятнистая", "Зубатка синяя", "Калуга", "Кальмар обыкновенный", 
                "Камбала морская", "Камбала палтусовидная", "Камбала хоботная", "Карасекарп", 
                "Карась золотой", "Карась серебряный", "Карп Динкенбюльский голый", 
                "Карп Динкенбюльский зеркальный", "Карп Динкенбюльский линейный", 
                "Карп Кои Ёцусиро", "Карп Кои Кохаку", "Карп Кои Мамэсибори Госики", 
                "Карп Кои Наруми Асаги", "Карп Кои Орэндзи Огон", "Карп Кои Хи Уцури", 
                "Карп Супер Фрикс", "Карп голый", "Карп голый - альбинос", "Карп голый - призрак", 
                "Карп зеркальный", "Карп зеркальный - альбинос", "Карп зеркальный - призрак", 
                "Карп красный Старвас - зеркальный", "Карп красный Старвас - чешуйчатый", 
                "Карп линейный", "Карп линейный - альбинос", "Карп линейный - призрак", 
                "Карп рамчатый", "Карп рамчатый - альбинос", "Карп рамчатый - призрак", 
                "Карп чешуйчатый", "Карп чешуйчатый - альбинос", "Карп чешуйчатый - призрак", 
                "Катран", "Керчак европейский", "Кета", "Кижуч", "Колюшка девятииглая", 
                "Колюшка малая южная", "Колюшка трёхиглая", "Конгер", "Корюшка", 
                "Корюшка азиатская", "Краб камчатский", "Краб съедобный", "Краснопёр монгольский", 
                "Краснопёр-Угай крупночешуйчатый", "Краснопёрка", "Кунджа", "Кутум", 
                "Ленок острорылый", "Ленок тупорылый", "Лещ", "Лещ восточный", "Ликод Эсмарка", 
                "Ликод полуголый", "Линь", "Линь Квольсдорфский", "Линь золотистый", 
                "Лосось атлантический", "Лосось каспийский", "Лосось ладожский", "Лягушка", 
                "Макрель атлантическая", "Макрурус северный", "Мальма", "Менёк", "Мерланг", 
                "Мерлуза", "Меч-рыба", "Мидия", "Микижа", "Минога дальневосточная ручьевая", 
                "Минога каспийская", "Минога сибирская", "Минога трёхзубая", "Минога украинская", 
                "Мольва голубая", "Мольва обыкновенная", "Морской чёрт", "Муксун", "Налим", 
                "Нейва", "Нельма", "Нерка", "Окунь", "Окунь каменный", "Окунь морской золотистый", 
                "Окунь морской норвежский", "Окунь солнечный", "Окунь-клювач", "Омуль арктический", 
                "Омуль байкальский", "Опах краснопёрый", "Осётр балтийский", "Осётр восточносибирский", 
                "Осётр ладожский", "Осётр персидский", "Осётр русский", "Палия кряжевая", 
                "Палия лудожная", "Палия обыкновенная", "Палтус атлантический", "Палтус синекорый", 
                "Пелядь", "Перловица", "Пескарь обыкновенный", "Пескарь сибирский", "Пикша", 
                "Пинагор", "Плотва обыкновенная", "Плотва сибирская", "Подкаменщик сибирский", 
                "Подуст", "Поллак", "Пузанок каспийский", "Путассу северная", "Рак речной", 
                "Рипус", "Ротан", "Рыбец", "Ряпушка", "Ряпушка сибирская", "Сазан", "Сайда", 
                "Сайра атлантическая", "Сардина европейская", "Севрюга", "Сельдь Бражникова", 
                "Сельдь Кесслера", "Сельдь атлантическая", "Сельдь черноморская", "Сиг валаамский", 
                "Сиг волховский", "Сиг вуоксинский", "Сиг куорский", "Сиг ладожский озёрный", 
                "Сиг свирский", "Сиг чёрный", "Сиг-лудога", "Сиг-пыжьян", "Сима", "Сима жилая", 
                "Синец", "Скат колючий", "Скат полярный", "Сом", "Сом альбинос", "Сом амурский", 
                "Стерлядь", "Стерлядь сибирская", "Судак", "Таймень", "Тарань", "Толстолобик белый", 
                "Толстолобик пёстрый", "Треска атлантическая", "Тугун", "Тунец голубой", 
                "Тюлька черноморская", "Тюрбо", "Угорь", "Уклейка", "Усач альбинос", 
                "Усач короткоголовый", "Усач обыкновенный", "Устрица съедобная", "Форель озерная", 
                "Форель радужная", "Форель ручьевая", "Форель севанская", "Хариус восточносибирский", 
                "Хариус европейский", "Хариус западносибирский", "Химера европейская", 
                "Центролоф чёрный", "Чавыча", "Чехонь", "Чир", "Чукучан", "Шемая каспийская", 
                "Шемая черноморская", "Шип", "Щука обыкновенная", "Язь"
            ]
            self.fish_prices = {fish: round(random.uniform(0.1, 5.0), 1) for fish in fish_list}
            self.save_fish_prices()

    def save_fish_prices(self):
        with open("fish_prices.json", "w", encoding="utf-8") as f:
            json.dump(self.fish_prices, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10), padding=5)
        style.configure("TLabel", font=("Helvetica", 10), background="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")
        
        top_frame = ttk.Frame(self.root, padding=10, relief="flat")
        top_frame.pack(fill="x")
        
        ttk.Label(top_frame, text="Настройки цен (сер/г)", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        self.fish_combo = ttk.Combobox(top_frame, values=list(self.fish_prices.keys()), width=40, font=("Helvetica", 10))
        self.fish_combo.pack(side="left", padx=5)
        self.fish_combo.bind("<<ComboboxSelected>>", self.update_price_entry)
        self.price_entry = ttk.Entry(top_frame, width=10, font=("Helvetica", 10))
        self.price_entry.pack(side="left", padx=5)
        ttk.Button(top_frame, text="Обновить", command=self.update_price).pack(side="left", padx=5)
        
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill="x")
        
        self.start_button = ttk.Button(control_frame, text="Старт", command=self.start_scanning)
        self.start_button.pack(side="left", padx=5)
        self.stop_button = ttk.Button(control_frame, text="Стоп", command=self.stop_scanning, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        self.reset_button = ttk.Button(control_frame, text="Сброс списка", command=self.reset_catch_list)
        self.reset_button.pack(side="left", padx=5)
        self.save_button = ttk.Button(control_frame, text="Сохранить в HTML", command=self.save_to_html)
        self.save_button.pack(side="left", padx=5)
        
        # Выбор интервала сканирования
        ttk.Label(control_frame, text="Интервал сканирования (мс):").pack(side="left", padx=5)
        self.interval_combo = ttk.Combobox(control_frame, values=[50, 100, 250, 500, 1000], width=10, font=("Helvetica", 10))
        self.interval_combo.set("100")  # Значение по умолчанию
        self.interval_combo.pack(side="left", padx=5)
        self.interval_combo.bind("<<ComboboxSelected>>", self.update_scan_interval)
        
        self.status_label = ttk.Label(self.root, text="Сканирование остановлено", foreground="red", font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=5)
        
        self.tree = ttk.Treeview(self.root, columns=("Fish", "Weight", "Price", "Time"), show="headings", height=15)
        self.tree.heading("Fish", text="Рыба")
        self.tree.heading("Weight", text="Вес (г)")
        self.tree.heading("Price", text="Стоимость (сер)")
        self.tree.heading("Time", text="Время")
        self.tree.column("Fish", width=300, anchor="center")
        self.tree.column("Weight", width=100, anchor="center")
        self.tree.column("Price", width=150, anchor="center")
        self.tree.column("Time", width=100, anchor="center")
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.total_label = ttk.Label(self.root, text="Примерный фарм: 0 серебра", font=("Helvetica", 12, "bold"))
        self.total_label.pack(pady=5)
        
        # Нижний фрейм с четырьмя кнопками
        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(side="bottom", fill="x")
        ttk.Button(bottom_frame, text="Telegram", command=lambda: webbrowser.open("https://t.me/s1maby_rf4")).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="Поддержать", command=lambda: webbrowser.open("https://www.donationalerts.com/r/s1ma_by")).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="Другие реквизиты", command=self.show_other_support).pack(side="left", padx=5)
        ttk.Button(bottom_frame, text="Справка", command=self.show_help).pack(side="left", padx=5)
        
    def update_price_entry(self, event):
        selected_fish = self.fish_combo.get()
        if selected_fish in self.fish_prices:
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(self.fish_prices[selected_fish]))
        
    def update_price(self):
        selected_fish = self.fish_combo.get()
        try:
            new_price = float(self.price_entry.get())
            if selected_fish in self.fish_prices:
                self.fish_prices[selected_fish] = new_price
                self.save_fish_prices()
                self.update_table()
        except ValueError:
            pass
        
    def update_scan_interval(self, event):
        self.scan_interval = int(self.interval_combo.get())
        print(f"Интервал сканирования изменен на {self.scan_interval} мс")
        
    def start_scanning(self):
        if not self.scanning:
            self.scanning = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="Сканирование запущено", foreground="green")
            self.auto_scan()
        
    def stop_scanning(self):
        self.scanning = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Сканирование остановлено", foreground="red")
        
    def reset_catch_list(self):
        self.catch_list = []
        self.update_table()
        
    def save_to_html(self):
        if not self.catch_list:
            return
        
        html_content = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Список пойманной рыбы</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-color: #f0f0f0; }
                h1 { text-align: center; color: #333; }
                table { width: 80%; margin: 0 auto; border-collapse: collapse; background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
                th, td { padding: 10px; text-align: center; border: 1px solid #ddd; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                tr:hover { background-color: #f1f1f1; }
            </style>
        </head>
        <body>
            <h1>Список пойманной рыбы</h1>
            <table>
                <tr>
                    <th>Рыба</th>
                    <th>Вес (г)</th>
                    <th>Стоимость (сер)</th>
                    <th>Время</th>
                </tr>
        """
        
        for fish, weight, price, timestamp in self.catch_list:
            html_content += f"""
                <tr>
                    <td>{fish}</td>
                    <td>{weight}</td>
                    <td>{price:.2f}</td>
                    <td>{timestamp}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open("Рыболовный отчет.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Список сохранен в catch_list.html")
        
    def show_other_support(self):
        # Пример окна с другими реквизитами (можно дополнить)
        messagebox.showinfo("Другие реквизиты", "Поддержать проект можно через:\n\n"
                            "Карта RUB: 2204 1201 0282 2851 Срок действия 08/27\n"
                            "Карта BYN: 5392 1412 4805 9005 Срок действия 12/29\n"
                            "YooMoney: 410015203820295\n"
                            "Спасибо большое!")
        
    def show_help(self):
        # Мини-окно со справкой
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("400x500")
        help_window.configure(bg="#f0f0f0")
        
        help_text = """
        **Инструкция по использованию программы:**

        1. **Настройки цен**: Выберите рыбу из списка и обновите цену за грамм (сер/г).
        2. **Сканирование**: Нажмите "Старт" для начала автоматического сканирования экрана.
        3. **Интервал**: Выберите интервал сканирования (100, 250, 500, 1000 мс !!! 50 может вызвать нагрузку на ПК!!!).
        4. **Остановка**: Нажмите "Стоп" для остановки сканирования.
        5. **Сброс**: Очистите список пойманной рыбы кнопкой "Сброс списка".
        6. **Сохранение**: Сохраните список в HTML-файл кнопкой "Сохранить в HTML" Файл появится в папке с програмой.
        7. **Поддержка**: Используйте кнопки "Telegram", "Поддержать" и "Другие реквизиты" для связи и помощи проекту.

                Программа распознает текст в формате  
                             "Щука обыкновенная
                                1,23 кг / 123 см".
        """
        
        ttk.Label(help_window, text=help_text, font=("Helvetica", 10), background="#f0f0f0", wraplength=350).pack(pady=10, padx=10)
        ttk.Button(help_window, text="Закрыть", command=help_window.destroy).pack(pady=5)
        
    def check_colors(self, screenshot, scan_x, scan_y):
        img = screenshot.convert("RGB")
        width, height = img.size
        green_detected = False
        yellow_detected = False
        
        check_width = min(300, scan_x)
        check_region = img.crop((0, 0, check_width, height))
        
        for x in range(check_region.width):
            for y in range(check_region.height):
                r, g, b = check_region.getpixel((x, y))
                if g > 150 and r < 100 and b < 100:
                    green_detected = True
                if r > 150 and g > 150 and b < 100:
                    yellow_detected = True
        
        if green_detected and yellow_detected:
            return "(ТРОФ)"
        elif green_detected:
            return "(З)"
        return ""
        
    def scan_screen(self):
        screen_width, screen_height = pyautogui.size()
        scan_width = screen_width // 2
        scan_height = int(screen_height * 0.2)
        scan_x = (screen_width - scan_width) // 2
        scan_y = 0
        scan_region = (scan_x, scan_y, scan_width, scan_height)
        
        screenshot = pyautogui.screenshot(region=scan_region)
        suffix = self.check_colors(screenshot, scan_x, scan_y)
        
        try:
            text = pytesseract.image_to_string(screenshot, lang='rus')
            if not text:
                return
            print(f"Распознанный текст: {text}")
        except Exception as e:
            print(f"Ошибка OCR: {e}")
            return
        
        fish_types = list(self.fish_prices.keys())
        pattern = r"(" + "|".join(map(re.escape, fish_types)) + r")\s*\n\s*(\d+(?:,\d+)?)\s*(г|кг|kg)\s*/\s*(\d+)\s*см"
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            found_fish = match.group(1).strip()
            weight_str = match.group(2).replace(",", ".")
            unit = match.group(3).lower()
            
            display_fish = f"{found_fish} {suffix}".strip()
            weight = float(weight_str)
            if unit in ["кг", "kg"]:
                weight *= 1000
            
            self.add_catch(display_fish, int(weight))
        
    def auto_scan(self):
        if self.scanning:
            self.scan_screen()
            self.root.after(self.scan_interval, self.auto_scan)  # Используем выбранный интервал
        
    def add_catch(self, fish, weight):
        catch_key = f"{fish}_{weight}"
        if catch_key in [f"{item[0]}_{item[1]}" for item in self.catch_list]:
            return
        
        base_fish = fish.replace("(З)", "").replace("(ТРОФ)", "").strip()
        price = weight * self.fish_prices[base_fish]
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.catch_list.insert(0, (fish, weight, price, timestamp))
        self.tree.delete(*self.tree.get_children())
        for item in self.catch_list:
            self.tree.insert("", "end", values=(item[0], item[1], f"{item[2]:.2f}", item[3]))
        
        total = sum(item[2] for item in self.catch_list)
        self.total_label.config(text=f"Примерный фарм: ~{total:.2f} серебра")
        
    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        total = 0
        for fish, weight, _, timestamp in self.catch_list:
            base_fish = fish.replace("(З)", "").replace("(ТРОФ)", "").strip()
            price = weight * self.fish_prices[base_fish]
            total += price
            self.tree.insert("", "end", values=(fish, weight, f"{price:.2f}", timestamp))
        self.total_label.config(text=f"Примерный фарм: ~{total:.2f} серебра")

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingApp(root)
    root.mainloop()