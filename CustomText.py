import tkinter as tk
from tkinter import ttk

class CustomText(ttk.Entry):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        ttk.Entry.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.call("rename", self._w, self._orig)
        self.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.ttk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result