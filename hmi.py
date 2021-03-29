import curses
import logging

import shared_cfg
import hardware

# Order of encoder values for each direction
CW_ORDER = [1, 3, 0, 2]
CCW_ORDER = [2, 0, 3, 1]
TICKS_PER_STEP = float(2)


# Button label positions are determined empirically and are dependent on
# character resolution.
# Dictionary key is max x character position.
BTN_LABEL_X_POS = {
    40: [1, 13, 24, 35],
    120: [3, 15, 26, 37]
}


# Maps TFT hard button ID to the action it performs. Button 1 is left-most.
class ButtonAction:
    BACK = 1
    EDIT = 2
    BUTTON_3 = 3
    LOCK = 4


# Maps button ID to UI text
HW_BTN_LABEL = {
    ButtonAction.EDIT: "EDIT",
    ButtonAction.LOCK: "LOCK",
    ButtonAction.BACK: "BACK",
    ButtonAction.BUTTON_3: "BUTT 3"
}


# Color pair IDs
class ColorPair:
    NORMAL = 1
    SELECTED = 2
    NO_DATA = 3
    NO_DATA_SELECTED = 4
    TITLE = 5


log = logging.getLogger(__name__)


class Extent:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def span(self):
        return self.max - self.min + 1


def send_string_to_hardware(text):
    if text and len(text) > 0:
        hardware.keyboard_out(text)
    else:
        log.debug("Not sending empty string to hardware.")


class StoreNavigator:
    """Renders current view of password store"""
    def __init__(self, min_col, min_row, max_col, max_row):
        self.level = "/"
        self.entry = None
        self.level_container = None # Container of current_level
        self.selection = 0  # index of current selection
        self.top_row_index = 0    # index of top visible row
        self.parent_info_row = min_row
        self.col_extent = Extent(min_col, max_col)
        self.row_extent = Extent(min_row+1, max_row) # Eat one row for parent
        self.level_container_names = []
        self.level_entry_names = []
        log.debug("New navigator: min_row: {0}  max_row: {1}  vis_rows: {2}\n"
                  "min_col: {3}  max_col: {4}  vis_cols: {5}"
                  .format(min_row, max_row, self.row_extent.span(),
                          min_col, max_col, self.col_extent.span()))
        self.entry_actions = []
        # Each action tuple holds the UI text and the corresponding Credential class
        # function that should be invoked on an Credential instance to get the
        # string that should be sent via the USB keyboard device for the action.
        # For example, the "Send password" action invokes "get_password()" on
        # the currently-selected Credential, and outputs the result to the USB
        # keyboard device.
        self.entry_actions.append(["Send password", "get_password"])
        self.entry_actions.append(["Send username", "get_username"])
        self.entry_actions.append(["Send URL", "get_url"])
        self.change_level(0)
        self.back_stack = []

    def get_entry_action_text(self, index):
        """
        For the Credential indicated by self.level, return the result of invoking the
        Credential member function for the action at index.
        :param index: Index into self.entry_actions, which selects the function
        to be invoked on the currently-selected Credential.
        :return: A string or None.
        """
        action = self.entry_actions[index][1]
        _, entry = shared_cfg.master_store.get_entry_by_path(self.level)
        return getattr(entry, action)()

    def perform_entry_action(self):
        log.debug("Performing action '{0}' for '{1}'"
                  .format(self.get_selection()[0], self.level))
        try:
            send_string_to_hardware(self.get_entry_action_text(self.selection))
        except Exception as ex:
            log.critical("Action '{0}' failed for entry '{1}': {2}"
                         .format(self.selection, self.level, str(ex)))

    def change_level(self, direction):
        if self.entry and direction < 0:
            self.perform_entry_action()
            return

        went_back = False
        self.entry = None
        if direction < 0: # Drilling down to the currently-selected level/entry
            name, is_cont = self.get_selection()
            self.back_stack.append([self.selection, self.top_row_index])
            if not is_cont:
                self.entry = name
            if not self.level == "/":
                self.level += "/"
            self.level += name
        elif direction > 0 and not self.level == "/": # Popping up to parent
            last_slash = self.level.rindex("/")
            self.level = self.level[0:last_slash]
            if len(self.level) == 0:
                self.level = "/"
            if len(self.back_stack) > 0:
                log.debug("Stack not empty; going back to previous selection.")
                self.selection, self.top_row_index = self.back_stack.pop(-1)
                went_back = True

        self.level_container_names = []
        self.level_entry_names = []
        if not self.entry:
            self.level_container = shared_cfg.master_store.get_container_by_path(self.level)
            for k, c in self.level_container.get_nodes():
                self.level_container_names.append(k)
            for k, e in self.level_container.get_credentials():
                self.level_entry_names.append(k)
            self.level_container_names.sort()
            self.level_entry_names.sort()

        if not went_back:
            self.selection = 0
            self.top_row_index = 0

    def get_selection(self):
        """
        :return: Returns a tuple, containing the name of current selection and
        a boolean indicating whether or not the selection is a container.
        """

        if self.entry:
            return self.entry_actions[self.selection][0], False

        cc = len(self.level_container_names)
        ec = len(self.level_entry_names)

        if cc == 0 and ec == 0:
            return "", False

        if self.selection >= cc:
            return self.level_entry_names[self.selection - cc], False
        return self.level_container_names[self.selection], True

    def change_selection(self, direction):
        """
        :type direction: int Positive number moves selection up in hierarchy,
        negative number moves down.
        """
        if self.entry:
            limit = len(self.entry_actions)
        else:
            limit = len(self.level_container_names)
            limit += len(self.level_entry_names)

        if self.selection <= 0 and direction < 0:
            return self.selection
        if self.selection >= limit - 1 and direction > 0:
            return self.selection

        self.selection += direction
        if self.selection < self.top_row_index:
            self.top_row_index -= 1
        if self.selection >= self.top_row_index + self.row_extent.span():
            self.top_row_index += 1

        return self.selection

    def elide_path_string(self, path):
        if len(path) > self.col_extent.span():
            # Show only enough characters that will fit in the span, prefixed
            # by an ellipsis.
            path = "..." + path[-(self.col_extent.span()-3):]
        return path

    def render_level(self, stdscr):
        stdscr.addstr(self.parent_info_row,
                      self.col_extent.min,
                      self.elide_path_string(self.level).center(self.col_extent.span()),
                      curses.A_BOLD)
        if not self.entry:
            self.render_container(stdscr)
        else:
            self.render_entry(stdscr)

    def render_container(self, stdscr):
        cc = len(self.level_container_names)
        ec = len(self.level_entry_names)
        for r in range(self.top_row_index, self.top_row_index + self.row_extent.span()):
            scr_row = self.row_extent.min + r - self.top_row_index
            scr_col = self.col_extent.min
            entry_text = ""
            if r < cc:
                entry_text = ">" + self.level_container_names[r]
            elif r < cc + ec + 1 and r - cc < ec:
                entry_text = self.level_entry_names[r-cc]
            elif self.selection == 0 and cc + ec == 0 and r == self.top_row_index:
                entry_text = "<<<<NO ENTRIES>>>>"

            if self.selection == r and cc + ec > 0:
                stdscr.addstr(scr_row, scr_col,
                              entry_text.ljust(self.col_extent.span()),
                              curses.A_REVERSE)
            else:
                stdscr.addstr(scr_row, scr_col,
                              entry_text.ljust(self.col_extent.span()))

    def render_entry(self, stdscr):
        cc = len(self.entry_actions)
        for r in range(self.top_row_index,
                       self.top_row_index + self.row_extent.span()):
            scr_row = self.row_extent.min + r - self.top_row_index
            scr_col = self.col_extent.min
            entry_text = ""
            text_attr = curses.color_pair(ColorPair.NORMAL)
            if r < cc:
                entry_text = self.entry_actions[r][0]
                text_to_send = self.get_entry_action_text(r)
                if not text_to_send or len(text_to_send) == 0:
                    if self.selection == r:
                        text_attr = curses.color_pair(ColorPair.NO_DATA_SELECTED)
                    else:
                        text_attr = curses.color_pair(ColorPair.NO_DATA)
                    entry_text += " (no data to send!)"
                elif self.selection == r:
                    text_attr = curses.color_pair(ColorPair.SELECTED)

                stdscr.addstr(scr_row, scr_col,
                              entry_text.ljust(self.col_extent.span()),
                              text_attr)
            else:
                stdscr.addstr(scr_row, scr_col,
                              entry_text.ljust(self.col_extent.span()))


def render_instructions(stdscr, row, maxx):
    text_attr = curses.color_pair(ColorPair.TITLE)
    text = ""
    addl_text_attr = curses.color_pair(ColorPair.NORMAL)
    addl_text = []
    if shared_cfg.is_in_keyboard_mode():
        text = "Keyboard Mode"
        if shared_cfg.master_store.is_empty():
            text += " (no data)"
            addl_text.append("Press {0} button to".format(
                HW_BTN_LABEL[ButtonAction.EDIT]))
            addl_text.append("add entries.")
        else:
            addl_text.append("Navigate with wheel and")
            addl_text.append("{0} button".format(
                HW_BTN_LABEL[ButtonAction.BACK]))
    elif shared_cfg.master_store:
        text = "Web Browser Management Mode"
        addl_text.append("Enable Keyboard mode from the")
        addl_text.append("web interface or go directly to")
        addl_text.append("{}/activate".format(shared_cfg.BASE_URL))
    else:
        text = "Device Locked"
        addl_text.append("Go to {}/login".format(shared_cfg.BASE_URL))
        addl_text.append(("to unlock."))
    stdscr.addstr(row, 1, text.center(maxx-2), text_attr)
    row += 1
    for r in range(0, len(addl_text)):
        stdscr.addstr(row, 1, addl_text[r].ljust(maxx-2), addl_text_attr)
        row += 1

    return row


def cryptex(stdscr):
    curses.start_color()
    curses.init_pair(ColorPair.NORMAL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.SELECTED, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(ColorPair.NO_DATA, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(ColorPair.NO_DATA_SELECTED, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(ColorPair.TITLE, curses.COLOR_BLACK, curses.COLOR_GREEN)
    hardware.set_device_mode(shared_cfg.RNDIS_USB_MODE)
    enc_value = hardware.get_enc_value()
    in_keyboard_mode = False
    navigator = None
    last_direction = 0

    curses.curs_set(0)  # Turn off cursor
    maxy, maxx = stdscr.getmaxyx()

    if maxx not in BTN_LABEL_X_POS.keys():
        raise Exception("Screen resolution of {0} x {1} characters "
                        "not supported. Sad.".format(maxx, maxy))

    try:
        while 1:
            stdscr.border()

            if shared_cfg.master_store:
                stdscr.addstr(maxy - 1, BTN_LABEL_X_POS[maxx][ButtonAction.LOCK-1],
                              HW_BTN_LABEL[ButtonAction.LOCK])

            if shared_cfg.is_in_keyboard_mode():
                stdscr.addstr(maxy - 1, BTN_LABEL_X_POS[maxx][ButtonAction.EDIT-1],
                              HW_BTN_LABEL[ButtonAction.EDIT])
                stdscr.addstr(maxy - 1, BTN_LABEL_X_POS[maxx][ButtonAction.BUTTON_3-1],
                              HW_BTN_LABEL[ButtonAction.BUTTON_3])
                stdscr.addstr(maxy - 1, BTN_LABEL_X_POS[maxx][ButtonAction.BACK-1],
                              HW_BTN_LABEL[ButtonAction.BACK])

            row = 1
            row = render_instructions(stdscr, row, maxx)

            new_enc_value, eb_pressed, hw_button = hardware.check_gpio(enc_value)

            if shared_cfg.master_store and hw_button == ButtonAction.LOCK:
                log.debug("Locking it down.")
                shared_cfg.lock_store()
                in_keyboard_mode = False
                navigator = None
                hardware.set_device_mode(shared_cfg.RNDIS_USB_MODE)
            elif shared_cfg.is_in_keyboard_mode():
                if hw_button == ButtonAction.EDIT:
                    log.debug("Going to web mode.")
                    shared_cfg.activate_web_mode()
                    in_keyboard_mode = False
                    navigator = None
                else:
                    direction = last_direction
                    if hw_button == 0:
                        if new_enc_value != enc_value:
                            if new_enc_value == CW_ORDER[enc_value]:
                                direction -= 1.0 / TICKS_PER_STEP
                            elif new_enc_value == CCW_ORDER[enc_value]:
                                direction += 1.0 / TICKS_PER_STEP
                            last_direction = direction
                            if abs(last_direction) >= 1.0:
                                last_direction = 0
                            enc_value = new_enc_value
                    elif hw_button == ButtonAction.BACK:
                        direction = -1
                        last_direction = 0

                    if not in_keyboard_mode:
                        in_keyboard_mode = True
                        navigator = StoreNavigator(1, row, maxx-2, maxy-3)
                        hardware.set_device_mode(shared_cfg.HID_USB_MODE)
                    navigator.change_selection(round(direction))
                    navigator.render_level(stdscr)
                    if eb_pressed:
                        navigator.change_level(-1)
                    elif hw_button == 1:
                        navigator.change_level(1)
            else: # Render all remaining rows empty
                while row < maxy - 2:
                    stdscr.addstr(row, 1, " ".ljust(maxx-2))
                    row += 1

            stdscr.refresh()
    except KeyboardInterrupt:
        hardware.GPIO.cleanup()

