from src.GUI.hack_gui import HACK_GUI

if __name__ == "__main__":

    gui = HACK_GUI()
    

    # file = open("tests/test_files/collatztest.txt", "r")
    # lines = file.readlines()
    # filelines = ("").join(lines)
    # file.close()

    # gui.ui.Code_view.setText(filelines)

    gui.open_window()