from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from win32api import GetSystemMetrics
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.uix.dropdown import DropDown
from kivy.graphics import Rectangle, Color

Window.size = (GetSystemMetrics(0) * .4, GetSystemMetrics(1) * .5)
Window.top = GetSystemMetrics(0) * .15
Window.left = GetSystemMetrics(1) * .5

Builder.load_file('Assets/design.kv')


class MainHome(Screen):
    todo_views = ObjectProperty(None)
    layout_main = ObjectProperty(None)
    header_id = ObjectProperty(None)
    todo_tabbed1 = ObjectProperty(None)
    todo_tabbed2 = ObjectProperty(None)
    add_btn_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainHome, self).__init__(**kwargs)
        Clock.schedule_once(self.start)

    dropdowns = []

    def start(self, event):
        self.todo_views.clear_widgets()
        self.dropdowns.clear()

        theme_file = open('Assets/colors.txt', 'r')
        color_theme = [i.replace('\n', '') for i in theme_file]
        bg_theme = color_theme[0].split(',')
        header1 = color_theme[1].split(',')
        button_clr = color_theme[2].split(',')
        task1 = color_theme[3].split(',')
        task2 = color_theme[4].split(',')
        task_font = color_theme[5].split(',')

        self.layout_main.canvas.before.add(Color(int(bg_theme[0])/255, int(bg_theme[1])/255, int(bg_theme[2])/255, 1, mode='rgba'))
        self.layout_main.canvas.before.add(Rectangle(pos=(0, 0), size=(Window.width, Window.height)))

        self.header_id.canvas.get_group('a')[0].rgba = (int(header1[0])/255, int(header1[1])/255, int(header1[2])/255, 1)

        self.todo_tabbed1.background_color = (int(button_clr[0])/100, int(button_clr[1])/100, int(button_clr[2])/100, 1)
        self.todo_tabbed2.background_color = (int(button_clr[0]) / 100, int(button_clr[1]) / 100, int(button_clr[2]) / 100, 1)
        self.add_btn_id.background_color = (int(button_clr[0]) / 100, int(button_clr[1]) / 100, int(button_clr[2]) / 100, 1)

        todo_grid = GridLayout(cols=1, spacing=20, size_hint_y=None, size=(self.size[0], self.size[1]))
        todo_grid.bind(minimum_height=todo_grid.setter('height'))

        tasks_stored = open('Assets/tasks.txt', 'r')
        tasks_list = [i.replace('\n', '').split('^') for i in tasks_stored]

        index = 0
        num = 0
        rectangles = []
        for i in reversed(tasks_list):
            todos_row = GridLayout(cols=2, size_hint_y=None, spacing=0)
            todos_row.bind(minimum_height=todos_row.setter('height'))

            task_lbl = Label(text=i[0], size_hint_y=None,
                             text_size=(Window.width * 0.6, None), halign='center',
                             valign='middle', size_hint_x=0.75, color=(int(task_font[0])/255, int(task_font[1])/255, int(task_font[2])/255, 1))

            status_dropdown = DropDown()
            del_btn = Button(text='Delete', size_hint_y=None, text_size=(self.width, 40), halign='center',
                             valign='center', height=Window.size[1] * 0.08)
            update_btn = Button(text='Update', size_hint_y=None, text_size=(self.width, 40), halign='center',
                                valign='center', height=Window.size[1] * 0.08)
            update_btn.bind(on_press=partial(self.update_stat, i[1], task_lbl, status_dropdown))
            del_btn.bind(on_press=partial(self.delete_task, task_lbl, i[1], status_dropdown))
            status_dropdown.add_widget(update_btn)
            status_dropdown.add_widget(del_btn)
            self.dropdowns.append(status_dropdown)

            status_holder = BoxLayout(orientation='vertical', size_hint_x=0.215)
            status_lbl = Button(text='Options', valign='center', background_color=(int(button_clr[0]) / 100, int(button_clr[1]) / 100, int(button_clr[2]) / 100, 1))
            status_lbl.bind(on_release=self.dropdowns[index].open)

            status_text = Label(text=i[1], valign='middle', color=(int(task_font[0])/255, int(task_font[1])/255, int(task_font[2])/255, 1))
            status_holder.add_widget(status_text)
            status_holder.add_widget(status_lbl)

            index += 1

            todos_row.add_widget(task_lbl)
            todos_row.add_widget(status_holder)
            todo_grid.add_widget(todos_row)

            if i[1] == 'Done':
                rectangles.append('Done')

            else:
                rectangles.append('Ongoing')

            num += todos_row.height + todo_grid.spacing[1]

        for i in rectangles:
            num -= todos_row.height + todo_grid.spacing[1]
            if i == 'Done':
                todo_grid.canvas.before.add(Color(int(task1[0])/255, int(task1[1])/255, int(task1[2])/255, 1, mode='rgba'))
                todo_grid.canvas.before.add(Rectangle(size=(Window.width, todos_row.height), pos=(0, num)))
            else:
                todo_grid.canvas.before.add(Color(int(task2[0])/255, int(task2[1])/255, int(task2[2])/255, 1, mode='rgba'))
                todo_grid.canvas.before.add(Rectangle(size=(Window.width, todos_row.height), pos=(0, num)))

        self.todo_views.add_widget(todo_grid)
        tasks_stored.close()

    popup = Popup(title='Add task', size_hint=(None, None), size=(400, 400))

    def open_task_add(self):
        popup_grid = BoxLayout(orientation='vertical', spacing=10)
        task_input = TextInput(size_hint_y=0.5)
        submit_btn = Button(text='Add', size_hint_y=0.2)
        submit_btn.bind(on_release=partial(self.add_task, task_input))

        popup_grid.add_widget(BoxLayout(size_hint_y=0.15))
        popup_grid.add_widget(task_input)
        popup_grid.add_widget(submit_btn)
        popup_grid.add_widget(BoxLayout(size_hint_y=0.15))
        self.popup.content = popup_grid
        self.popup.open()

    def add_task(self, task_input, event):
        print(task_input.text)
        tasks_stored = open('Assets/tasks.txt', 'a')
        tasks_stored.write(task_input.text + '^Ongoing\n')
        tasks_stored.close()
        task_input.text = ''
        self.start(None)

    def delete_task(self, task, status, dropdown, event):
        print(task.text)
        print(status)
        dropdown.dismiss()

        with open("Assets/tasks.txt", "r") as f:
            accounts = f.readlines()
        with open("Assets/tasks.txt", "w") as f:
            for account in accounts:
                if account.strip("\n") != task.text + '^' + status:
                    f.write(account)
        self.start(None)

    def update_stat(self, status, task, dropdown, event):
        print('Status being updated.', status)
        print(task.text)
        if status == 'Done':
            changed_stat = 'Ongoing'
        else:
            changed_stat = 'Done'
        print(changed_stat)

        with open("Assets/tasks.txt", "r") as f:
            accounts = f.readlines()
        with open("Assets/tasks.txt", "w") as f:
            for account in accounts:
                if account.strip("\n") == task.text + '^' + status:
                    f.write(task.text + '^' + changed_stat + '\n')
                else:
                    f.write(account)
        dropdown.dismiss()
        self.start(None)

    def lavie(self):
        print('Lavie en Rose - Theme')
        with open("Assets/colors.txt", "w") as f:
            f.write('50,13,62,1\n')
            f.write('255,100,200,1\n')
            f.write('77,81,152,1\n')
            f.write('217,2,238,1\n')
            f.write('241,98,255,1\n')
            f.write('0,0,0,1\n')
        self.start(None)

    def efficascent(self):
        print('Efficascent - Theme')
        with open("Assets/colors.txt", "w") as f:
            f.write('32,30,32,1\n')
            f.write('29,60,69,1\n')
            f.write('29,60,69,1\n')
            f.write('221,195,165,1\n')
            f.write('224,169,109,1\n')
            f.write('0,0,0,1\n')
        self.start(None)

    def blue_acad(self):
        print('Blue Academy - Theme')
        with open("Assets/colors.txt", "w") as f:
            f.write('245,240,225,1\n')
            f.write('30,61,89,1\n')
            f.write('30,61,89,1\n')
            f.write('255,110,64,1\n')
            f.write('255,193,59,1\n')
            f.write('0,0,0,1\n')
        self.start(None)

class DoTrackR(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainHome(name='home'))
        return sm


if __name__ == '__main__':
    DoTrackR().run()
