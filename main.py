# main.py - Kivy Camera Application

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.logger import Logger
import os
from datetime import datetime

class CameraApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.camera_active = False
        
    def build(self):
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='📷 Camera App',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True
        )
        
        # Camera widget (initially hidden)
        self.camera = Camera(
            play=False,
            resolution=(640, 480),
            size_hint=(1, 0.7)
        )
        
        # Status label
        self.status_label = Label(
            text='Ready to take photos!',
            size_hint=(1, 0.1),
            font_size='16sp'
        )
        
        # Buttons layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            spacing=10
        )
        
        # Camera button
        self.camera_btn = Button(
            text='📷 Open Camera',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.camera_btn.bind(on_press=self.toggle_camera)
        
        # Capture button
        self.capture_btn = Button(
            text='📸 Take Photo',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.8, 0.2, 1),
            disabled=True
        )
        self.capture_btn.bind(on_press=self.capture_photo)
        
        # Add buttons to layout
        button_layout.add_widget(self.camera_btn)
        button_layout.add_widget(self.capture_btn)
        
        # Add all widgets to main layout
        self.main_layout.add_widget(title)
        self.main_layout.add_widget(self.camera)
        self.main_layout.add_widget(self.status_label)
        self.main_layout.add_widget(button_layout)
        
        return self.main_layout
    
    def toggle_camera(self, instance):
        """Toggle camera on/off"""
        try:
            if not self.camera_active:
                # Start camera
                self.camera.play = True
                self.camera_active = True
                self.camera_btn.text = '📵 Close Camera'
                self.camera_btn.background_color = (0.8, 0.2, 0.2, 1)
                self.capture_btn.disabled = False
                self.status_label.text = 'Camera is active. Ready to capture!'
                Logger.info("Camera: Camera started successfully")
            else:
                # Stop camera
                self.camera.play = False
                self.camera_active = False
                self.camera_btn.text = '📷 Open Camera'
                self.camera_btn.background_color = (0.2, 0.6, 0.8, 1)
                self.capture_btn.disabled = True
                self.status_label.text = 'Camera stopped.'
                Logger.info("Camera: Camera stopped")
                
        except Exception as e:
            self.show_error(f"Camera error: {str(e)}")
            Logger.error(f"Camera: Error toggling camera - {str(e)}")
    
    def capture_photo(self, instance):
        """Capture and save photo"""
        try:
            if not self.camera_active:
                self.show_error("Camera is not active!")
                return
            
            # Create photos directory if it doesn't exist
            photos_dir = '/storage/emulated/0/Pictures/CameraApp'
            if not os.path.exists(photos_dir):
                os.makedirs(photos_dir)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.png"
            filepath = os.path.join(photos_dir, filename)
            
            # Capture photo
            self.camera.export_to_png(filepath)
            
            # Update status
            self.status_label.text = f'Photo saved: {filename}'
            
            # Show success popup
            self.show_success(f"Photo saved successfully!\n\nLocation: {filepath}")
            
            Logger.info(f"Camera: Photo saved to {filepath}")
            
        except Exception as e:
            error_msg = f"Failed to capture photo: {str(e)}"
            self.show_error(error_msg)
            Logger.error(f"Camera: {error_msg}")
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(
            title='❌ Error',
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4),
            auto_dismiss=True
        )
        popup.open()
    
    def show_success(self, message):
        """Show success popup"""
        popup = Popup(
            title='✅ Success',
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4),
            auto_dismiss=True
        )
        popup.open()
        
        # Auto close after 3 seconds
        Clock.schedule_once(popup.dismiss, 3)

# Run the app
if __name__ == '__main__':
    CameraApp().run()


# buildozer.spec - Configuration for building APK

