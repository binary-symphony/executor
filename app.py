from textual.app import App, ComposeResult
from textual.widgets import RichLog, Input, Header, Footer
from textual.containers import Vertical
from typing import Callable, Dict

class Executor(App):
    
    
    
    KEY_BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    
    CSS = """
    
    Screen {
        background: rgb(10,10,10);
        color: rgb(200,200,200);
    }
    
    Header  {
        background: rgb(200,0,0);
        color: rgb(200,200,200);
    }
    
    Footer {
        background: rgb(200,0,0);
        color: rgb(200,200,200);
    }
    
    """
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header()
            yield RichLog(id="log")
            yield Input(placeholder="Enter command...", id="input")
            yield Footer()

    def on_mount(self):
        global model_context
        model_context = "" # Placeholder for actual context
        self.commands = {
            "help": self.cmd_HELP,
            "ASSERT": self.cmd_ASSERT,
            "VIEW": self.cmd_VIEW_CONTEXT,
            "RESET": self.cmd_RESET,
        }
        self.log_line("Executor started. Type 'help' for commands.\n")
    
    def log_line(self, text: str):
        log = self.query_one(RichLog)
        log.write(text)
    
    def on_input_submitted(self, event: Input.Submitted):
        cmd_line = event.value.strip()
        parts = cmd_line.split(maxsplit=1)
        cmd_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd_name in self.commands:
            self.commands[cmd_name](args)
            
        # Clear input
        event.input.value = ""
        
        
    def cmd_HELP(self, args: str):
        self.log_line("Available commands:\n")
        self.log_line("  ASSERT <text> - Append text to the selected model's local context.\n")
        self.log_line("  VIEW - Display the selected model's local context.\n")
        self.log_line("  RESET - Clear the selected model's local context.\n")
    
    def cmd_ASSERT(self, args: str):
        global model_context
        self.log_line(f"ASSERT: {args}")
        model_context = str(model_context) + args
    
    def cmd_RESET(self, args: str):
        global model_context
        model_context = ""
        self.log_line("Context reset.")
        
    def cmd_VIEW_CONTEXT(self, args: str):
        global model_context
        self.log_line(f"CONTEXT: {model_context}")
    
if __name__ == "__main__":
    Executor().run()