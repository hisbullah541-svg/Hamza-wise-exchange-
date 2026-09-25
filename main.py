from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Set phone-friendly window size for testing
Window.size = (360, 640)

# Exchange rates relative to USD (Base)
RATES = {
    "USD ($)": 1.0,
    "EUR (€)": 0.92,
    "GBP (£)": 0.79,
    "NGN (₦)": 1550.0,
    "CAD ($)": 1.35
}

class RoundedBox(BoxLayout):
    """Custom layout with background color and rounded corners"""
    def __init__(self, bg_color=(0.15, 0.15, 0.2, 1), radius=15, **kwargs):
        super(RoundedBox, self).__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[self.radius])
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(text="[b]Hamza Wise Exchange[/b]", markup=True, font_size=24, size_hint_y=None, height=40, color=(1, 1, 1, 1))
        layout.add_widget(header)
        
        # Quick Balance Card
        card = RoundedBox(orientation='vertical', padding=15, spacing=10, size_hint_y=None, height=120, bg_color=(0.2, 0.3, 0.5, 1))
        card.add_widget(Label(text="Available Balance", font_size=14, color=(0.8, 0.8, 0.8, 1)))
        card.add_widget(Label(text="₦ 1,450,200.00", font_size=26, bold=True, color=(1, 1, 1, 1)))
        card.add_widget(Label(text="Security Status: Encrypted & Verified", font_size=12, color=(0.4, 1, 0.4, 1)))
        layout.add_widget(card)
        
        # Navigation Buttons
        btn_layout = GridLayout(cols=2, spacing=15, size_hint_y=None, height=220)
        
        btn_converter = Button(text="Currency\nConverter", background_color=(0.1, 0.6, 0.8, 1), font_size=16, bold=True)
        btn_converter.bind(on_press=lambda x: setattr(self.manager, 'current', 'converter'))
        
        btn_transfer = Button(text="Send &\nReceive", background_color=(0.2, 0.7, 0.3, 1), font_size=16, bold=True)
        btn_transfer.bind(on_press=lambda x: setattr(self.manager, 'current', 'transfer'))
        
        btn_profit = Button(text="Daily Income\nCalculator", background_color=(0.8, 0.5, 0.1, 1), font_size=16, bold=True)
        btn_profit.bind(on_press=lambda x: setattr(self.manager, 'current', 'profit'))
        
        btn_logout = Button(text="Lock Out /\nSecurity", background_color=(0.8, 0.2, 0.2, 1), font_size=16, bold=True)
        btn_logout.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        
        btn_layout.add_widget(btn_converter)
        btn_layout.add_widget(btn_transfer)
        btn_layout.add_widget(btn_profit)
        btn_layout.add_widget(btn_logout)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text="[b]Security Login[/b]", markup=True, font_size=28, color=(1,1,1,1), size_hint_y=None, height=50))
        
        self.pin_input = TextInput(text='', password=True, hint_text='Enter 4-Digit PIN', font_size=20, multiline=False, size_hint_y=None, height=50, halign='center')
        layout.add_widget(self.pin_input)
        
        btn_login = Button(text="Unlock App", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.8, 1), bold=True)
        btn_login.bind(on_press=self.verify_login)
        layout.add_widget(btn_login)
        
        self.msg_label = Label(text="", color=(1, 0.3, 0.3, 1), size_hint_y=None, height=30)
        layout.add_widget(self.msg_label)
        
        self.add_widget(layout)

    def verify_login(self, instance):
        if self.pin_input.text == "1234" or len(self.pin_input.text) == 4:  # Default sample validation
            self.manager.current = 'dashboard'
        else:
            self.msg_label.text = "Incorrect PIN. Try any 4 digits."

class ConverterScreen(Screen):
    def __init__(self, **kwargs):
        super(ConverterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="[b]Currency Converter[/b]", markup=True, font_size=22, size_hint_y=None, height=40))
        
        self.amount_input = TextInput(hint_text='Enter amount', font_size=18, multiline=False, size_hint_y=None, height=45)
        layout.add_widget(self.amount_input)
        
        self.from_spinner = Spinner(text='USD ($)', values=list(RATES.keys()), size_hint_y=None, height=45)
        layout.add_widget(self.from_spinner)
        
        self.to_spinner = Spinner(text='NGN (₦)', values=list(RATES.keys()), size_hint_y=None, height=45)
        layout.add_widget(self.to_spinner)
        
        btn_convert = Button(text="Convert Now", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.8, 1), bold=True)
        btn_convert.bind(on_press=self.convert_currency)
        layout.add_widget(btn_convert)
        
        self.result_label = Label(text="Result: --", font_size=20, bold=True, color=(0.4, 1, 0.4, 1))
        layout.add_widget(self.result_label)
        
        btn_back = Button(text="Back to Dashboard", size_hint_y=None, height=45, background_color=(0.4, 0.4, 0.4, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def convert_currency(self, instance):
        try:
            amt = float(self.amount_input.text)
            fr = self.from_spinner.text
            to = self.to_spinner.text
            
            # Convert to USD base first, then to target currency
            val_in_usd = amt / RATES[fr]
            final_val = val_in_usd * RATES[to]
            
            self.result_label.text = f"Converted: {final_val:,.2f} {to.split()[0]}"
        except ValueError:
            self.result_label.text = "Please enter a valid number!"

class TransferScreen(Screen):
    def __init__(self, **kwargs):
        super(TransferScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        layout.add_widget(Label(text="[b]Send & Receive Money[/b]", markup=True, font_size=22, size_hint_y=None, height=40))
        
        self.recipient_input = TextInput(hint_text='Recipient Account / ID', font_size=16, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.recipient_input)
        
        self.send_amount = TextInput(hint_text='Amount to Send', font_size=16, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.send_amount)
        
        btn_send = Button(text="Process Transfer (Calc Charges)", size_hint_y=None, height=45, background_color=(0.2, 0.7, 0.3, 1), bold=True)
        btn_send.bind(on_press=self.calculate_transfer)
        layout.add_widget(btn_send)
        
        self.info_label = Label(text="Charges: 1.5% + ₦100 flat fee", font_size=14, color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(self.info_label)
        
        self.summary_label = Label(text="", font_size=16, bold=True, color=(1, 1, 0.4, 1))
        layout.add_widget(self.summary_label)
        
        btn_back = Button(text="Back to Dashboard", size_hint_y=None, height=45, background_color=(0.4, 0.4, 0.4, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def calculate_transfer(self, instance):
        try:
            amt = float(self.send_amount.text)
            charge = (amt * 0.015) + 100.0  # 1.5% + 100 flat charges
            total_deduction = amt + charge
            self.summary_label.text = f"Charge: ₦{charge:,.2f} | Total Debit: ₦{total_deduction:,.2f}"
        except ValueError:
            self.summary_label.text = "Enter a valid amount to send!"

class ProfitCalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super(ProfitCalculatorScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        layout.add_widget(Label(text="[b]Daily Income Profit Calculator[/b]", markup=True, font_size=20, size_hint_y=None, height=40))
        
        self.capital_input = TextInput(hint_text='Total Daily Capital / Turnover', font_size=16, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.capital_input)
        
        self.margin_input = TextInput(hint_text='Average Profit Margin (%) e.g. 2.5', font_size=16, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.margin_input)
        
        btn_calc = Button(text="Calculate Daily Profit", size_hint_y=None, height=45, background_color=(0.8, 0.5, 0.1, 1), bold=True)
        btn_calc.bind(on_press=self.calculate_profit)
        layout.add_widget(btn_calc)
        
        self.profit_result = Label(text="Estimated Profit: ₦0.00", font_size=18, bold=True, color=(0.4, 1, 0.4, 1))
        layout.add_widget(self.profit_result)
        
        btn_back = Button(text="Back to Dashboard", size_hint_y=None, height=45, background_color=(0.4, 0.4, 0.4, 1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_back)
        
        self.add_widget(layout)

    def calculate_profit(self, instance):
        try:
            capital = float(self.capital_input.text)
            margin = float(self.margin_input.text)
            daily_profit = capital * (margin / 100.0)
            monthly_est = daily_profit * 30
            self.profit_result.text = f"Daily: ₦{daily_profit:,.2f}\nEst. Monthly: ₦{monthly_est:,.2f}"
        except ValueError:
            self.profit_result.text = "Please enter valid numbers!"

class WiseExchangeApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.14, 1)  # Dark theme background
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ConverterScreen(name='converter'))
        sm.add_widget(TransferScreen(name='transfer'))
        sm.add_widget(ProfitCalculatorScreen(name='profit'))
        return sm

if __name__ == '__main__':
    WiseExchangeApp().run()
