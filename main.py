#!/usr/bin/env python3
print("[INFO]: Khuushuur IME Starting up ...")
import gi
gi.require_version('IBus', '1.0')
from gi.repository import IBus, GLib

class Engine(IBus.Engine):
    def __init__(self):
        super().__init__() 
        self.bm = ""
        self.bt = ["", ""]
        self.map = {'f': 'ф', 'ts': 'ц', 'u': 'у', 'j': 'ж', 'e': 'э', 'n': 'н', 'g': 'г', 'sh': 'ш', "'u": 'ү', 'z': 'з', 'k': 'к', 'c': 'к', "''": 'ъ', 'ye': 'е', 'shch': 'щ', 'w': 'щ', "'i": 'й', 'ii': 'ы', 'b': 'б', "'o": 'ө', 'a': 'а', 'kh': 'х', 'h': 'х', 'r': 'р', 'o': 'о', 'l': 'л', 'd': 'д', 'p': 'п', 'ya': 'я', 'ch': 'ч', 'yo': 'ё', 's': 'с', 'm': 'м', 'i': 'и', 't': 'т', "'": 'ь', "i'": 'ь', 'v': 'в', 'yu': 'ю', "y": "я"}
        print("[INFO]: Khuushuur init sucees")

    def do_process_key_event(self, keyval, keycode, state):
        if state & (1 << 30):
            return False
        up = bool(state & (1 << 0)) or bool(state & (1 << 1)) or IBus.keyval_to_unicode(keyval).isupper()
        key = IBus.keyval_to_unicode(keyval)
            
        if keyval in (IBus.KEY_space, IBus.KEY_Return, IBus.KEY_Tab):
            self.commit_text(IBus.Text.new_from_string(self.bm))
            self.hide_preedit_text()
            self.bm = ""  
            self.bt = ["", ""]
            return False
        elif keyval ==  IBus.KEY_BackSpace:
             if self.bm.strip():
              del self.bt[1]
              self.bt.insert(0, "")
              self.bm = self.bm[:-1]
              self.bm += self.map.get("".join(self.bt), "")
              self.update_preedit_text(IBus.Text.new_from_string(self.bm), len(self.bm), True)
              return True
             else:
               return False
        del self.bt[0]
        self.bt.append(key)
        if "".join(self.bt) in self.map.keys():
            self.bm = self.bm[:-1]
            self.bm += self.map.get("".join(self.bt).lower(), key).upper() if up else self.map.get("".join(self.bt), key)
        else:
            self.bm += self.map.get(key.lower(), key).upper() if up else self.map.get(key, key)
        self.update_preedit_text(IBus.Text.new_from_string(self.bm), len(self.bm), True)
        return True
        
    def do_focus_in(self):
        self.bm = "" 
        self.bt = ["", ""]

    def do_focus_out(self):
        self.commit_text(IBus.Text.new_from_string(self.bm)) if self.bm.strip() else None
        self.bm = ""
        self.bt = ["", ""]

class Factory:
    def __init__(self):
        self.bus = IBus.Bus()
        self.factory = IBus.Factory.new(self.bus.get_connection())
        self.factory.add_engine("xkb:mn::ime", Engine)
        self.bus.request_name("org.freedesktop.IBus.KhuushuurIME", 0)

if __name__ == "__main__":
    IBus.init()
    factory = Factory()
    print("[INFO]: Khuushuur IME is going to loop ...")
    GLib.MainLoop().run()

