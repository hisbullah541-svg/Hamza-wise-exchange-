import hashlib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

# --- CYBERSECURITY UTILITIES ---
def hash_password(password: str) -> str:
    """Simulates secure password storage using SHA-256 hashing."""
    return hashlib.sha256(password.encode()).hexdigest()

# Simulated database containing user data (Username: Hashed Password)
# The password below is the SHA-256 hash for 'admin123'
USER_DATABASE = {
    "hamza": "240e90098224021d7b326cbba64157a419515ef82239d56bf70ed364a50ca531"
}


# --- SCREEN 1: SECURE LOGIN SCREEN ---
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text="SECURE LOGIN PORTAL", font_size='22sp', bold=True, color=(0, 0.6, 1, 1)))
        
        self.username_input = TextInput(hint_text="Username", multiline=False, font_size='16sp')
        layout.add_widget(self.username_input)
        
        # password_mask=True hides the characters as the user types (Security Best Practice)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False, font_size='16sp')
        layout.add_widget(self.password_input)
        
        login_btn = Button(text="Authenticate", font_size='16sp', bold=True, background_color=(0, 0.5, 0.8, 1))
        login_btn.bind(on_press=self.authenticate_user)
        layout.add_widget(login_btn)
        
        self.status_label = Label(text="", font_size='14sp', color=(1, 0, 0, 1))
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def authenticate_user(self, instance):
        username = self.username_input.text.strip().lower()
        password = self.password_input.text
        
        # 1. Input Sanity Check (Defense against empty/malicious fields)
        if not username or not password:
            self.status_label.text = "Error: Fields cannot be empty."
            return
            
        # 2. Secure Hash Verification
        input_hash = hash_password(password)
        if username in USER_DATABASE and USER_DATABASE[username] == input_hash:
            self.status_label.text = ""
            self.password_input.text = "" # Clear password buffer from memory
            self.manager.current = 'exchange' # Navigate to main screen
        else:
            self.status_label.text = "Access Denied: Invalid Credentials."


# --- SCREEN 2: EXCHANGE APPLICATION ---
class ExchangeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        layout.add_widget(Label(text="HAMZA WISE EXCHANGE", font_size='22sp', bold=True))
        
        self.input = TextInput(text="100", multiline=False, font_size='18sp')
        layout.add_widget(self.input)
        
        btn = Button(text="Convert USD to NGN", font_size='16sp', bold=True, background_color=(0, 0.7, 0.4, 1))
        btn.bind(on_press=self.convert)
        layout.add_widget(btn)
        
        self.result = Label(text="Result: 165,000 NGN", font_size='18sp')
        layout.add_widget(self.result)
        
        # Back door to log out safely
        logout_btn = Button(text="Secure Logout", font_size='12sp', size_hint_y=0.4)
        logout_btn.bind(on_press=self.logout)
        layout.add_widget(logout_btn)
        
        self.add_widget(layout)

    def convert(self, instance):
        # Input Validation & Exception Handling
        try:
            val = float(self.input.text)
            if val < 0:
                self.result.text = "Error: Amount cannot be negative."
                return
            if val > 100000000: # Mitigate overflow / ridiculous values
                self.result.text = "Error: Amount exceeds transaction limit."
                return
                
            self.result.text = f"Result: {val * 1650:,.0f} NGN"
        except ValueError:
            self.result.text = "Error: Input must be a valid number."

    def logout(self, instance):
        self.manager.current = 'login'


# --- CORE APP RUNNER ---
class WiseExchangeApp(App):
    def build(self):
        # The ScreenManager controls shifting between the login interface and the main UI
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ExchangeScreen(name='exchange'))
        return sm

if __name__ == '__main__':
    WiseExchangeApp().run()
