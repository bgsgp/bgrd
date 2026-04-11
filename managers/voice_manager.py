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
        """启动后台工作线程，顺序处理语音任务"""
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        while self.running:
            try:
                texts = self.task_queue.get(timeout=0.5)
                if texts is None:  # 退出信号
                    break
                # 逐个播报，每个文本使用独立的引擎实例
                for text in texts:
                    if not self.config.get("voice_enabled", True):
                        break
                    self._speak_single(text)
                    # 略微延迟，避免引擎资源冲突
                    time.sleep(0.05)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"语音工作线程错误: {e}")

    def _speak_single(self, text: str):
        """播报单个文本，每次创建新引擎，确保完整输出"""
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"TTS 播报失败 ('{text}'): {e}")

    def speak(self, texts: List[str]):
        """外部调用：将文本列表加入队列，立即返回"""
        if not self.config.get("voice_enabled", True):
            return
        # 清空旧任务（只保留当前最新一次抽选的所有文本）
        self._clear_pending_tasks()
        # 加入新任务（整个列表作为一个任务，但内部会逐条播报）
        self.task_queue.put(texts)

    def _clear_pending_tasks(self):
        """清空队列中未处理的任务"""
        try:
            while True:
                self.task_queue.get_nowait()
        except queue.Empty:
            pass

    def speak_single(self, text: str):
        self.speak([text])

    def shutdown(self):
        """程序退出时调用，停止工作线程"""
        self.running = False
        self.task_queue.put(None)
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1.0)