import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QListWidget, 
                             QProgressBar, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PIL import Image

class ImageProcessorWorker(QThread):
    """
    Worker thread to handle image processing without freezing the GUI.
    """
    progress_update = pyqtSignal(int)
    log_update = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.is_running = True

    def run(self):
        total_files = len(self.file_paths)
        if total_files == 0:
            self.finished.emit()
            return

        for i, file_path in enumerate(self.file_paths):
            if not self.is_running:
                break
            
            try:
                self.process_image(file_path)
            except Exception as e:
                self.log_update.emit(f"Error processing {os.path.basename(file_path)}: {str(e)}")
            
            # Update progress
            progress_percent = int(((i + 1) / total_files) * 100)
            self.progress_update.emit(progress_percent)

        self.finished.emit()

    def process_image(self, file_path):
        directory, filename = os.path.split(file_path)
        name, ext = os.path.splitext(filename)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(directory, "processed_output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with Image.open(file_path) as img:
            img = img.convert("RGBA") # Ensure consistency
            width, height = img.size
            
            mid_point = height // 2
            
            # Logic: Remove 1 line if even height, 3 lines if odd height
            if height % 2 == 0:
                lines_to_remove = 1
                # Remove the exact middle line (index mid_point)
                # Crop Top: 0 to mid_point
                # Crop Bottom: mid_point + 1 to end
                top_box = (0, 0, width, mid_point)
                bottom_box = (0, mid_point + 1, width, height)
            else:
                lines_to_remove = 3
                # Remove middle line and one above, one below
                # If height is too small (e.g. 1px), handle gracefully
                if height < 3:
                    self.log_update.emit(f"Skipped {filename}: Image too small to cut 3 lines.")
                    return

                # Center is mid_point. Remove (mid_point-1), (mid_point), (mid_point+1)
                top_box = (0, 0, width, mid_point - 1)
                bottom_box = (0, mid_point + 2, width, height)

            # Perform Crops
            top_part = img.crop(top_box)
            bottom_part = img.crop(bottom_box)

            # Create new image
            new_height = top_part.height + bottom_part.height
            new_img = Image.new("RGBA", (width, new_height))

            # Paste parts
            new_img.paste(top_part, (0, 0), top_part)
            new_img.paste(bottom_part, (0, top_part.height), bottom_part)

            # Save
            save_path = os.path.join(output_dir, f"{name}{ext}")
            new_img.save(save_path)
            self.log_update.emit(f"Processed: {filename} (Removed {lines_to_remove} lines)")

    def stop(self):
        self.is_running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Center Line Remover")
        self.resize(600, 500)
        self.file_paths = []

        # --- UI Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instructions
        instruction_label = QLabel("Select images to remove the center pixel line.\n(Removes 1 line for even heights, 3 lines for odd heights)")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)

        # List of files
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Select Images")
        self.btn_add.clicked.connect(self.select_images)
        self.btn_clear = QPushButton("Clear List")
        self.btn_clear.clicked.connect(self.clear_list)
        
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_clear)
        layout.addLayout(btn_layout)

        # Process Button
        self.btn_process = QPushButton("Start Processing")
        self.btn_process.clicked.connect(self.start_processing)
        self.btn_process.setStyleSheet("font-weight: bold; padding: 10px; background-color: #4CAF50; color: white;")
        layout.addWidget(self.btn_process)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status Label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def select_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp *.tiff)")
        if files:
            for f in files:
                if f not in self.file_paths:
                    self.file_paths.append(f)
                    self.file_list.addItem(os.path.basename(f))
            self.status_label.setText(f"{len(self.file_paths)} images selected.")

    def clear_list(self):
        self.file_paths = []
        self.file_list.clear()
        self.status_label.setText("List cleared.")
        self.progress_bar.setValue(0)

    def start_processing(self):
        if not self.file_paths:
            QMessageBox.warning(self, "No Images", "Please select images first.")
            return

        self.btn_process.setEnabled(False)
        self.btn_add.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Processing...")

        # Initialize and start worker thread
        self.worker = ImageProcessorWorker(self.file_paths)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.log_update.connect(self.update_status)
        self.worker.finished.connect(self.processing_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_label.setText(message)

    def processing_finished(self):
        self.btn_process.setEnabled(True)
        self.btn_add.setEnabled(True)
        self.btn_clear.setEnabled(True)
        self.status_label.setText("Processing Complete! Check 'processed_output' folder.")
        QMessageBox.information(self, "Done", "All images have been processed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
