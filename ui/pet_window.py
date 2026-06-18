from PySide6.QtWidgets import QWidget, QLabel, QMenu, QSystemTrayIcon, QApplication
from PySide6.QtGui import QMovie, QAction, QIcon, QColor
from PySide6.QtCore import Qt, QTimer, QPoint
import data.pet_config as cfg
import data.pet_actions as act
import data.interactions as inter
import data.themes as theme

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        # 置顶、无边框、透明窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
        self.setWindowOpacity(cfg.PET_ALPHA)

        # 宠物显示标签
        self.label_pet = QLabel(self)
        self.label_pet.setFixedSize(self.width(), self.height())
        self.current_anim_key = "idle"
        self.load_anim(self.current_anim_key)

        # 自动移动定时器
        self.timer_move = QTimer()
        self.timer_move.timeout.connect(self.auto_walk)
        self.timer_move.start(3000)
        self.move_direction = 1

        # 状态衰减定时器（每分钟扣数值）
        self.timer_status = QTimer()
        self.timer_status.timeout.connect(self.status_decay)
        self.timer_status.start(60000)

        # 拖拽标记
        self.drag_start_pos = QPoint()
        self.is_dragging = False

        # 托盘右键菜单
        self.tray = QSystemTrayIcon(QIcon(), self)
        self.build_menu()

    # 加载动画
    def load_anim(self, anim_key):
        path = act.PET_ACTIONS.get(anim_key, act.PET_ACTIONS["idle"])
        movie = QMovie(path)
        movie.setScaledSize(self.label_pet.size())
        self.label_pet.setMovie(movie)
        movie.start()
        self.current_anim_key = anim_key

    # 自动左右行走
    def auto_walk(self):
        screen_width = self.screen().geometry().width()
        new_x = self.x() + self.move_direction * cfg.MOVE_SPEED
        # 碰到屏幕边缘反向
        if new_x <= 0 or new_x >= screen_width - self.width():
            self.move_direction *= -1
            self.load_anim("walk")
        self.move(new_x, self.y())
        self.load_anim("idle")

    # 情绪数值自动衰减
    def status_decay(self):
        inter.PET_STATUS["hunger"] -= 1
        inter.PET_STATUS["mood"] -= 1
        inter.PET_STATUS["energy"] -= 1

    # 右键菜单
    def build_menu(self):
        menu = QMenu()
        act_feed = QAction("喂食", self)
        act_feed.triggered.connect(lambda: self.do_interact("feed"))
        act_play = QAction("玩耍", self)
        act_play.triggered.connect(lambda: self.do_interact("play"))
        act_rest = QAction("休息", self)
        act_rest.triggered.connect(lambda: self.do_interact("rest"))
        act_hide = QAction("隐藏宠物", self)
        act_hide.triggered.connect(self.hide)
        act_exit = QAction("退出程序", self)
        act_exit.triggered.connect(QApplication.quit)

        menu.addAction(act_feed)
        menu.addAction(act_play)
        menu.addAction(act_rest)
        menu.addSeparator()
        menu.addAction(act_hide)
        menu.addAction(act_exit)
        self.tray.setContextMenu(menu)
        self.tray.show()

    # 交互功能，提升数值
    def do_interact(self, opt_key):
        for item in inter.INTERACTIONS:
            if item["action"] == opt_key:
                if "饱食度" in item["effect"]:
                    inter.PET_STATUS["hunger"] += 20
                if "心情" in item["effect"]:
                    inter.PET_STATUS["mood"] += 20
                if "体力" in item["effect"]:
                    inter.PET_STATUS["energy"] += 20
        self.load_anim("click")

    # 鼠标拖拽窗口
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            self.load_anim("click")
        elif event.button() == Qt.RightButton:
            self.tray.contextMenu().exec(event.globalPos())

    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_pos)

    def mouseReleaseEvent(self, event):
        self.is_dragging = False
        self.load_anim("idle")