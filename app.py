from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from math import sqrt, pow


class CalculatorApp(App):
    def build(self):
        self.icon = "tax-calculate.png"
        self.operators = ['+', '-', '*', '/', '^', '%']
        self.last_was_operator = None
        self.last_button = None

        # Set window size and background color
        Window.size = (350, 550)
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Display
        self.solution = TextInput(
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            font_size=40,
            readonly=True,
            multiline=False,
            halign='right',
            padding=[10, 20],
            size_hint=(1, 0.2)
        )
        main_layout.add_widget(self.solution)

        # Buttons Layout
        buttons_layout = GridLayout(cols=4, spacing=10, size_hint=(1, 0.8))

        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('.', '0', 'C', '+'),
            ('√', '^', '%', '⌫'),
            ('CE', '(', ')', '=')
        ]

        for row in buttons:
            for label in row:
                button = Button(
                    text=label,
                    font_size=28,
                    background_color=(0.3, 0.3, 0.3, 1),
                    color=(1, 1, 1, 1),
                    size_hint=(1, 1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    background_normal='',
                    background_down='atlas://data/images/defaulttheme/button_pressed'
                )
                button.border_radius = [20, 20, 20, 20]
                button.bind(on_press=self.on_button_press)
                buttons_layout.add_widget(button)

        main_layout.add_widget(buttons_layout)
        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == 'C':
            self.solution.text = ''
        elif button_text == 'CE':
            self.solution.text = current[:-1] if current else ''
        elif button_text == '⌫':
            self.solution.text = current[:-1] if current else ''
        elif button_text == '=':
            self.calculate_result()
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                return
            elif current == '' and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text

        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def calculate_result(self):
        try:
            expression = self.solution.text
            # Replace '^' with '**' for power operation
            expression = expression.replace('^', '**')
            # Handle square root
            if '√' in expression:
                expression = expression.replace('√', 'sqrt')
            # Handle percentage
            if '%' in expression:
                expression = expression.replace('%', '/100')
            result = str(eval(expression))
            self.solution.text = result
        except Exception as e:
            self.solution.text = "Error"


if __name__ == '__main__':
    CalculatorApp().run()