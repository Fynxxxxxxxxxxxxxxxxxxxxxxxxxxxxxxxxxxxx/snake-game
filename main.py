from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
import random
import webbrowser

Window.size = (412, 732)

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)
GREEN = (0, 1, 0, 1)
DARK_GREEN = (0, 0.7, 0, 1)
RED = (1, 0, 0, 1)
GRAY = (0.3, 0.3, 0.3, 1)
YELLOW = (1, 1, 0, 1)
PURPLE = (0.45, 0.54, 0.85, 1)
BODY_GREEN = (0, 0.78, 0.2, 1)
TAIL_GREEN = (0, 0.6, 0, 1)

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = AnchorLayout()
        box = BoxLayout(orientation='vertical', spacing=dp(20), size_hint=(0.8, 0.6))
        
        title = Label(text="Snake Game", font_size='48sp', bold=True, color=GREEN, size_hint=(1, 0.2))
        made_by = Label(text="Made by Fynx", font_size='28sp', color=WHITE, size_hint=(1, 0.15))
        
        discord_btn = Button(text="discord.gg/JYDyAaH2MY", font_size='22sp', color=PURPLE, 
                            background_color=(0,0,0,0), size_hint=(1, 0.1), underline=True)
        discord_btn.bind(on_press=lambda x: webbrowser.open("https://discord.gg/JYDyAaH2MY"))
        
        hint = Label(text="[color=#808080]Cham vao man hinh de choi[/color]", 
                    font_size='18sp', markup=True, size_hint=(1, 0.1))
        invite = Label(text="Tham gia Discord de cap nhat game moi!", 
                      font_size='14sp', color=GRAY, size_hint=(1, 0.1))
        
        start_btn = Button(text="", background_color=(0,0,0,0), size_hint=(1, 0.35))
        start_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'game'))
        
        for widget in [title, made_by, discord_btn, hint, invite, start_btn]:
            box.add_widget(widget)
        
        layout.add_widget(box)
        self.add_widget(layout)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

class GameOverScreen(Screen):
    victory = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = AnchorLayout()
        self.box = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(0.8, 0.7))
        
        self.title_label = Label(text="", font_size='42sp', bold=True, size_hint=(1, 0.2))
        self.sub_label = Label(text="", font_size='22sp', color=WHITE, size_hint=(1, 0.15))
        
        self.discord_btn = Button(text="discord.gg/JYDyAaH2MY", font_size='20sp', 
                                 color=PURPLE, background_color=(0,0,0,0), 
                                 size_hint=(1, 0.1), underline=True)
        self.discord_btn.bind(on_press=lambda x: webbrowser.open("https://discord.gg/JYDyAaH2MY"))
        
        self.hint_label = Label(text="Cham de choi lai", font_size='18sp', 
                               color=GRAY, size_hint=(1, 0.1))
        self.restart_btn = Button(text="", background_color=(0,0,0,0), size_hint=(1, 0.35))
        self.restart_btn.bind(on_press=self.restart_game)
        
        for widget in [self.title_label, self.sub_label, self.discord_btn, 
                      self.hint_label, self.restart_btn]:
            self.box.add_widget(widget)
        
        layout.add_widget(self.box)
        self.add_widget(layout)
    
    def on_enter(self):
        if self.victory:
            self.title_label.text = "Victory!!"
            self.title_label.color = YELLOW
            self.sub_label.text = "You have defeated the game by Fynx"
        else:
            self.title_label.text = "Game Over"
            self.title_label.color = RED
            self.sub_label.text = "Made by Fynx"
    
    def restart_game(self, instance):
        self.manager.current = 'game'
        self.manager.get_screen('game').game_widget.reset_game()

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GRID_COLS = 20
        self.GRID_ROWS = 30
        self.CELL_SIZE = dp(20)
        self.WIN_SCORE = 20
        self.reset_game()
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        Clock.schedule_interval(self.update, 0.1)
    
    def reset_game(self):
        self.snake = [
            [self.GRID_COLS//2, self.GRID_ROWS//2],
            [self.GRID_COLS//2 - 1, self.GRID_ROWS//2],
            [self.GRID_COLS//2 - 2, self.GRID_ROWS//2]
        ]
        self.direction = [1, 0]
        self.score = len(self.snake)
        self.game_over = False
        self.victory = False
        self._generate_food()
        self._update_canvas()
    
    def _generate_food(self):
        while True:
            self.food = [random.randint(0, self.GRID_COLS-1), 
                        random.randint(0, self.GRID_ROWS-1)]
            if self.food not in self.snake:
                break
    
    def _on_keyboard_closed(self):
        pass
    
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up' and self.direction != [0, 1]:
            self.direction = [0, -1]
        elif keycode[1] == 'down' and self.direction != [0, -1]:
            self.direction = [0, 1]
        elif keycode[1] == 'left' and self.direction != [1, 0]:
            self.direction = [-1, 0]
        elif keycode[1] == 'right' and self.direction != [-1, 0]:
            self.direction = [1, 0]
        return True
    
    def on_touch_down(self, touch):
        if self.game_over or self.victory:
            return
        
        cx, cy = self.width/2, dp(80)
        btn_size = dp(60)
        
        if cx - btn_size/2 < touch.x < cx + btn_size/2:
            if cy + btn_size/2 < touch.y < cy + btn_size*1.5 and self.direction != [0, 1]:
                self.direction = [0, -1]
            elif cy - btn_size*0.5 < touch.y < cy + btn_size/2 and self.direction != [0, -1]:
                self.direction = [0, 1]
        elif cx - btn_size*1.5 < touch.x < cx - btn_size/2 and \
             cy - btn_size/2 < touch.y < cy + btn_size/2 and self.direction != [1, 0]:
            self.direction = [-1, 0]
        elif cx + btn_size/2 < touch.x < cx + btn_size*1.5 and \
             cy - btn_size/2 < touch.y < cy + btn_size/2 and self.direction != [-1, 0]:
            self.direction = [1, 0]
    
    def update(self, dt):
        if self.game_over or self.victory:
            return
        
        head = self.snake[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        head[0] %= self.GRID_COLS
        head[1] %= self.GRID_ROWS
        
        if self.score >= self.WIN_SCORE:
            self.victory = True
            self.parent.parent.current = 'gameover'
            self.parent.parent.get_screen('gameover').victory = True
            return
        
        if head in self.snake:
            self.game_over = True
            self.parent.parent.current = 'gameover'
            self.parent.parent.get_screen('gameover').victory = False
            return
        
        self.snake.insert(0, head)
        
        if head == self.food:
            self.score += 1
            self._generate_food()
        else:
            self.snake.pop()
        
        self._update_canvas()
    
    def _update_canvas(self):
        self.canvas.clear()
        
        with self.canvas:
            Color(*BLACK)
            Rectangle(pos=(0, 0), size=(self.width, self.height))
            
            offset_x = (self.width - self.GRID_COLS * self.CELL_SIZE) / 2
            offset_y = self.height - self.GRID_ROWS * self.CELL_SIZE - dp(120)
            
            Color(0.08, 0.08, 0.08, 1)
            for x in range(self.GRID_COLS + 1):
                Line(points=[offset_x + x*self.CELL_SIZE, offset_y,
                            offset_x + x*self.CELL_SIZE, offset_y + self.GRID_ROWS*self.CELL_SIZE], width=1)
            for y in range(self.GRID_ROWS + 1):
                Line(points=[offset_x, offset_y + y*self.CELL_SIZE,
                            offset_x + self.GRID_COLS*self.CELL_SIZE, offset_y + y*self.CELL_SIZE], width=1)
            
            for i, segment in enumerate(self.snake):
                x = offset_x + segment[0]*self.CELL_SIZE
                y = offset_y + segment[1]*self.CELL_SIZE
                
                if i == 0:
                    Color(*DARK_GREEN)
                    Rectangle(pos=(x-2, y-2), size=(self.CELL_SIZE+4, self.CELL_SIZE+4))
                    if self.direction == [1, 0]:
                        Color(*WHITE)
                        Ellipse(pos=(x+self.CELL_SIZE-8, y+4), size=(6, 6))
                        Ellipse(pos=(x+self.CELL_SIZE-8, y+self.CELL_SIZE-10), size=(6, 6))
                        Color(*BLACK)
                        Ellipse(pos=(x+self.CELL_SIZE-6, y+6), size=(4, 4))
                        Ellipse(pos=(x+self.CELL_SIZE-6, y+self.CELL_SIZE-8), size=(4, 4))
                        Color(1, 0.2, 0.2, 1)
                        Line(points=[x+self.CELL_SIZE, y+self.CELL_SIZE/2,
                                    x+self.CELL_SIZE+8, y+self.CELL_SIZE/2], width=2)
                    elif self.direction == [-1, 0]:
                        Color(*WHITE)
                        Ellipse(pos=(x+2, y+4), size=(6, 6))
                        Ellipse(pos=(x+2, y+self.CELL_SIZE-10), size=(6, 6))
                        Color(*BLACK)
                        Ellipse(pos=(x+4, y+6), size=(4, 4))
                        Ellipse(pos=(x+4, y+self.CELL_SIZE-8), size=(4, 4))
                        Color(1, 0.2, 0.2, 1)
                        Line(points=[x, y+self.CELL_SIZE/2,
                                    x-8, y+self.CELL_SIZE/2], width=2)
                    elif self.direction == [0, -1]:
                        Color(*WHITE)
                        Ellipse(pos=(x+4, y+self.CELL_SIZE-8), size=(6, 6))
                        Ellipse(pos=(x+self.CELL_SIZE-10, y+self.CELL_SIZE-8), size=(6, 6))
                        Color(*BLACK)
                        Ellipse(pos=(x+6, y+self.CELL_SIZE-6), size=(4, 4))
                        Ellipse(pos=(x+self.CELL_SIZE-8, y+self.CELL_SIZE-6), size=(4, 4))
                        Color(1, 0.2, 0.2, 1)
                        Line(points=[x+self.CELL_SIZE/2, y+self.CELL_SIZE,
                                    x+self.CELL_SIZE/2, y+self.CELL_SIZE+8], width=2)
                    else:
                        Color(*WHITE)
                        Ellipse(pos=(x+4, y+2), size=(6, 6))
                        Ellipse(pos=(x+self.CELL_SIZE-10, y+2), size=(6, 6))
                        Color(*BLACK)
                        Ellipse(pos=(x+6, y+4), size=(4, 4))
                        Ellipse(pos=(x+self.CELL_SIZE-8, y+4), size=(4, 4))
                        Color(1, 0.2, 0.2, 1)
                        Line(points=[x+self.CELL_SIZE/2, y,
                                    x+self.CELL_SIZE/2, y-8], width=2)
                
                elif i == len(self.snake) - 1:
                    Color(*TAIL_GREEN)
                    Rectangle(pos=(x+4, y+4), size=(self.CELL_SIZE-8, self.CELL_SIZE-8))
                else:
                    Color(*BODY_GREEN)
                    Rectangle(pos=(x+1, y+1), size=(self.CELL_SIZE-2, self.CELL_SIZE-2))
            
            Color(*RED)
            fx = offset_x + self.food[0]*self.CELL_SIZE
            fy = offset_y + self.food[1]*self.CELL_SIZE
            Ellipse(pos=(fx+2, fy+2), size=(self.CELL_SIZE-4, self.CELL_SIZE-4))
            
            btn_cx = self.width/2
            btn_cy = dp(80)
            btn_size = dp(50)
            
            Color(0.3, 0.3, 0.3, 1)
            Rectangle(pos=(btn_cx-btn_size/2, btn_cy+btn_size/2), size=(btn_size, btn_size))
            Rectangle(pos=(btn_cx-btn_size/2, btn_cy-btn_size*1.5), size=(btn_size, btn_size))
            Rectangle(pos=(btn_cx-btn_size*1.5, btn_cy-btn_size/2), size=(btn_size, btn_size))
            Rectangle(pos=(btn_cx+btn_size/2, btn_cy-btn_size/2), size=(btn_size, btn_size))

class SnakeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(GameOverScreen(name='gameover'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()
