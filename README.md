# nara_qt

The **PyQt6 binding for [nara](https://github.com/aotabekov91/nara)** — concrete Qt widget implementations of nara's abstract plug framework, plus a library of ready-to-use views for building modal desktop applications.

[nara](https://github.com/aotabekov91/nara) gives you the plug architecture, modal key handling, and config system. nara_qt gives you the actual GUI: a `QApplication`-backed `App`, a `QMainWindow`-backed `View`, and a whole "gizmo" library of tabbed/tiled/docked/status-bar/toolbar/tree/list widgets that compose into a real application window.

If nara is the skeleton, nara_qt is the skin.

---

## What you get

- **`App(nara.App, QObject)`** — a Qt-backed application with `QApplication` set up for you, plus four lifecycle signals (`appSoonStarts`, `appViewIsLaunched`, `appIsLaunched`, `appSoonQuits`).
- **`View(WindowView)`** — a `QMainWindow` subclass pre-configured with a center `TabView`, a `Docks` panel, and a `StatusBarView`. Ready to show on boot.
- **`vimo.View(nara.View)`** — Qt signal versions of every view lifecycle event (`resized`, `painted`, `focusLost`, `focusGained`, `modelChanged`, `viewIsRedrawn`, …).
- **`gizmo.*`** — a widget library: `WindowView`, `TabView`, `TileView`, `Docks`, `StatusBarView`, `ToolView`, `TreeView`, `ItemListView`, `ElementListView`.
- **Qt-aware managers** — `Plugman`, `Earman`, `Buffman`, `Stateman`, `Styleman`, `Configman` all subclassed from nara's core managers with Qt signal/slot integration.

## Requirements

- Python 3.9+
- [PyQt6](https://pypi.org/project/PyQt6/) 6.8.0
- [nara](https://github.com/aotabekov91/nara) (the core framework)

## Installation

### From source

```bash
git clone https://github.com/aotabekov91/nara_qt.git
cd nara_qt
pip install .
```

Poetry will pull in PyQt6 and nara automatically.

## Quick start — a minimal modal Qt app

```python
from nara_qt.app import App
from nara_qt.app.view import View

class MyApp(App):
    """Three-line app: boots a QMainWindow, loads plugs, enters Qt event loop."""
    pass

app = MyApp()
app.activate()   # loads plugs from <config>/autorun/, shows the main window
app.run()        # emits appSoonStarts → appViewIsLaunched → appIsLaunched → qapp.exec()
```

That's it. On `activate()`:

1. `setupQApp()` creates `QApplication(sys.argv)`.
2. `setupParts()` constructs the seven managers (with Qt-aware subclasses).
3. `setupView()` instantiates the `View`, which builds:
   - `self.main` — a `TabView` (the center area)
   - `self.docks` — a `Docks` widget (dockable panels)
   - `self.bar` — a `StatusBarView` (status bar at the bottom)
4. `loadAutorunPlugs()` discovers plugs in `<config>/autorun/` and loads them.
5. `run()` emits the lifecycle signals and enters `qapp.exec()`.

You now have a window with a tabbed center, dockable side panels, and a status bar — and any plugs you drop in `autorun/` are live.

## The lifecycle signals

`App` emits four Qt signals during startup and shutdown. Plugs connect to these to know when it's safe to do their work:

| Signal | When | Typical use |
| --- | --- | --- |
| `appSoonStarts` | Just before the Qt event loop starts | Last-minute setup that needs the qapp to exist |
| `appViewIsLaunched` | After the main view is created but before plugs are loaded | Plug wants to hook into the view's signals |
| `appIsLaunched` | After plugs are loaded, app is fully running | Connect to other plugs, register delegations |
| `appSoonQuits` | On shutdown | Save state, disconnect signals |

Example — a plug that waits for the app to be fully launched before connecting to the Normal plug:

```python
from nara import Plug

class MyPlug(Plug):
    def setup(self):
        super().setup()
        if self.app.running:
            self.connectToNormal()
        else:
            self.app.appIsLaunched.connect(self.connectToNormal)

    def connectToNormal(self):
        normal = self.app.plugman.getPlug('Normal')
        if normal:
            normal.stateChanged.connect(self.onStateChanged)
```

## The `View` — a ready-made main window

`nara_qt.app.view.View` extends `gizmo.WindowView` (which is `vimo.View` + `QtWidgets.QMainWindow`). Out of the box it has:

| Attribute | Type | Role |
| --- | --- | --- |
| `self.main` | `gizmo.TabView` | Center area — holds tabbed sub-views |
| `self.docks` | `gizmo.Docks` | Dockable panel container (left/right/bottom) |
| `self.bar` | `gizmo.StatusBarView` | Status bar at the bottom |

The default `TabView` is configured to use `TileView` as its tab class — so tabs can be split into tiles side-by-side.

To add a view to the center area:

```python
self.app.view.addView(my_subview)
```

To dock a panel:

```python
self.app.view.docks.addView(my_panel, area=Qt.LeftDockWidgetArea)
```

## The `gizmo` widget library

Every gizmo is a `vimo.View` subclass (so it has the full signal set) wrapped around a Qt widget. They compose: a `TabView` holds `TileView`s, a `TileView` holds arbitrary views, a `Docks` holds dockable views, etc.

| Widget | Qt base | Role |
| --- | --- | --- |
| `WindowView` | `QMainWindow` | Top-level window — the app's root view |
| `TabView` | (custom) | Tabbed container — holds multiple views, one visible at a time |
| `TileView` | (custom) | Tiled container — holds multiple views side-by-side |
| `Docks` | `QDockWidget` area | Dockable panel container |
| `StatusBarView` | `QStatusBar` | Status bar — shows messages, state indicators |
| `ToolView` | `QToolBar` | Toolbar — action buttons |
| `TreeView` | `QTreeView` | Tree widget — file explorers, outline views |
| `ItemListView` | `QListView` | List widget — quickpick, command palette |
| `ElementListView` | `QListView` | List widget for rendered elements |

All are importable from `nara_qt.gizmo`:

```python
from nara_qt import gizmo

panel = gizmo.TreeView(label='P', parent=self, app=self.app,
                      manager=self.app.view, name='ProjectTree')
self.app.view.docks.addView(panel)
```

## The `vimo.View` — Qt signals for every view event

nara's abstract `View` defines the lifecycle; nara_qt's `vimo.View` adds Qt signals so other plugs can subscribe:

```python
class View(nara.View):
    cleanUpWanted   = pyqtSignal()
    viewIsRedrawn   = pyqtSignal()
    resized         = pyqtSignal(object)
    painted         = pyqtSignal(object, object)
    focusLost       = pyqtSignal(object)
    focusGained     = pyqtSignal(object)
    closeWanted     = pyqtSignal(object)
    modelLoaded     = pyqtSignal(object, object)
    modelChanged    = pyqtSignal(object)
    indexChanged    = pyqtSignal(object)
    posIndexChanged = pyqtSignal(object, object, object)
    identifierChanged = pyqtSignal(object, object, object)
    geometryChanged = pyqtSignal()
    viewIsToBeRedrawn = pyqtSignal()
```

The `event()` override auto-emits `resized` on `QEvent.Type.Resize` and `painted` on `QEvent.Type.Paint` — so any plug can listen for these without subclassing the view.

Example — a plug that redraws a minimap whenever the main view resizes:

```python
class Minimap(Plug):
    def setup(self):
        super().setup()
        self.app.appIsLaunched.connect(self.connect_to_view)

    def connect_to_view(self):
        view = self.app.view
        if view:
            view.resized.connect(self.redraw_minimap)
            view.painted.connect(self.redraw_minimap)
```

## The managers — Qt-aware subclasses

Each manager in `nara_qt.app/` subclasses its nara counterpart and integrates with Qt's signal/slot system where needed:

| Manager | nara base | Qt additions |
| --- | --- | --- |
| `App` | `nara.App` + `QObject` | `QApplication` setup, 4 lifecycle signals |
| `Plugman` | `nara.Plugman` | (same API, runs on Qt event loop) |
| `Earman` | `nara.Earman` | Qt key event handling |
| `Buffman` | `nara.Buffman` | `viewCreated` as a Qt signal |
| `Stateman` | `nara.Stateman` | Qt-aware state transitions |
| `Styleman` | `nara.Styleman` | QSS stylesheet application |
| `Configman` | `nara.Configman` | (same API, TOML config) |

You usually don't construct these directly — `App.setupParts()` does it for you.

## How it composes with nara

```
nara (core framework)
  ├── Plug              ← abstract base class
  ├── App               ← abstract app (no GUI)
  ├── Plugman           ← abstract plug loader
  ├── Earman            ← abstract key listener
  ├── vimo.View         ← abstract view
  └── ...

nara_qt (PyQt6 binding)
  ├── app.App           ← nara.App + QObject, creates QApplication
  ├── app.View          ← gizmo.WindowView (QMainWindow)
  ├── app.Plugman       ← nara.Plugman (Qt-aware)
  ├── app.Earman        ← nara.Earman (Qt key events)
  ├── vimo.View         ← nara.View + Qt signals
  └── gizmo.*           ← concrete Qt widgets (TabView, Docks, StatusBarView, ...)
```

nara defines **what** a plug-in modal app is. nara_qt provides **how** it renders and handles input on Qt6.

## File layout

```
nara_qt/
├── src/nara_qt/
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── app.py            ← App(nara.App, QObject)
│   │   ├── view.py           ← View (the main window)
│   │   ├── plugman.py        ← Qt-aware Plugman
│   │   ├── earman.py         ← Qt-aware Earman (key handling)
│   │   ├── buffman.py        ← Qt-aware Buffman
│   │   ├── stateman.py       ← Qt-aware Stateman
│   │   ├── styleman.py       ← QSS stylesheet manager
│   │   ├── configman.py      ← TOML config (same as nara)
│   │   ├── utils.py
│   │   ├── gizmo/
│   │   └── vimo/
│   ├── gizmo/                ← widget library
│   │   ├── __init__.py       ← exports all gizmo views
│   │   ├── window.py         ← WindowView (QMainWindow)
│   │   ├── tab.py            ← TabView
│   │   ├── tile/             ← TileView (tiled layout)
│   │   ├── dock/             ← Docks (dockable panels)
│   │   ├── bar.py            ← StatusBarView
│   │   ├── tool/             ← ToolView (toolbar)
│   │   ├── tree.py           ← TreeView
│   │   ├── itemlist/         ← ItemListView
│   │   ├── elementlist/      ← ElementListView
│   │   ├── element/          ← Element base
│   │   └── layout/           ← Layout helpers
│   └── vimo/                 ← Qt-signaling View
│       ├── __init__.py
│       ├── view.py           ← View(nara.View) + pyqtSignals
│       ├── model.py          ← Qt-aware Model
│       └── item.py
├── pyproject.toml            ← poetry build config
├── LICENSE                   ← GPL-3.0
└── README.md
```

## Dependencies

```toml
[tool.poetry.dependencies]
python  = "^3.9"
PyQt6   = "==6.8.0"
nara    = { git = "https://github.com/aotabekov91/nara" }
```

nara_qt pins PyQt6 to 6.8.0 for stability. If you need a newer PyQt6, override the pin in your app's `pyproject.toml`.

## A real app built on nara_qt

[ayleen](https://github.com/aotabekov91/ayleen) is a modalizer built on nara + nara_qt. Its core is essentially:

```python
from nara_qt.app import App

class Ayleen(App):
    pass

app = Ayleen()
app.activate()
app.run()
```

…plus a set of nara plugs in `~/.config/ayleen/autorun/` providing the Normal mode, motion commands, editing, leap history ([leaper](https://github.com/aotabekov91/leaper)), SQLite-backed tables ([table_sqlite](https://github.com/aotabekov91/table_sqlite)), and the Picky plugin manager itself.

## License

See [GPL-3.0](LICENSE).
