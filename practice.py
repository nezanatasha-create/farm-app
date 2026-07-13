import json
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

class practice(MDApp):
    def load_crops(self):
        try:
            file=open("practice.json","r")
            self.crops=json.load(file)
            file.close()
        except:
            self.crops=[]
    def build(self):
        self.load_crops()
        layout=MDBoxLayout(
            orientation="vertical"
        )
        self.crop_input=MDTextField(
            hint_text="Enter crop"
        )
        self.crop_list=MDBoxLayout(
            orientation="horizontal"
        )
        button=MDRaisedButton(
            text="Add crop",
            on_release=self.button_pressed
        )
    
        layout.add_widget(self.crop_input)
        layout.add_widget(button)
        layout.add_widget(self.crop_list)
        
        return layout 
    def button_pressed(self,button):
        crop={"name":self.crop_input}
        self.crops.append(crop)
        self.load_crops()
        self.save_crops()
        
    def save_crops(self):
        file=open("practice.json", "w")
        json.dump(self.crop_input.text, file)
        file.close()
    
practice().run()