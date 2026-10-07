import os
import sys
import csv
import html
import random
import secrets
import string
from datetime import datetime

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (QColor, QFont, QPainter, QPainterPath, QPen,
                           QLinearGradient, QRadialGradient)
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

# Decoration settings
WIN_W, WIN_H = 800, 600
RADIUS = 28
BG_COLOR = QColor("#EDB88B")
TEXT_COLOR = "#3a2a1c"
HINT_COLOR = "rgba(58,42,28,170)"
FONT_FAMILY = "Century Gothic"
FONT_STACK = "'Century Gothic','Questrial','Avenir','Arial',sans-serif"

desktop = os.path.join(os.path.expanduser("~"), "Desktop")

def batch_filepath():
    now = datetime.now()
    for n in range(1, 100):
        path = os.path.join(desktop, "batch{:02d}{:02d}{:02d}.csv".format(n, now.month, now.day))
        if not os.path.exists(path):
            return path
    return os.path.join(desktop, "batch99{:02d}{:02d}.csv".format(now.month, now.day))

def current_batch_filepath():
    now = datetime.now()
    existing = []
    for n in range(1, 100):
        path = os.path.join(desktop, "batch{:02d}{:02d}{:02d}.csv".format(n, now.month, now.day))
        if os.path.exists(path):
            existing.append(path)
    return existing[-1] if existing else batch_filepath()

def generate_code(name, last_name):
    return (name[:2].lower() + last_name[:2].lower()
            + str(datetime.now().month).zfill(2) + str(random.randint(0, 999)))

def generate_password(length=6):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))


#  User Interface.
class Jandsheic(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(WIN_W, WIN_H)
        self.setFocusPolicy(Qt.StrongFocus)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 0, 40, 0)
        layout.setSpacing(0)

        # This is what sets the "Jandsheic" logo on the superior third of the image.
        self.logo = QLabel()
        self.logo.setFixedHeight(110)
        self.logo.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.logo.setTextFormat(Qt.RichText)
        self.logo.setText(
            "<span style=\"font-family:%s; font-size:24px; font-weight:bold;\">"
            "<span style='color:#80c242;'>J</span>"
            "<span style='color:#7bbfe9;'>andsheic</span></span>" % FONT_STACK)

        # Instructions block,  set below the logo.
        self.hint = QLabel()
        self.hint.setFixedHeight(WIN_H // 3 - 110)
        self.hint.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.hint.setTextFormat(Qt.PlainText)
        self.hint.setWordWrap(True)
        hf = QFont(FONT_FAMILY)
        hf.setBold(True)
        hf.setPixelSize(18)
        self.hint.setFont(hf)
        self.hint.setStyleSheet("color: %s; background: transparent; padding-top: 10px;" % HINT_COLOR)


        self.body = QLabel()
        self.body.setFixedHeight(WIN_H - WIN_H // 3)
        self.body.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.body.setTextFormat(Qt.RichText)
        self.body.setWordWrap(True)
        f = QFont(FONT_FAMILY)
        f.setBold(True)
        f.setPixelSize(18)
        self.body.setFont(f)
        self.body.setStyleSheet("color: %s; background: transparent;" % TEXT_COLOR)

        for w in (self.logo, self.hint, self.body):
            w.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._drag = None

        layout.addWidget(self.logo)
        layout.addWidget(self.hint)
        layout.addWidget(self.body)

        self.go_menu()

    # Glassmorphism deco
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, RADIUS, RADIUS)
        p.setClipPath(path)

        # Background and some graph. effects.
        p.fillPath(path, BG_COLOR)

        for cx, cy, r in ((150, 120, 260), (680, 160, 240), (480, 520, 280)):
            rg = QRadialGradient(QPointF(cx, cy), r)
            rg.setColorAt(0, QColor(255, 255, 255, 55))
            rg.setColorAt(1, QColor(255, 255, 255, 0))
            p.fillRect(self.rect(), rg)

        shine = QLinearGradient(0, 0, 0, WIN_H)
        shine.setColorAt(0, QColor(255, 255, 255, 70))
        shine.setColorAt(0.5, QColor(255, 255, 255, 0))
        p.fillPath(path, shine)
        p.setClipping(False)
        p.setPen(QPen(QColor(255, 255, 255, 170), 1.5))
        p.drawPath(path)


    def show_html(self, rows=(), lines=(), hint="", message=""):

        out = ["<div style=\"font-family:%s; font-size:18px; font-weight:bold;\">" % FONT_STACK]
        if rows:
            out.append("<table align='center' cellspacing='6'>")
            for label, value, active in rows:
                cur = "&#9611;" if active else ""
                out.append("<tr><td align='left'>%s</td><td align='left'>&nbsp;%s%s</td></tr>"
                           % (html.escape(label), html.escape(value), cur))
            out.append("</table>")
        for ln in lines:
            out.append("<p align='center' style='margin:4px;'>%s</p>" % html.escape(ln))
        if message:
            out.append("<p align='center' style='margin:10px;'>%s</p>" % html.escape(message))
        out.append("</div>")
        self.hint.setText(hint)
        self.body.setText("".join(out))

    # Main menu
    def go_menu(self, message=""):
        self.mode = "menu"
        self.message = message
        out = ["<div style=\"font-family:%s; font-size:18px; font-weight:bold;\">" % FONT_STACK,
               "<table align='center' cellspacing='8'>",
               "<tr><td align='left'>1-</td><td align='left'>Admin mode</td></tr>",
               "<tr><td align='left'>2-</td><td align='left'>Terminal mode</td></tr>",
               "<tr><td align='left'>3-</td><td align='left'>Exit</td></tr>",
               "</table>"]
        if message:
            out.append("<p align='center'>%s</p>" % html.escape(message))
        out.append("</div>")
        self.hint.setText("Press the number to access the desired mode or press ESC to exit")
        self.body.setText("".join(out))

    # Terminal mode
    def go_terminal(self):
        self.mode = "terminal"
        self.stage = "first"
        self.first = self.last = ""
        self.buffer = ""
        self.message = ""
        self.refresh_terminal()

    def refresh_terminal(self):
        rows = [("Type the first name:", self.first if self.stage != "first" else self.buffer, self.stage == "first"),
                ("Type the last name:", self.last if self.stage != "last" else (self.buffer if self.stage == "last" else ""),
                 self.stage == "last")]
        self.show_html(rows=rows, message=self.message,
                       hint="Type your first and last name to get a user ID and a Password. ESC: menu")

    # Admin mode
    def go_admin(self):
        self.mode = "admin"
        self.stage = "count"
        self.buffer = ""
        self.count = 0
        self.members = []
        self.first = self.last = ""
        self.message = ""
        self.saved = False
        self.refresh_admin()

    def refresh_admin(self):
        if self.stage == "count":
            rows = [("Enter no. of new members:", self.buffer, True)]
        else:
            rows = [("Enter no. of new members:", str(self.count), False),
                    ("Type the first name:", self.buffer if self.stage == "first" else self.first,
                     self.stage == "first"),
                    ("Type the last name:", self.buffer if self.stage == "last" else "",
                     self.stage == "last")] if self.stage in ("first", "last") else \
                   [("Enter no. of new members:", str(self.count), False)]
        lines = [", ".join(m) for m in self.members[-4:]]
        if self.stage == "review":
            hint = "Press F5: save to .csv  or  ESC to return to main menu"
        elif self.stage == "saved":
            hint = "ESC: menu"
        else:
            hint = "ESC: menu at any time. When finished, press F5 to save the .csv"
        self.show_html(rows=rows, lines=lines, message=self.message, hint=hint)

    # What allows the window to be dragged by mouse
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            handle = self.windowHandle()
            if handle is not None and handle.startSystemMove():
                return
            self._drag = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag is not None and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag)

    def mouseReleaseEvent(self, e):
        self._drag = None

    def keyPressEvent(self, e):
        key, text = e.key(), e.text()

        if self.mode == "menu":
            if text == "1":
                self.go_admin()
            elif text == "2":
                self.go_terminal()
            elif text == "3" or key == Qt.Key_Escape:
                self.close()
            else:
                self.go_menu("Get serious!")
            return

        if key == Qt.Key_Escape:
            self.go_menu()
            return

        if self.mode == "admin" and self.stage in ("review",) and key == Qt.Key_F5:
            path = batch_filepath()
            with open(path, "a", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["first name", "last name", "user id", "password"])
                w.writerows(self.members)
            self.stage = "saved"
            self.message = "Saved to " + path
            self.refresh_admin()
            return

        if key in (Qt.Key_Backspace,):
            self.buffer = self.buffer[:-1]
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self.submit()
            return
        elif text and text.isprintable():
            self.buffer += text
        else:
            return
        self.refresh_terminal() if self.mode == "terminal" else self.refresh_admin()

    def submit(self):
        if self.mode == "terminal":
            if self.stage == "first":
                self.first, self.buffer, self.stage = self.buffer, "", "last"
            else:
                last = self.buffer
                code = generate_code(self.first, last)
                pw = generate_password()
                path = current_batch_filepath()
                new_file = not os.path.exists(path) or os.path.getsize(path) == 0
                with open(path, "a", newline="") as fh:
                    w = csv.writer(fh)
                    if new_file:
                        w.writerow(["first name", "last name", "user id", "password"])
                    w.writerow([self.first, last, code, pw])
                self.message = "Hi, %s, your UId is %s and the pass is: %s" % (self.first, code, pw)
                self.first = self.last = self.buffer = ""
                self.stage = "first"
            self.refresh_terminal()
            return

        if self.stage == "count":
            try:
                n = int(self.buffer)
                if n < 1:
                    raise ValueError
            except ValueError:
                self.message = "Enter a valid number."
                self.buffer = ""
                self.refresh_admin()
                return
            self.count, self.buffer, self.message, self.stage = n, "", "", "first"
        elif self.stage == "first":
            self.first, self.buffer, self.stage = self.buffer, "", "last"
        elif self.stage == "last":
            last = self.buffer
            self.members.append([self.first, last, generate_code(self.first, last), generate_password()])
            self.first, self.buffer = "", ""
            self.stage = "review" if len(self.members) >= self.count else "first"
        self.refresh_admin()


def main():
    app = QApplication(sys.argv)
    w = Jandsheic()
    geo = app.primaryScreen().availableGeometry()
    w.move(geo.center().x() - WIN_W // 2, geo.center().y() - WIN_H // 2)
    w.show()
    w.setFocus()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()