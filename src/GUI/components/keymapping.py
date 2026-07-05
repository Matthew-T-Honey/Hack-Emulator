from PyQt6 import QtCore, QtGui, QtWidgets

class KeyMapping():
    def keyevent_to_int(event):
        special_char_mapping = {16777219:127,  #DEL
                            16777220:128,  #newline
                            16777219:129,  #backspace
                            16777234:130,  #leftarrow
                            16777235:131,  #uparrow
                            16777236:132,  #rightarrow
                            16777237:133,  #downarrow
                            16777232:134,  #home
                            16777233:135,  #end
                            16777238:136,  #pageup
                            16777239:137,  #pagedown
                            16777222:138,  #insert
                            16777223:139,  #delete
                            16777216:140,  #esc
                            16777264:141,  #f1
                            16777265:142,  #f2
                            16777266:143,  #f3
                            16777267:144,  #f4
                            16777268:145,  #f5
                            16777269:146,  #f6
                            16777270:147,  #f7
                            16777271:148,  #f8
                            16777272:149,  #f9
                            16777273:150,  #f10
                            16777274:151,  #f11
                            16777275:152,  #f12
                            }
        if event.key() < 128 and event.key() >= 32:
            return ord(event.text())
        elif event.key() in special_char_mapping:
            return special_char_mapping[event.key()]
        else:
            return 0
        
    def special_char_to_string(key):
        special_char_mapping = {32:"Space",
                            127:"Del",  #DEL
                            128:"Enter",  #newline
                            129:"BackSpace",  #backspace
                            130:"Left Arrow",  #leftarrow
                            131:"Up Arrow",  #uparrow
                            132:"Right Arrow",  #rightarrow
                            133:"Down Arrow",  #downarrow
                            134:"Home",  #home
                            135:"End",  #end
                            136:"PageUp",  #pageup
                            137:"PageDown",  #pagedown
                            138:"Insert",  #insert
                            139:"Delete",  #delete
                            140:"Esc",  #esc
                            141:"F1",  #f1
                            142:"F2",  #f2
                            143:"F3",  #f3
                            144:"F4",  #f4
                            145:"F5",  #f5
                            146:"F6",  #f6
                            147:"F7",  #f7
                            148:"F8",  #f8
                            149:"F9",  #f9
                            150:"F10",  #f10
                            151:"F11",  #f11
                            152:"F12",  #f12
                            }
        if key < 128 and key > 32:
            return chr(key)
        elif key in special_char_mapping:
            return special_char_mapping[key]
        else:
            return ""

