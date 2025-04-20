from Source.settings_view import SettingsView


from PIL import Image


from copy import deepcopy


class Filter:
    def __init__(self, image: Image.Image):
        self.name: str = "filter"
        self.image: Image.Image
        self.previous_image: Image.Image
        self.settings_view: SettingsView = SettingsView()
        self.settings_view.attach_filter(self)

    def hide_settings(self):
        self.settings_view.hide()

    def filter(self):
        self.image = self.image

    def execute(self, previous_img: Image.Image):
        self.previous_image = deepcopy(previous_img)
        self.image = deepcopy(previous_img)
        self.filter()
        self.settings_view.update_preview()
        self.settings_view.show()

    def update_settings(self):
        #setting: int = self.settings_view.slider.value()
        self.execute(self.previous_image)