import asyncio
from prompt_toolkit import print_formatted_text, ANSI
from prompt_toolkit import Application
from prompt_toolkit.formatted_text import HTML, merge_formatted_text
from prompt_toolkit.layout.containers import VSplit, Window, HSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import FormattedTextControl
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import Frame, FormattedTextToolbar, Label
import subprocess
from subprocess import Popen
import sys

class convo_list_widget:
    def __init__(self, get_list, kb):
        self.selected_line = 0
        self.get_list = get_list
        self.kb = kb(widget=self)
        self.update_list()
        self.container = Window(
            content=FormattedTextControl(
                text=self._get_formatted_text,
                focusable=True,
                key_bindings=self.kb,
            ),
            style="class:select-box",
            cursorline=True,
            cursorcolumn=True,
            right_margins=[ScrollbarMargin(display_arrows=True), ],
            #width=20,
            #always_hide_cursor=False,
        )

    def update_list(self,*args,**kwargs):
        temp_list = self.get_list(*args,**kwargs)
        if temp_list is dict:
            temp_list = []
            for k,v in temp_list.values():
                temp_list.append((k,v))
        else:
            new_temp_list = []
            for item in temp_list:
                if item is not tuple:
                    new_temp_list.append((item,item))
            temp_list = new_temp_list
        self.list = temp_list

    def _get_formatted_text(self):
        show_list = []
        for i, item in enumerate(self.list):
            if i == self.selected_line:
                show_list.append([("[SetCursorPosition]", "")])
            show_list.append(ANSI(item[1]))
            show_list.append("\n")
        return merge_formatted_text(show_list)

    def __pt_container__(self):
        return self.container

def vi_list(widget=None,enter=None):
    kb = KeyBindings()

    @ kb.add('c-q')
    def exit_(event):
        event.app.exit()
    @ kb.add("k")
    def _go_up(event) -> None:
        widget.selected_line = (widget.selected_line - 1) % len(widget.list)
        app.output.hide_cursor()

    @ kb.add("j")
    def _go_down(event) -> None:
        widget.selected_line = (widget.selected_line + 1) % len(widget.list)
        app.output.hide_cursor()

    @ kb.add('enter')
    def _(event):
       # if enter is not None:
            
        print(widget.list[widget.selected_line][1])
 #       app.invalidate()
 #       lw.update_list()
    return kb
print(type(("\n".join(sys.argv[1:]))))
#make_list = lambda : ("\n".join(sys.argv[1:])).split(sep="\n")
command = sys.argv[1]
def call_cmd(command):
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = process.communicate()
    stdout = output[0]
    stderr = output[1]
#    proc = Popen(command, shell=True, stdout=subprocess.PIPE)
#    return proc.stdout.read().decode("utf-8").split("\n")
    return stdout.decode("utf-8").split("\n")
   # return stdout
make_list = lambda : call_cmd(command)

lw = convo_list_widget(make_list,vi_list)
root = HSplit([
    Label(text="Wifi Menu", width=10),
    lw,
])

app = Application(layout=Layout(root), refresh_interval=1 ,full_screen=True)
app.invalidate()
#app.run()
#app.on_invalidate = lw.update_list
async def main():
        # Define application.
   asyncio.ensure_future(ping())
   result = await app.run_async()


   print(result)


async def ping():
   while True:
       await asyncio.sleep(1)
       lw.update_list()
       app.invalidate()

asyncio.get_event_loop().run_until_complete(main())
#asyncio.get_event_loop().ensure_future(ping())
