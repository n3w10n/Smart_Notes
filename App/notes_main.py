from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QHBoxLayout, QMessageBox, QGroupBox, QTextEdit, QListWidget, QLineEdit, QInputDialog

app = QApplication([])

main_win = QTextEdit()
main_win.show()
main_win.resize(1000, 800)
main_win.setWindowTitle("Smart Notes")

layout_left = QVBoxLayout()
edit_text = QTextEdit()
layout_left.addWidget(edit_text)
layout_right = QVBoxLayout()

layout_topright = QVBoxLayout()
layout_right.addLayout(layout_topright)
label_note = QLabel("List of notes")
list_topright = QListWidget()
layout_topright.addWidget(label_note)
layout_topright.addWidget(list_topright)
button_layout = QHBoxLayout()
button_left = QPushButton("Create note")
button_right = QPushButton("Delete note")
button_layout.addWidget(button_left)
button_layout.addWidget(button_right)
layout_topright.addLayout(button_layout)
save_button = QPushButton("Save note")
layout_topright.addWidget(save_button)

layout_bottomright = QVBoxLayout()
layout_right.addLayout(layout_bottomright)
label_tag = QLabel("List of tags")
list_bottomright = QListWidget()
layout_bottomright.addWidget(label_tag)
layout_bottomright.addWidget(list_bottomright)
search_tag = QLineEdit()
search_tag.setPlaceholderText("Enter tag...")
layout_bottomright.addWidget(search_tag)
button_horizontal = QHBoxLayout()
button_l = QPushButton("Add to note")
button_r = QPushButton("Untag from note")
button_horizontal.addWidget(button_l)
button_horizontal.addWidget(button_r)
layout_bottomright.addLayout(button_horizontal)
search_button = QPushButton("Search notes by tag")
layout_bottomright.addWidget(search_button)

layout_main = QHBoxLayout()
layout_main.addLayout(layout_left, stretch=3)
layout_main.addLayout(layout_right)

import json
# file = open("results.json", "w")
# json.dump(data, file)

file = open("notes_data.json", "r")
data = json.load(file)
note_name_list = data.keys()
list_topright.addItems(note_name_list)

def showNote():
    select_note = list_topright.selectedItems()[0].text()
    
    tags = data[select_note]["tags"]

    text = data[select_note]["text"]
    edit_text.setText(text)
    
    list_bottomright.clear()
    list_bottomright.addItems(tags)

list_topright.itemClicked.connect(showNote)

def addTag():
    select_note = list_topright.selectedItems()[0].text()
    tags = data[select_note]["tags"]
    
    new_tag = search_tag.text()
    
    if new_tag in tags:
        print("already added")
    else:
        tags.append(new_tag)
        list_bottomright.clear()
        list_bottomright.addItems(tags)

button_l.clicked.connect(addTag)

def removeTag():
    select_note = list_topright.selectedItems()[0].text()
    select_tag = list_bottomright.selectedItems()[0].text()
    tags = data[select_note]["tags"]
    tags.remove(select_tag)

    list_bottomright.clear()
    list_bottomright.addItems(tags)

button_r.clicked.connect(removeTag)

def searchTag():
    tag = search_tag.text()
    results = ""
    count = 0
    for note in data:
        tags = data[note]["tags"]
        if tag in tags:
            results += note + "\n"
            count += 1
    
    if count == 0:
        results = "There are no notes with that tag"
    edit_text.setText(results)

def removeNote():
    select_note = list_topright.selectedItems()[0].text()
    del data[select_note]
    note_name_list = data.keys()
    list_topright.clear()
    list_topright.addItems(note_name_list)

button_right.clicked.connect(removeNote)

def createNote():
    note_name, result = QInputDialog.getText(main_win, "Create Note", "Note name:")
    print(note_name, result)

    if len(note_name) != 0:
        if result == True:
            data[note_name] = {"tags": [], "text": ""}

            note_name_list = data.keys()
            list_topright.clear()
            list_topright.addItems(note_name_list)

def saveNote():
    notes_data = open("results.json", "w")
    json.dump(data, notes_data)

save_button.clicked.connect(saveNote)

button_left.clicked.connect(createNote)

search_button.clicked.connect(searchTag)

main_win.setLayout(layout_main)
app.exec_()