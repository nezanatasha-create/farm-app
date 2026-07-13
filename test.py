import json
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.scrollview import MDScrollView
class FarmApp(MDApp):
    
    def load_crops(self):
        try:
            file=open("crops.json","r")
            self.crops= json.load(file)
            file.close()
        except:
            self.crops=[]
    def save_crops(self):
        file=open("crops.json","w")
        json.dump(self.crops,file)
        file.close()
    def build(self):
        self.load_crops()
        self.edit_index=None
        layout=MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            padding="10dp"
        )
        self.dashboard=MDLabel(
            text="",
            halign="center",
            size_hint_y=None,
            height="90dp"
        )
        self.watering_label=MDLabel(
            text="",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
    
        self.crop_input= MDTextField(
            hint_text="Enter crop name"
        )
        self.quantity_input=MDTextField(
            hint_text="Enter quantity of crop"
        )
        self.date_input=MDTextField(
            hint_text="Enter planting date (YYYY-MM-DD)"
        )
        self.status_input=MDTextField(
            hint_text="Status (Planted/Growing/Harvested)"
        )
        self.last_watered_input=MDTextField(
            hint_text="last watered date(YYYY-MM-DD)"
        )
        self.watering_input=MDTextField(
            hint_text="Water every (days)"
        )
        
        self.harvest_input=MDTextField(
            hint_text="Expected harvest date (YYYY-MM-DD)"
        )
        self.crops_list=MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing="10dp"
        )
        self.crops_list.bind(
            minimum_height=self.crops_list.setter("height"))
        self.scroll=MDScrollView(
            size_hint_y=1
        )
        self.scroll.add_widget(self.crops_list)
        
        self.crop_button=MDRaisedButton(
            text="Add Crop",
            on_release=self.button_pressed
        )
        
        layout.add_widget(self.dashboard)
        layout.add_widget(self.watering_label)
        layout.add_widget(self.crop_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.status_input)
        layout.add_widget(self.last_watered_input)
        layout.add_widget(self.watering_input)
        layout.add_widget(self.harvest_input)
        layout.add_widget(self.crop_button)
        layout.add_widget(self.scroll)
        self.update_crop_display()
        return layout
    def button_pressed(self, button):
        crop={"name": self.crop_input.text,
              "quantity": self.quantity_input.text,
              "planting_date":self.date_input.text,
              "status":self.status_input.text,
              "last_watered":self.last_watered_input.text,
              "water_every":self.watering_input.text,
              "harvest_date":self.harvest_input.text}
        if self.edit_index==None:
            self.crops.append(crop)
        else:
            self.crops[self.edit_index]=crop
            self.edit_index=None
            self.crop_button.text="Add Crop"
        self.save_crops()
        self.update_crop_display()
        self.crop_input.text=""
        self.quantity_input.text=""
        self.date_input.text=""
        self.status_input.text=""
        self.last_watered_input.text=""
        self.watering_input.text=""
        self.harvest_input.text=""
    def update_dashboard(self):
        total=len(self.crops)
        planted=0
        growing=0
        harvested=0
        for crop in self.crops:
            status=crop.get('status','').lower()
            if status=="planted":
                planted+=1
            elif status=="growing":
                growing+=1
            elif status=="harvested":
                harvested+=1 
        self.dashboard.text=(
            f"Total crops: {total}\n"
            f"Planted: {planted}\n"
            f"Growing: {growing}\n"
            f"harvested: {harvested}\n"
            
        )
        self.update_watering_status()
    def update_watering_status(self):
        needs_water=[]
        for crop in self.crops:
            if crop.get("water_every",""):
                needs_water.append(crop['name'])
        if needs_water:
            self.watering_label.text=(
                "Check watering:\n"+
                ",".join(needs_water))
        else:
            self.watering_label.text="No watering reminders"       
                  
    def update_crop_display(self):
        self.crops_list.clear_widgets()
        for index, crop in enumerate(self.crops):
            row=MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="70dp"
            )
            crop_label=MDLabel(
                text=(crop['name']+"\nStatus: "+crop.get('status','Unknown')),
                size_hint_x=0.5)
            details_button=MDRectangleFlatButton(
                text="View Details",
                size_hint_x=0.2,
                on_release=lambda button, i=index:self.view_details(i)
            )
            delete_button=MDRectangleFlatButton(
                text="Delete",
                size_hint_x=0.2, 
                on_release=lambda button, i=index:self.delete_crop(i)
            )
            edit_button=MDRectangleFlatButton(
                text="Edit",
                size_hint_x=0.2,
                on_release=lambda button, i=index: self.edit_crop(i)
            )
            row.add_widget(crop_label)
            row.add_widget(details_button)
            row.add_widget(edit_button)
            row.add_widget(delete_button)
            self.crops_list.add_widget(row)
            self.update_dashboard()
    def delete_crop(self,index):
        self.crops.pop(index)
        self.save_crops()
        self.update_crop_display()
    def view_details(self,index):
        crop=self.crops[index]
        details=(
            f"Crop: {crop['name']}\n"
            f"Quantity: {crop['quantity']} units\n"
            f"Planted: {crop.get('planting_date','Unknown')}\n"
            f"Status: {crop.get('status','Unknown')}\n"
            f"Last watered: {crop.get('last_watered','Unknown')}\n"
            f"Water Every: {crop.get('water_every','Unknown')} days\n"
            f"Harvest date: {crop.get('harvest_date','Unknown')}"
        )
        self.dialog= MDDialog(
            title="Crop Details",
            text=details,
            buttons=[
                MDFlatButton(
                    text="Close",
                    on_release=lambda x:self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    def edit_crop(self,index):
        crop=self.crops[index]
        self.crop_input.text=crop["name"]
        self.quantity_input.text=crop["quantity"]
        self.date_input.text=crop["planting_date"]
        self.status_input.text=crop["status"]
        self.last_watered_input.text=crop.get("last_watered","")
        self.watering_input.text=crop.get("water_every","")
        self.harvest_input.text=crop.get("harvest_date","")
        self.edit_index=index
        self.crop_button.text="Update Crop"

FarmApp().run()

