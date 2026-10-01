from sql import add_data, firstTime
# from ai import transcribe, gen_history, load_model

from rich.text import Text
from sql import searchInfo
from datetime import date, datetime, timezone, timedelta
# import threading
# import pyaudio
# import wave

from textual import on
from textual.screen import Screen
from textual.app import App
from textual.widgets import Button, Input, Header, Footer, Label, DataTable
from textual.validation import Validator

# load_thread = threading.Thread(target=load_model)
# load_thread.start()

class DateValidator(Validator):
     def validate(self, value):
        try:
            date.fromisoformat(value)
            return self.success()
        except ValueError:
            return self.failure("not a valid ISO date, use YYYY-MM-DD")

class GenderValidator(Validator):
    def validate(self, value):
        if value.lower().strip() == "m" or value.lower().strip() == "f":
            return self.success()
        else:
            return self.failure("Pick \"m\" or \"f\"")

class Data(Screen):

    BINDINGS = [("a", "add_screen", "Add patients"),
                # ("r", "record_screen", "Record")
                ]  

    def compose(self):
        yield Header()
        yield Label("Patients")
        yield DataTable()
        yield Footer()

    def on_mount(self):
        columns = [("id", "date", "name", "age", "sex", "bday", "history")]
        rows = searchInfo()
        self.title = "EMR"
        self.sub_title = "A TUI application"
        table = self.query_one(DataTable)
        table.add_columns(*columns[0])
        for row in rows:
            stylized_row = [
                Text(str(cell), style="bold", justify="center") for cell in row
                ]
            table.add_row(*stylized_row)

    def action_add_screen(self):
        self.app.push_screen(Add())

    # def action_record_screen(self):
    #     self.app.push_screen(Record())

class Add(Screen):

    BINDINGS = [("d", "data_screen", "Data"),
                # ("r", "record_screen", "Record"),
                ("escape", "unfocus", "Unfocus")]

    def action_data_screen(self):
        self.app.push_screen(Data())

    # def action_record_screen(self):
    #     self.app.push_screen(Record())

    def action_unfocus(self) -> None:
        self.app.set_focus(None)

    def compose(self):
        yield Header()
        yield Footer()
        yield Input(placeholder="Name", type="text", id="name", classes="input", validate_on="blur")
        yield Input(placeholder="Age", type="number", id="age", classes="input", validate_on="blur")
        yield Input(placeholder="Gender(m/f)", type="text", id="gender", classes="input", validators=[GenderValidator()], validate_on="blur")
        yield Input(placeholder="DOB(yyyy-mm-dd)", type="text", id="dob", classes="input", validators = [DateValidator()], validate_on="blur") 
        if "hist" not in globals():
            yield Input(placeholder="History", type="text", id="history", classes="input", validate_on="blur")
        # elif "hist" in globals():
        #     yield Input(value=hist, placeholder="History", type="text", id="history", classes="input", validate_on="blur")
        yield Button("Submit", id="submit")

    @on(Button.Pressed, "#submit")
    def submit(self):
        gender_input = self.query_one("#gender", Input)
        dob_input = self.query_one("#dob", Input)

        checks = [gender_input.validate(gender_input.value), dob_input.validate(dob_input.value)]
        if all(r.is_valid for r in checks):
            datee = datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat().split("T")[0]
            name = self.query_one("#name", Input).value
            age = self.query_one("#age", Input).value
            gender = self.query_one("#gender", Input).value
            dob = self.query_one("#dob", Input).value
            history = self.query_one("#history", Input).value
            add_data(datee, name, age, gender, dob, history)

            text_inputs = self.query(Input)
            for input in text_inputs:
                with input.prevent(Input.Changed):
                    input.value = ""
        else: 
            self.notify("You've put something wrong.", severity="error", timeout=10)

    def on_mount(self):
        self.title = "EMR"
        self.sub_title = "A TUI application"

# class Record(Screen):
#     BINDINGS = [("d", "data_screen", "Data"),
#                 ("a", "add_screen", "Add patients")]

#     def action_add_screen(self):
#         self.app.push_screen(Add())

#     def action_data_screen(self):
#         self.app.push_screen(Data())

#     def on_mount(self):
#             self.title = "EMR"
#             self.sub_title = "A TUI application"
#             self.click_count = 0
#             self.record_thread = None

#     def compose(self):
#         yield Button("Start recording", id="record")
#         yield Header()
#         yield Footer()
    
#     def record(self):
#         chunk = 1024
#         format = pyaudio.paInt16
#         channels = 2
#         rate = 44100
#         Output_Filename = "Recorded.wav"
    
#         p = pyaudio.PyAudio()
    
#         stream = p.open(format=format,
#                         channels=channels,
#                         rate=rate,
#                         input=True,
#                         input_device_index=12,
#                         frames_per_buffer=chunk)
    
#         frames = []
#         while self.click_count == 1:
#             data = stream.read(chunk, exception_on_overflow=False)  
#             frames.append(data) 
    
#         stream.stop_stream()
#         stream.close()
    
#         wf = wave.open(Output_Filename, 'wb')  
#         wf.setnchannels(channels)
#         wf.setsampwidth(p.get_sample_size(format))
#         wf.setframerate(rate)
#         wf.writeframes(b''.join(frames))
#         wf.close()
#         p.terminate()

#     def process_recording(self):
#         global hist
#         load_thread.join()
#         transcript = transcribe()
#         hist = gen_history(transcript)

#     @on(Button.Pressed)
#     def on_click(self, event: Button.Pressed):
#         global hist
#         if event.button.id == "record":
#             if self.click_count == 0:
#                 event.button.label = "Stop recording"
#                 self.click_count = 1
#                 self.record_thread = threading.Thread(target=self.record)
#                 self.record_thread.start()
#             else:
#                 self.click_count = 0
#                 event.button.label = "Start recording"

#                 self.record_thread.join()
#                 processing_thread = threading.Thread(target=self.process_recording)
#                 processing_thread.start()

class mainApp(App): 
     def on_mount(self):
          self.push_screen(Add())


app = mainApp()
app.run()