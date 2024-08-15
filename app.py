import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Video Editor")
        self.setGeometry(100, 100, 1200, 600)

        self.video_clip = None
        self.video_clips = []
        self.final_clip = None

        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Video Control Layout
        control_layout = QHBoxLayout()

        self.load_button = QPushButton("Load Video", self)
        self.load_button.clicked.connect(self.load_video)
        control_layout.addWidget(self.load_button)

        self.cut_button = QPushButton("Cut Video", self)
        self.cut_button.clicked.connect(self.cut_video)
        control_layout.addWidget(self.cut_button)

        self.concat_button = QPushButton("Concatenate Videos", self)
        self.concat_button.clicked.connect(self.concatenate_videos)
        control_layout.addWidget(self.concat_button)

        self.export_button = QPushButton("Export Video", self)
        self.export_button.clicked.connect(self.export_video)
        control_layout.addWidget(self.export_button)

        main_layout.addLayout(control_layout)

        # Timeline Slider
        self.timeline_slider = QSlider(Qt.Horizontal)
        self.timeline_slider.setRange(0, 100)
        self.timeline_slider.setValue(0)
        self.timeline_slider.sliderMoved.connect(self.slider_moved)
        main_layout.addWidget(self.timeline_slider)

        # Status Label
        self.status_label = QLabel("No video loaded.", self)
        main_layout.addWidget(self.status_label)

        # Set Main Widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.video_clip = VideoFileClip(file_path)
            self.status_label.setText(f"Loaded video: {file_path.split('/')[-1]}")
            self.timeline_slider.setRange(0, int(self.video_clip.duration * 100))
            self.timeline_slider.setValue(0)

    def slider_moved(self, position):
        if self.video_clip:
            current_time = position / 100
            self.status_label.setText(f"Current time: {current_time:.2f} sec")

    def cut_video(self):
        if self.video_clip:
            start_time = self.timeline_slider.value() / 100
            end_time = min(start_time + 5, self.video_clip.duration)  # Cut a 5-second segment
            cut_clip = self.video_clip.subclip(start_time, end_time)
            self.video_clips.append(cut_clip)
            self.status_label.setText(f"Cut segment from {start_time:.2f} to {end_time:.2f} sec.")
        else:
            self.status_label.setText("Load a video first!")

    def concatenate_videos(self):
        if self.video_clips:
            self.final_clip = concatenate_videoclips(self.video_clips)
            self.status_label.setText("Videos concatenated.")
        else:
            self.status_label.setText("No video segments to concatenate.")

    def export_video(self):
        if self.final_clip:
            export_path, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "MP4 Files (*.mp4)")
            if export_path:
                self.final_clip.write_videofile(export_path)
                self.status_label.setText(f"Exported video to {export_path}.")
        else:
            self.status_label.setText("No final video to export.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = VideoEditor()
    editor.show()
    sys.exit(app.exec_())
