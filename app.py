import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QSlider, QLabel, QStyle, QToolBar, QAction, QStatusBar)
from PyQt5.QtCore import Qt, QUrl  # Import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from moviepy.editor import VideoFileClip


class VideoEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Advanced Video Editor")
        self.setGeometry(100, 100, 1280, 720)

        # Video playback components
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        # Video clip and editing parameters
        self.video_clip = None
        self.in_point = None
        self.out_point = None

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Video display
        main_layout.addWidget(self.video_widget)
        self.media_player.setVideoOutput(self.video_widget)

        # Playback controls
        control_layout = QHBoxLayout()

        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_pause_video)
        control_layout.addWidget(self.play_button)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        control_layout.addWidget(self.slider)

        self.position_label = QLabel("00:00")
        control_layout.addWidget(self.position_label)

        main_layout.addLayout(control_layout)

        # Editing tools
        edit_layout = QHBoxLayout()

        self.set_in_button = QPushButton("Set In Point")
        self.set_in_button.clicked.connect(self.set_in_point)
        edit_layout.addWidget(self.set_in_button)

        self.set_out_button = QPushButton("Set Out Point")
        self.set_out_button.clicked.connect(self.set_out_point)
        edit_layout.addWidget(self.set_out_button)

        self.cut_button = QPushButton("Cut Video")
        self.cut_button.clicked.connect(self.cut_video)
        edit_layout.addWidget(self.cut_button)

        self.preview_button = QPushButton("Preview")
        self.preview_button.clicked.connect(self.preview_edit)
        edit_layout.addWidget(self.preview_button)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_video)
        edit_layout.addWidget(self.export_button)

        main_layout.addLayout(edit_layout)

        # Set central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Menu bar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        open_action = QAction("Open Video", self)
        open_action.triggered.connect(self.load_video)
        toolbar.addAction(open_action)

        # Status bar
        self.setStatusBar(QStatusBar(self))

        # Media player signals
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.video_clip = VideoFileClip(file_path)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))  # QUrl is now defined
            self.play_button.setEnabled(True)
            self.statusBar().showMessage(f"Loaded video: {file_path.split('/')[-1]}")

    def play_pause_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.media_player.play()
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_position(self, position):
        self.slider.setValue(position)
        self.position_label.setText(f"{position//60000}:{(position//1000)%60:02}")

    def update_duration(self, duration):
        self.slider.setRange(0, duration)

    def set_in_point(self):
        if self.video_clip:
            self.in_point = self.media_player.position() / 1000
            self.statusBar().showMessage(f"Set In Point: {self.in_point:.2f} sec")

    def set_out_point(self):
        if self.video_clip:
            self.out_point = self.media_player.position() / 1000
            self.statusBar().showMessage(f"Set Out Point: {self.out_point:.2f} sec")

    def cut_video(self):
        if self.video_clip and self.in_point is not None and self.out_point is not None:
            self.video_clip = self.video_clip.subclip(self.in_point, self.out_point)
            self.statusBar().showMessage(f"Video cut from {self.in_point:.2f} to {self.out_point:.2f} sec.")
            self.in_point, self.out_point = None, None  # Reset points

    def preview_edit(self):
        if self.video_clip:
            preview_file = "preview.mp4"
            self.video_clip.write_videofile(preview_file)
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(preview_file)))
            self.media_player.play()
            self.statusBar().showMessage("Previewing edited video...")

    def export_video(self):
        if self.video_clip:
            export_path, _ = QFileDialog.getSaveFileName(self, "Export Video", "", "MP4 Files (*.mp4)")
            if export_path:
                self.video_clip.write_videofile(export_path)
                self.statusBar().showMessage(f"Exported video to {export_path}.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = VideoEditor()
    editor.show()
    sys.exit(app.exec_())
