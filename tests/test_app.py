"""Virtual Desktop Name Display Application のテスト."""

import tkinter as tk
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from deskname.app import ColorScheme, DesktopNameDisplay


def test_color_scheme_from_name() -> None:
    """ColorScheme.from_name()のテスト."""
    # 同じ名前からは同じ色が生成される
    colors1 = ColorScheme.from_name("Test Desktop")
    colors2 = ColorScheme.from_name("Test Desktop")
    assert colors1 == colors2

    # 異なる名前からは異なる色が生成される
    colors3 = ColorScheme.from_name("Another Desktop")
    assert colors1 != colors3

    # 背景色と文字色は6桁の16進数
    assert len(colors1.background) == 7  # #を含めて7文字
    assert len(colors1.foreground) == 7
    assert colors1.background.startswith("#")
    assert colors1.foreground.startswith("#")


@pytest.fixture
def mock_virtual_desktop() -> Generator[MagicMock, None, None]:
    """VirtualDesktop.current()のモック."""
    with patch("deskname.app.VirtualDesktop") as mock:
        current = MagicMock()
        current.name = "Test Desktop"
        current.number = 1
        mock.current.return_value = current
        yield mock


@pytest.fixture
def app(mock_virtual_desktop: MagicMock) -> DesktopNameDisplay:
    """テスト用のアプリケーションインスタンス."""
    return DesktopNameDisplay()


def test_desktop_name_display_init(app: DesktopNameDisplay) -> None:
    """DesktopNameDisplayの初期化テスト."""
    assert isinstance(app.root, tk.Tk)
    assert app.root.title() == "Virtual Desktop Name"
    assert app.root.overrideredirect()
    assert app.root.attributes("-topmost")
    assert not app.root.resizable(True, True)


def test_desktop_name_display_get_desktop_name(
    app: DesktopNameDisplay, mock_virtual_desktop: MagicMock
) -> None:
    """get_desktop_name()のテスト."""
    # 名前が設定されている場合
    assert app.get_desktop_name() == "Test Desktop"

    # 名前が設定されていない場合
    mock_virtual_desktop.current.return_value.name = None
    mock_virtual_desktop.current.return_value.number = 2
    assert app.get_desktop_name() == "Desktop 2"


def test_desktop_name_display_update(
    app: DesktopNameDisplay, mock_virtual_desktop: MagicMock
) -> None:
    """update_display()のテスト."""
    initial_text = app.label["text"]
    initial_bg = app.label["bg"]
    initial_fg = app.label["fg"]

    # デスクトップ名が変更された場合
    mock_virtual_desktop.current.return_value.name = "New Desktop"
    app.update_display()

    assert app.label["text"] == "New Desktop"
    assert app.label["bg"] != initial_bg
    assert app.label["fg"] != initial_fg

    # デスクトップ名が同じ場合
    app.update_display()
    assert app.label["text"] == "New Desktop"
    assert app.label["bg"] == app.label["bg"]
    assert app.label["fg"] == app.label["fg"]
