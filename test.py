import json
from datetime import datetime, timedelta
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
        self.dashboard_layout=MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height="120dp",
            spacing="5dp"
        )
        self.dashboard=MDLabel(
            text="",
            halign="center",
            
        )
        self.dashboard_layout.add_widget(self.dashboard)
    
        self.watering_label=MDLabel(
            text="",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        self.filter_layout=MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_x=None,
            size_hint_y=None,
            height="50dp"
        )
        self.filter_layout.bind(
            minimum_width=self.filter_layout.setter("width")
        )
        self.filter_scroll=MDScrollView(
            do_scroll_y=False,
            size_hint_y=None,
            height="50dp"
        )
        self.filter_scroll.add_widget(self.filter_layout)
        all_button=MDRectangleFlatButton(
            text="All",
            on_release=lambda x: self.set_filter("all")
        )
        water_button=MDRectangleFlatButton(
            text="Needs Water",
            on_release=lambda x:self.set_filter("water")
        )
        planted_button=MDRectangleFlatButton(
            text="Planted",
            on_release=lambda x: self.set_filter("planted")
        )
        growing_button=MDRectangleFlatButton(
            text="Growing",
            on_release=lambda x: self.set_filter("growing")
        )
        harvested_button=MDRectangleFlatButton(
            text="Harvested",
            on_release=lambda x: self.set_filter("harvested")
        )

        self.current_filter="all"
        
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
            on_release=self.open_add_crop_dialog
        )
        

        self.filter_layout.add_widget(all_button)
        self.filter_layout.add_widget(water_button)
        self.filter_layout.add_widget(growing_button)
        self.filter_layout.add_widget(planted_button)
        self.filter_layout.add_widget(harvested_button)

        layout.add_widget(self.dashboard_layout)
        layout.add_widget(self.watering_label)
        layout.add_widget(self.filter_scroll)
        layout.add_widget(self.crop_button)
        layout.add_widget(self.scroll)
        self.update_crop_display()
        return layout
    def set_filter(self,filter_name):
        self.current_filter=filter_name
        self.update_crop_display()
    def open_add_crop_dialog(self,*args):
        content=MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="500dp"
        )
        self.dialog_crop_input= MDTextField(
            hint_text="Enter crop name"
        )
        self.dialog_quantity_input=MDTextField(
            hint_text="Enter quantity of crop"
        )
        self.dialog_date_input=MDTextField(
            hint_text="Enter planting date (YYYY-MM-DD)"
        )
        self.dialog_status_input=MDTextField(
            hint_text="Status (Planted/Growing/Harvested)"
        )
        self.dialog_last_watered_input=MDTextField(
            hint_text="last watered date(YYYY-MM-DD)"
        )
        self.dialog_watering_input=MDTextField(
            hint_text="Water every (days)"
        )
        
        self.dialog_harvest_input=MDTextField(
            hint_text="Expected harvest date (YYYY-MM-DD)"
        )
        content.add_widget(self.dialog_crop_input)
        content.add_widget(self.dialog_quantity_input)
        content.add_widget(self.dialog_date_input)
        content.add_widget(self.dialog_status_input)
        content.add_widget(self.dialog_last_watered_input)
        content.add_widget(self.dialog_watering_input)
        content.add_widget(self.dialog_harvest_input)

        self.dialog=MDDialog(
            title="Add crop",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Save",
                    on_release=lambda x:self.save_from_dialog()
                ),
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x:self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    def save_from_dialog(self):
        crop={"name": self.dialog_crop_input.text,
              "quantity": self.dialog_quantity_input.text,
              "planting_date":self.dialog_date_input.text,
              "status":self.dialog_status_input.text,
              "last_watered":self.dialog_last_watered_input.text,
              "water_every":self.dialog_watering_input.text,
              "harvest_date":self.dialog_harvest_input.text}
        if self.edit_index==None:
            self.crops.append(crop)
        else:
            self.crops[self.edit_index]=crop
            self.edit_index=None
            
        self.save_crops()
        self.update_crop_display()
        self.dialog.dismiss()
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
        #self.crop_input.text=""
        #self.quantity_input.text=""
        #self.date_input.text=""
        #self.status_input.text=""
        #self.last_watered_input.text=""
        #self.watering_input.text=""
        #self.harvest_input.text=""
    def update_dashboard(self):
        total=len(self.crops)
        planted=0
        growing=0
        harvested=0
        harvest_soon=len(self.get_crops_harvesting_soon())
        for crop in self.crops:
            status=crop.get('status','').lower()
            if status=="planted":
                planted+=1
            elif status=="growing":
                growing+=1
            elif status=="harvested":
                harvested+=1 
        needs_water= len(self.get_crops_needing_water())
        self.dashboard.text=(
            f"Total crops: {total}\n"
            f"Planted: {planted}\n"
            f"Growing: {growing}\n"
            f"Harvested: {harvested}\n"
            f"Need water: {needs_water}\n"
            f"Harvest soon: {harvest_soon}"
        )
        self.update_watering_status()
    def get_crops_needing_water(self):
        needs_water=[]
        today=datetime.today().date()
        for crop in self.crops:
            try:
                last_watered=datetime.strptime(
                    crop["last_watered"],
                    "%Y-%m-%d"
                ).date()
                water_every=int(crop["water_every"])
                next_watering=last_watered+timedelta(days=water_every)
                if today>=next_watering:
                    needs_water.append(crop["name"])
            except:
                pass
        return needs_water
    def get_crops_harvesting_soon(self):
        harvest_soon=[]
        today=datetime.today().date()
        for crop in self.crops:
            try:
                harvest_date=datetime.strptime(
                    crop["harvest_date"],"%Y-%m-%d"
                ).date()
                days_left=(harvest_date-today).days
                if 0 <=days_left<=7:
                    harvest_soon.append(crop["name"])
            except:
                pass
        return harvest_soon
    def update_watering_status(self):
        needs_water=self.get_crops_needing_water()
        today=datetime.today().date()

        if needs_water:
            self.watering_label.text=(
                "Water today:\n"+
                ",".join(needs_water))
        else:
            self.watering_label.text="No watering reminders"       
    def get_crop_progress(self,crop):
        try:
            today=datetime.today().date()
            planted=datetime.strptime(
                crop['planting_date'],"%Y-%m-%d"
            ).date()
            days_growing=(today-planted).days
            return f"Growing for: {days_growing} days"
        except:
            return "Growing time unavailable"
    def get_harvest_countdown(self, crop):
        try:
            today=datetime.today().date()
            harvest=datetime.strptime(
                crop['harvest_date'],"%Y-%m-%d"
            ).date()
            days_left=(harvest-today).days
            if days_left<0:
                return "Harvest date passed"
            elif days_left==0:
                return "Harvest today!"
            else:
                return f"Harvest in: {days_left} days"
        except:
            return "Harvest date unavailable"
    def update_crop_display(self):
        self.crops_list.clear_widgets()
        for index, crop in enumerate(self.crops):
            if self.current_filter=="water":
                if crop['name'] not in self.get_crops_needing_water():
                    continue
            elif self.current_filter=="growing":
                if crop.get("status","").lower() !="growing":
                    continue
            elif self.current_filter=="planted":
                if crop.get("status","").lower()!="planted":
                    continue
            elif self.current_filter=="harvested":
                if crop.get("status","").lower()!="harvested":
                    continue
            row=MDBoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height="160dp",
                padding="10dp",
                spacing="5dp"
            )
            crop_label=MDLabel(
                text=(crop['name']
                      +"\nStatus: "
                      +crop.get('status','Unknown')
                      +"\nQuantity "
                      +crop.get("quantity","Unknown")
                      ), 
                size_hint_y=None,
                height="100dp")
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
            water_button=MDRectangleFlatButton(
                text="Water",
                size_hint_x=0.2,
                on_release=lambda button, i = index:self.mark_watered(i)
            )
            buttons_layout=MDBoxLayout(
                orientation="vertical",
                spacing="5dp",
                size_hint_y=None,
                height="80dp"

            )
            top_buttons=MDBoxLayout(
                orientation="horizontal",
                spacing="10dp",
                size_hint_y=None,
                height="40dp"
            )
            bottom_buttons=MDBoxLayout(
                orientation="horizontal",
                spacing="10dp",
                size_hint_y=None,
                height="40dp"
            )
            top_buttons.add_widget(details_button)
            top_buttons.add_widget(edit_button)
            bottom_buttons.add_widget(delete_button)
            bottom_buttons.add_widget(water_button)

            buttons_layout.add_widget(top_buttons)
            buttons_layout.add_widget(bottom_buttons)
            row.add_widget(crop_label)
            row.add_widget(buttons_layout)
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
            f"{self.get_crop_progress(crop)}\n"
            f"{self.get_harvest_countdown(crop)}\n"
            f"Harvest date: {crop.get('harvest_date','Unknown')}\n"
            
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
        self.edit_index=index
        self.open_add_crop_dialog()
        self.dialog_crop_input.text=crop["name"]
        self.dialog_quantity_input.text=crop["quantity"]
        self.dialog_date_input.text=crop["planting_date"]
        self.dialog_status_input.text=crop["status"]
        self.dialog_last_watered_input.text=crop.get("last_watered","")
        self.dialog_watering_input.text=crop.get("water_every","")
        self.dialog_harvest_input.text=crop.get("harvest_date","")
    def mark_watered(self,index):
        today=datetime.today().strftime("%Y-%m-%d")
        self.crops[index]["last_watered"]=today
        self.save_crops()
        self.update_crop_display()
        

FarmApp().run()

