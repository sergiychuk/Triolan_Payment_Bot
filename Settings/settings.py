# -*- coding: utf-8 -*-
# region ──────────╼[ IMPORT ]╾──────────
import json
# endregion

class Settings:
    # region ───╼[ Constructor ]╾───
    def __init__(self):
        self._debug_mode = False
    # endregion

    # region ───╼[ Properties ]╾───
    # region [ Debug Mode ]
    @property
    def debug_mode(self):
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value: bool):
        self._debug_mode = value
    # endregion

    # endregion
