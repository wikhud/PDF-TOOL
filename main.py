import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFrame, QLabel, QFileDialog, QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import fitz  # PyMuPDF
import os
import io
from PyQt5.QtGui import QFont

import fitz  # PyMuPDF
import os
import os
import fitz  # PyMuPDF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ButtonFrameExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_index = 00
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Button Frame Example")
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.main_menu()

    def main_menu(self):
        self.clear_layout(self.main_layout)

        main_menu_frame = QFrame()
        main_menu_layout = QVBoxLayout(main_menu_frame)

        concat_button = QPushButton("Concatenate files")
        concat_button.clicked.connect(self.concat)
        split_button = QPushButton("Split file")
        split_button.clicked.connect(self.split)

        main_menu_layout.addWidget(concat_button)
        main_menu_layout.addWidget(split_button)

        self.main_layout.addWidget(main_menu_frame)

    def split(self):
        self.clear_layout(self.main_layout)

        # Vars for spliting
        self.pdf_to_split = ''
        self.imgs_split = [] # List to store merged PDFs as images (to display)

        # Frame and layout
        split_frame = QFrame()
        split_layout = QVBoxLayout(split_frame)

        # Label widgets
        stable_info_label_1 = QLabel("SPLITING")
        stable_info_label_1.setAlignment(QtCore.Qt.AlignCenter)
        stable_info_label_1.setFont(QFont("Arial", 20, QFont.Bold))
        stable_info_label_3 = QLabel("Page Ranges (e.g., 1-3, 5, 4-6):")
        stable_info_label_2 = QLabel("Selected file:")
        self.selected_file_label = QLabel()  # Create pdf_list QLabel instance attribute
        self.split_info_label_1 = QLabel("")
        self.split_info_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.split_info_label_1.setFont(QFont("Arial", 15))
        self.split_info_label_1.setStyleSheet("color: red;")
        self.split_image_label = QLabel()
        self.split_image_label.setAlignment(QtCore.Qt.AlignCenter) # Diplay selected file
        # self.concat_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.split_image_label.setFixedSize(600, 600)
        self.split_page_n_label = QLabel()

        # Entry widgets
        self.ranges_entry = QLineEdit()
        # Create a regular expression pattern that allows numbers, comma, and hyphen and disallow hyphen or comma as the first character
        pattern = "^(?![-,])(?!.*(--|,,|,-|-,|,,))[-,\d]*$"
        validator = QRegExpValidator(QRegExp(pattern))
        # Set the validator for the ranges_entry QLineEdit
        self.ranges_entry.setValidator(validator)
        self.ranges_entry.textEdited.connect(lambda: self.split_info_label_1.setText(''))

        # Button widgets
        select_file_button = QPushButton("Add file")
        select_file_button.clicked.connect(lambda: self.select_pdf('split'))
        split_button = QPushButton("Split file")
        split_button.clicked.connect(self.split_pdf)  # Connect the button to the concatenation function
        clear_all_button = QPushButton("Clear all")
        clear_all_button.clicked.connect(lambda: self.start_over_split('all'))
        back_to_main = QPushButton("Back to Main Menu")
        back_to_main.clicked.connect(self.main_menu)    
        self.split_next_button = QPushButton('Next') # Next page of displayed file button
        self.split_next_button.clicked.connect(lambda: self.next_image('split'))
        self.split_prev_button = QPushButton('Previous')
        self.split_prev_button.clicked.connect(lambda: self.prev_image('split'))

        # Placing widgets in concat frame
        split_layout.addWidget(stable_info_label_1)
        split_layout.addWidget(select_file_button)
        split_layout.addWidget(stable_info_label_2)
        split_layout.addWidget(self.selected_file_label)
        split_layout.addWidget(stable_info_label_3)
        split_layout.addWidget(self.ranges_entry)
        split_layout.addWidget(split_button)
        split_layout.addWidget(self.split_info_label_1)  
        split_layout.addWidget(self.split_image_label)
        split_layout.addWidget(self.split_page_n_label)
        split_layout.addWidget(self.split_next_button) 
        split_layout.addWidget(self.split_prev_button)       
        split_layout.addWidget(clear_all_button)
        split_layout.addWidget(back_to_main)

        self.main_layout.addWidget(split_frame)

        self.update_buttons_state('split')

    def concat(self):
        self.clear_layout(self.main_layout)

        # Vars for concating
        self.pdfs_to_concat = []  # List to store selected PDFs
        self.imgs_concat = [] # List to store merged PDFs as images (to display)
        

        # Frame and layout
        frame_concat = QFrame()
        layout_concat = QVBoxLayout(frame_concat)

        # Label widgets
        stable_info_label_1 = QLabel("CONCATENATION")
        stable_info_label_1.setAlignment(QtCore.Qt.AlignCenter)
        stable_info_label_1.setFont(QFont("Arial", 20, QFont.Bold))
        stable_info_label_2 = QLabel("Selected files:")
        self.selected_files_list_label = QLabel()  # Create pdf_list QLabel instance attribute
        self.concat_info_label_1 = QLabel("") # Concatenateing completed info
        self.concat_info_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.concat_info_label_1.setFont(QFont("Arial", 15))
        self.concat_info_label_1.setStyleSheet("color: red;")
        self.concat_image_label = QLabel() # Display selected file
        self.concat_image_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.concat_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.concat_image_label.setFixedSize(600, 600)
        self.concat_page_n_label = QLabel()

        # Button widgets
        select_file_button = QPushButton("Add file")
        select_file_button.clicked.connect(lambda: self.select_pdf('concat'))
        concatenate_button = QPushButton("Concatenate files")
        concatenate_button.clicked.connect(self.concatenate_pdfs)
        clear_all_button = QPushButton("Clear all")
        clear_all_button.clicked.connect(self.start_over_concat)       
        back_to_main = QPushButton("Back to Main Menu")
        back_to_main.clicked.connect(self.main_menu)
        self.concat_next_button = QPushButton('Next') # Next page of displayed file button
        self.concat_next_button.clicked.connect(lambda: self.next_image('concat'))
        self.concat_prev_button = QPushButton('Previous')
        self.concat_prev_button.clicked.connect(lambda: self.prev_image('concat'))

        # Placing widgets in concat frame
        layout_concat.addWidget(stable_info_label_1)
        layout_concat.addWidget(select_file_button)
        layout_concat.addWidget(stable_info_label_2)
        layout_concat.addWidget(self.selected_files_list_label)
        layout_concat.addWidget(concatenate_button)
        layout_concat.addWidget(self.concat_info_label_1)
        layout_concat.addWidget(self.concat_image_label)
        layout_concat.addWidget(self.concat_page_n_label)
        layout_concat.addWidget(self.concat_next_button) 
        layout_concat.addWidget(self.concat_prev_button)
        layout_concat.addWidget(clear_all_button)
        layout_concat.addWidget(back_to_main)

        
        self.main_layout.addWidget(frame_concat)

        self.update_buttons_state('concat')

    def update_image(self, action):

        self.update_buttons_state(action)

        if action == 'concat':
        
            if not self.imgs_concat:
                return
            
            pixmap = self.imgs_concat[self.current_index]
            # Resize the pixmap to fit the label while preserving aspect ratio
            scaled_pixmap = pixmap.scaled(self.concat_image_label.size(), QtCore.Qt.KeepAspectRatio)
            self.concat_image_label.setPixmap(scaled_pixmap)

            self.concat_page_n_label.setText(f'{self.current_index + 1}/{len(self.imgs_concat)}')
        
        if action == 'split':    
            
            if not self.imgs_split:
                return
            
            pixmap = self.imgs_split[self.current_index]
            # Resize the pixmap to fit the label while preserving aspect ratio
            scaled_pixmap = pixmap.scaled(self.split_image_label.size(), QtCore.Qt.KeepAspectRatio)
            self.split_image_label.setPixmap(scaled_pixmap)

            self.split_page_n_label.setText(f'{self.current_index + 1}/{len(self.imgs_split)}')
        

    def update_buttons_state(self, action):
        if action == 'concat':
            self.concat_prev_button.setEnabled(self.current_index > 0)
            self.concat_next_button.setEnabled(self.current_index < len(self.imgs_concat) - 1)
        if action == 'split':
            self.split_prev_button.setEnabled(self.current_index > 0)
            self.split_next_button.setEnabled(self.current_index < len(self.imgs_split) - 1)
        

    def next_image(self, action):
        if action == 'concat':
            self.current_index = (self.current_index + 1) % len(self.imgs_concat)

        if action == 'split':
            self.current_index = (self.current_index + 1) % len(self.imgs_split)

        self.update_image(action)

    def prev_image(self, action):
        if action == 'concat':
            self.current_index = (self.current_index - 1) % len(self.imgs_concat)

        if action == 'split':
            self.current_index = (self.current_index - 1) % len(self.imgs_split)
        
        self.update_image(action)




    def select_pdf(self, action):
        if action == 'split':
            if self.split_info_label_1.text() == 'Spliting completed!':
                self.start_over_split()
            if self.split_info_label_1.text() == 'Select file to split!' or self.split_info_label_1.text() == 'Set pages split range!' or self.split_info_label_1.text() == 'Invalid range!' :
                self.split_info_label_1.setText('')

            new_file, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")

            if new_file:
                self.pdf_to_split = new_file
                self.selected_file_label.setText(self.pdf_to_split)
                # Check if there is PDF already displayed, if so and new one is selected - clear it.
                if self.imgs_split != []:
                    self.imgs_split == []
                self.marging_and_displaying_split()

        if action == 'concat':    
            if self.concat_info_label_1.text() == 'Concatenation completed!':
                self.start_over_concat()

            if self.concat_info_label_1.text() == 'Select at least 2 files to concatenate!':
                self.concat_info_label_1.setText('')   

            selected_pdfs, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")

            if selected_pdfs:
                self.pdfs_to_concat.extend(selected_pdfs)  # Use extend() instead of append()
                self.update_concat_pdf_list_label()
                self.marging_and_displaying()
                

    def split_pdf(self):
        if self.split_info_label_1.text() == 'Spliting completed!':
            return
        if not self.pdf_to_split:
            print('Select file to split!')
            self.split_info_label_1.setText('Select file to split!')
            return
        elif self.ranges_entry.text() == '':
            print('Set pages split range!')
            self.split_info_label_1.setText('Set pages split range!')
            return
        
        self.split_range_clean()
        page_ranges = self.ranges_entry.text()
        pdf_reader = PdfReader(self.pdf_to_split)

        # Calculate the total number of pages in the PDF
        total_pages = len(pdf_reader.pages)
        # Split the page_ranges string into individual ranges
        ranges = page_ranges.split(',')

        # Validate all ranges
        for i, page_range in enumerate(ranges):
            if '-' in page_range:
                start, end = map(int, page_range.split("-"))
            else:
                start = end = int(page_range)
            # Handle cases while out of range
            if start < 1 or end > total_pages or start > end:
                print('Invalid range!')
                self.split_info_label_1.setText('Invalid range!')
                return

        # Split ranges
        for i, page_range in enumerate(ranges):
            splited_file_name = os.path.basename(self.pdf_to_split)
            # file_name = os.path.basename(file_path)
            splited_file_name = os.path.splitext(splited_file_name)[0]
            # Handle cases where the range might be empty or only have one value
            if '-' in page_range:
                start, end = map(int, page_range.split("-"))
                output_file_name = f"{splited_file_name}_pages_{page_range}"
            else:
                start = end = int(page_range)
                output_file_name = f"{splited_file_name}_page_{page_range}"

            # print(page_range)
            # output_file_name = f"splited_file_page_{page_range}"
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Splited PDF", output_file_name, "PDF Files (*.pdf)")
            
            if file_path:
                pdf_writer = PdfWriter()
                for page in range(start - 1, end):
                    pdf_writer.add_page(pdf_reader.pages[page])

                with open(file_path, 'wb') as output:
                    pdf_writer.write(output)
                    
                print('ok')
                self.split_info_label_1.setText('Spliting completed!')

        

    def concatenate_pdfs(self):
        if self.concat_info_label_1.text() == 'Concatenation completed!':
            return

        if not self.pdfs_to_concat or len(self.pdfs_to_concat) == 1:
            print('Select at least 2 files to concatenate!')
            self.concat_info_label_1.setText('Select at least 2 files to concatenate!')
            return  # Nothing to concatenate

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Concatenated PDF", "concatenated_file", "PDF Files (*.pdf)")

        if file_path:
            merger = PdfMerger()
            for pdf_file in self.pdfs_to_concat:
                merger.append(pdf_file)

            with open(file_path, "wb") as output_file:
                merger.write(output_file)
            print('ok')

            self.concat_info_label_1.setText('Concatenation completed!')
 

    def marging_and_displaying(self):
        merger = PdfMerger()
        for pdf_file in self.pdfs_to_concat:
            merger.append(pdf_file)

        # Create a BytesIO object to hold the PDF data
        pdf_buffer = io.BytesIO()
        
        # Write the concatenated PDF data to the buffer
        merger.write(pdf_buffer)
        pdf_buffer.seek(0)  # Reset the buffer position to the beginning

        # Call pdf_to_image on the concatenated PDF
        self.imgs_concat = self.pdf_to_image(pdf_buffer)  # Pass the temporary file path

        self.update_image('concat')


    def marging_and_displaying_split(self):
        pdf_buffer = open(self.pdf_to_split, "rb").read()
        self.imgs_split = self.pdf_to_image(pdf_buffer)
        self.update_image('split')


    def pdf_to_image(self, pdf_data):
        pdf_document = fitz.open(stream=pdf_data)
        images = []

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            image = page.get_pixmap()
            # Convert the PyMuPDF Pixmap to a QImage and then to a QPixmap
            image_qimg = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image_qimg)   

            images.append(pixmap)

        pdf_document.close()

        return images



    def split_range_clean(self):
        last_char = self.ranges_entry.text()[-1]
        if last_char == ',' or last_char == '-':
            new_text = self.ranges_entry.text()[:-1]  # Remove last character
            self.ranges_entry.setText(new_text)
            
    def start_over_split(self, clearing_type = ''):
        self.split_info_label_1.setText('')
        self.pdf_to_split = ''
        self.selected_file_label.setText(self.pdf_to_split)
        if clearing_type == "all":
            self.ranges_entry.clear()


        self.split_page_n_label.setText('')
        self.split_image_label.setPixmap(QPixmap()) 
        self.current_index = 0

        self.imgs_split.clear()

        self.update_image('split')
    
    def update_concat_pdf_list_label(self):
        pdf_list_text =[]

        if self.pdfs_to_concat:
            for i in range(len(self.pdfs_to_concat)):
                pdf_list_text.append(f"({i+1}) {self.pdfs_to_concat[i]}")
            pdf_text = "\n".join(pdf_list_text)
            self.selected_files_list_label.setText(pdf_text)

        else:
            pdf_list_text = "\n".join(self.pdfs_to_concat)
            self.selected_files_list_label.setText(pdf_list_text)

    def start_over_concat(self):
        self.concat_info_label_1.setText('')
        self.concat_page_n_label.setText('')
        self.concat_image_label.setPixmap(QPixmap()) 
        self.current_index = 0
        self.pdfs_to_concat.clear()
        self.imgs_concat.clear()
        self.update_concat_pdf_list_label()
        self.update_image('concat')


    def clear_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ButtonFrameExample()
    window.show()
    sys.exit(app.exec_())
