import threading
import queue
import time
from typing import List
import pyttsx3

class VoiceManager:
    def __init__(self, config):
        self.config = config
        self.task_queue = queue.Queue()
        self.worker_thread = None
        self.running = True
        self._start_worker()

    def _start_worker(self):
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        while self.running:
            try:
                texts = self.task_queue.get(timeout=0.5)
                if texts is None:
                    break
                for text in texts:
                    if not self.config.get("voice_enabled", True):
                        break
                    self._speak_single(text)
                    time.sleep(0.05)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"语音工作线程错误: {e}")

    def _speak_single(self, text: str):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"TTS 播报失败 ('{text}'): {e}")

    def speak(self, texts: List[str]):
        if not self.config.get("voice_enabled", True):
            return
        self._clear_pending_tasks()
        self.task_queue.put(texts)

    def _clear_pending_tasks(self):
        try:
            while True:
                self.task_queue.get_nowait()
        except queue.Empty:
            pass

    def speak_single(self, text: str):
        self.speak([text])

    def shutdown(self):
        self.running = False
        self.task_queue.put(None)
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1.0)