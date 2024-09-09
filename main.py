import cv2
import tkinter as tk
from threading import Thread

class VideoRecorder:
    def __init__(self, window_title="Video Recorder"):
        self.recording = True
        self.paused = False
        self.video_capture = cv2.VideoCapture(0)
        self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_writer = cv2.VideoWriter('output_4k.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (self.frame_width, self.frame_height))
        self.running = True
        self.thread = Thread(target=self.record_video)
        self.thread.start()


        self.root = tk.Tk()
        self.root.title(window_title)
        self.root.geometry("300x250")

        self.start_stop_button = tk.Button(self.root, text="Pause/Resume", command=self.toggle_pause)
        self.start_stop_button.pack(pady=20)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording)
        self.stop_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Запись запущена", font=('Arial', 12))
        self.status_label.pack(pady=10)

    def record_video(self):
        while self.running:
            if not self.paused:
                ret, frame = self.video_capture.read()
                if not ret:
                    print("Ошибка: не удалось захватить кадр.")
                    break

                if self.recording:
                    self.video_writer.write(frame)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            print("Запись приостановлена.")
            self.status_label.config(text="Запись приостановлена.")
        else:
            print("Запись возобновлена.")
            self.status_label.config(text="Запись: Возобновлена")
# TODO отображение в консоли надо ли?
    def stop_recording(self):
        self.recording = False
        self.running = False
        self.video_capture.release()
        self.video_writer.release()
        self.root.destroy()
        print("Запись остановлена и видео сохранено как output_4k.avi")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    recorder = VideoRecorder()
    recorder.run()
