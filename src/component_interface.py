from abc import ABC, abstractmethod


class ComponentInterface(ABC):
    @abstractmethod
    def refresh(self):
        pass

    def disable_button(self, button):
        button["state"] = "disable"

    def enable_button(self, button):
        button["state"] = "enable"
