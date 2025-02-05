"""Virtual Desktop Name Display Application.

Windows用の仮想デスクトップ名表示アプリケーション。
常に最前面に表示される小さなウィンドウに、現在の仮想デスクトップ名を表示します。
デスクトップ名に応じて背景色と文字色が自動的に変更されます。
"""

import hashlib
import random
import tkinter as tk
from dataclasses import dataclass
from typing import Callable

from pyvda import VirtualDesktop


@dataclass
class ColorScheme:
    """背景色と前景色の組み合わせを表すデータクラス."""

    background: str
    foreground: str

    @staticmethod
    def from_name(name: str) -> "ColorScheme":
        """文字列からカラースキームを生成する.

        Args:
            name: カラースキームの生成元となる文字列

        Returns:
            生成されたカラースキーム
        """
        seed = int(hashlib.md5(name.encode()).hexdigest(), 16)
        random.seed(seed)
        bg_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        fg_color = f"#{random.randint(0, 0xFFFFFF):06x}"

        def brightness(color: str) -> float:
            """16進カラーコードから明度を計算."""
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return (r * 299 + g * 587 + b * 114) / 1000

        # 背景色と文字色の明度差が小さい場合は文字色を白または黒に調整
        if abs(brightness(bg_color) - brightness(fg_color)) < 125:
            fg_color = "#ffffff" if brightness(bg_color) < 128 else "#000000"

        return ColorScheme(bg_color, fg_color)


class DraggableWindow:
    """ドラッグ可能なウィンドウを実現するクラス."""

    def __init__(self, widget: tk.Tk) -> None:
        """イニシャライザ.

        Args:
            widget: ドラッグ可能にするウィジェット
        """
        self.widget = widget
        self.dragging = False
        self.start_x = 0
        self.start_y = 0

        widget.bind("<Button-1>", self.start_drag)
        widget.bind("<B1-Motion>", self.do_drag)
        widget.bind("<ButtonRelease-1>", self.stop_drag)

    def start_drag(self, event: tk.Event) -> None:
        """ドラッグ開始時の処理."""
        self.dragging = True
        self.start_x = event.x_root - self.widget.winfo_x()
        self.start_y = event.y_root - self.widget.winfo_y()

    def do_drag(self, event: tk.Event) -> None:
        """ドラッグ中の処理."""
        if self.dragging:
            x = event.x_root - self.start_x
            y = event.y_root - self.start_y
            self.widget.geometry(f"+{x}+{y}")

    def stop_drag(self, event: tk.Event) -> None:  # noqa: ARG002
        """ドラッグ終了時の処理."""
        self.dragging = False


class DesktopNameDisplay:
    """仮想デスクトップ名を表示するメインアプリケーションクラス."""

    def __init__(self) -> None:
        """イニシャライザ."""
        self.root = tk.Tk()
        self.setup_window()
        self.current_name: str | None = None
        self.label = self.create_label()
        self.draggable = DraggableWindow(self.root)
        self.setup_menu()

    def setup_window(self) -> None:
        """メインウィンドウの設定."""
        self.root.title("Virtual Desktop Name")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

    def create_label(self) -> tk.Label:
        """表示用ラベルの作成.

        Returns:
            設定済みのラベルウィジェット
        """
        name = self.get_desktop_name()
        colors = ColorScheme.from_name(name)
        self.root.config(bg=colors.background)
        label = tk.Label(
            self.root,
            text=name,
            font=("Helvetica", 32),
            bg=colors.background,
            fg=colors.foreground,
        )
        label.pack(padx=20, pady=20)
        return label

    def setup_menu(self) -> None:
        """右クリックメニューの設定."""
        self.root.bind("<Button-3>", self.show_exit_menu)

    def show_exit_menu(self, event: tk.Event) -> None:
        """終了メニューを表示する."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="終了", command=self.root.quit)
        menu.post(event.x_root, event.y_root)

    @staticmethod
    def get_desktop_name() -> str:
        """現在の仮想デスクトップ名を取得する.

        Returns:
            仮想デスクトップ名(未設定の場合は"Desktop X"形式)
        """
        current = VirtualDesktop.current()
        return current.name if current.name else f"Desktop {current.number}"

    def update_display(self) -> None:
        """仮想デスクトップ名と色設定を更新する."""
        new_name = self.get_desktop_name()
        if new_name != self.current_name:
            self.current_name = new_name
            colors = ColorScheme.from_name(new_name)
            self.label.config(text=new_name, bg=colors.background, fg=colors.foreground)
            self.root.config(bg=colors.background)
        self.root.after(500, self.update_display)

    def run(self) -> None:
        """アプリケーションを実行する."""
        self.root.after(500, self.update_display)
        self.root.mainloop()


def main() -> None:
    """アプリケーションのエントリーポイント."""
    app = DesktopNameDisplay()
    app.run()


if __name__ == "__main__":
    main()
