
import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class VehicleQuote:
    name: str
    code: str
    base_fare: float
    per_km: float
    multiplier: float
    capacity: int
    eta_min: int
    color: str


class UberLiveSimulation(tk.Tk):
    """
    Uber-inspired ride booking simulation.

    Features:
    - Large interactive map
    - Pickup selection from named locations
    - Destination selection from dropdown OR by clicking the map
    - Moving nearby vehicle simulation
    - Live fare quotes and ETA updates
    - Driver-to-passenger pickup animation
    - Passenger-to-destination trip animation
    - Fare receipt and reset support

    No external packages are required.
    """

    APP_BG = "#F2F4F6"
    SURFACE = "#FFFFFF"
    TEXT = "#111827"
    MUTED = "#6B7280"
    BORDER = "#E5E7EB"
    BLACK = "#111111"
    GREEN = "#06C167"
    GREEN_DARK = "#038A49"
    BLUE = "#276EF1"
    ORANGE = "#F59E0B"
    RED = "#EF4444"
    MAP_BG = "#EEF1F3"
    ROAD = "#D7DCE1"
    ROAD_EDGE = "#C9CED4"
    PARK = "#D9EBD6"
    WATER = "#CFE8F8"

    MAP_WIDTH = 980
    MAP_HEIGHT = 650

    LOCATIONS = {
        "Dhanmondi": (150, 150),
        "Farmgate": (355, 105),
        "Gulshan": (690, 120),
        "Banani": (590, 205),
        "Mohakhali": (465, 235),
        "Shahbag": (285, 345),
        "Motijheel": (575, 420),
        "Old Dhaka": (330, 535),
        "Uttara": (815, 330),
        "Airport": (825, 175),
        "Mirpur": (115, 330),
        "Bashundhara": (760, 500),
    }

    DRIVERS = [
        {"name": "Arif Hasan", "rating": 4.92, "car": "Toyota Axio", "plate": "DHAKA-GA-21-4587"},
        {"name": "Nusrat Jahan", "rating": 4.88, "car": "Honda Grace", "plate": "DHAKA-METRO-16-2034"},
        {"name": "Sakib Ahmed", "rating": 4.95, "car": "Toyota Premio", "plate": "DHAKA-GHA-18-7741"},
        {"name": "Rafiul Islam", "rating": 4.84, "car": "Suzuki WagonR", "plate": "DHAKA-CHA-13-9206"},
        {"name": "Tanjim Rahman", "rating": 4.90, "car": "Honda Vezel", "plate": "DHAKA-GA-19-6642"},
    ]

    VEHICLE_QUOTES = {
        "Bike": VehicleQuote("Bike", "B", 35, 18, 0.82, 1, 2, "#8B5CF6"),
        "UberX": VehicleQuote("UberX", "X", 70, 30, 1.00, 4, 3, "#111111"),
        "Comfort": VehicleQuote("Comfort", "C", 100, 40, 1.24, 4, 4, "#276EF1"),
        "XL": VehicleQuote("XL", "XL", 140, 52, 1.58, 6, 6, "#F59E0B"),
    }

    ROAD_SEGMENTS = [
        ((45, 175), (930, 175)),
        ((45, 305), (930, 305)),
        ((70, 455), (900, 455)),
        ((225, 40), (225, 600)),
        ((455, 45), (455, 590)),
        ((650, 45), (650, 605)),
        ((820, 75), (820, 565)),
        ((90, 90), (360, 360)),
        ((360, 360), (690, 120)),
        ((280, 535), (575, 420)),
        ((575, 420), (825, 175)),
    ]

    def __init__(self):
        super().__init__()
        self.title("Uber Live Ride Simulation — V3 Fixed")
        self.geometry("1380x820")
        self.minsize(1080, 680)
        self.configure(bg=self.APP_BG)

        self.selected_vehicle = "UberX"
        self.pickup_name = tk.StringVar(value="Dhanmondi")
        self.destination_name = tk.StringVar(value="Choose on map")
        self.passenger_name = tk.StringVar(value="Tanvir Robin")
        self.payment_method = tk.StringVar(value="Cash")

        self.destination_point: Optional[Tuple[float, float]] = None
        self.destination_label = "Choose on map"
        self.ride_active = False
        self.trip_completed = False
        self.animation_job = None
        self.live_vehicle_job = None
        self.quote_job = None
        self.driver_record = None
        self.assigned_vehicle = None
        self.assigned_live_id = None
        self.route_points: List[Tuple[float, float]] = []
        self.route_distance_km = 0.0
        self.current_fare = 0.0
        self.elapsed_seconds = 0

        self.live_vehicles: Dict[int, dict] = {}
        self.vehicle_cards: Dict[str, dict] = {}

        self._setup_styles()
        self._build_header()
        self._build_main_layout()
        self._draw_map()
        self._spawn_live_vehicles()
        self._refresh_destination_from_dropdown()
        self._refresh_quotes()
        self._start_live_vehicle_loop()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Modern.TCombobox",
            padding=10,
            fieldbackground="#F9FAFB",
            background="#F9FAFB",
            foreground=self.TEXT,
            bordercolor=self.BORDER,
            arrowsize=15,
        )
        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", "#F9FAFB"), ("disabled", "#F3F4F6")],
            foreground=[("disabled", "#9CA3AF")],
            selectbackground=[("readonly", "#F9FAFB")],
            selectforeground=[("readonly", self.TEXT)],
        )
        style.configure(
            "Ride.Horizontal.TProgressbar",
            troughcolor="#E5E7EB",
            background=self.GREEN,
            bordercolor="#E5E7EB",
            lightcolor=self.GREEN,
            darkcolor=self.GREEN,
            thickness=10,
        )

    def _build_header(self):
        header = tk.Frame(self, bg=self.BLACK, height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="UBER",
            bg=self.BLACK,
            fg="white",
            font=("Helvetica", 22, "bold"),
        ).pack(side="left", padx=(24, 8))

        tk.Label(
            header,
            text="LIVE RIDE SIMULATION",
            bg=self.BLACK,
            fg="#D1D5DB",
            font=("Helvetica", 10, "bold"),
        ).pack(side="left")

        self.header_status = tk.Label(
            header,
            text="● ONLINE",
            bg="#183C2A",
            fg="#45E991",
            font=("Helvetica", 10, "bold"),
            padx=12,
            pady=7,
        )
        self.header_status.pack(side="right", padx=24)

    def _build_main_layout(self):
        body = tk.Frame(self, bg=self.APP_BG)
        body.pack(fill="both", expand=True, padx=16, pady=16)

        self.sidebar = tk.Frame(
            body,
            bg=self.SURFACE,
            width=350,
            highlightthickness=1,
            highlightbackground=self.BORDER,
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 12))
        self.sidebar.pack_propagate(False)

        self.map_shell = tk.Frame(
            body,
            bg=self.SURFACE,
            highlightthickness=1,
            highlightbackground=self.BORDER,
        )
        self.map_shell.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self._build_map_shell()

    def _label(self, parent, text, size=10, bold=False, color=None, bg=None):
        return tk.Label(
            parent,
            text=text,
            bg=bg or self.SURFACE,
            fg=color or self.TEXT,
            font=("Helvetica", size, "bold" if bold else "normal"),
        )


    def _build_sidebar(self):
        panel = self.sidebar

        # The action area stays permanently visible at the bottom.
        footer = tk.Frame(
            panel,
            bg=self.SURFACE,
            highlightthickness=1,
            highlightbackground=self.BORDER,
        )
        footer.pack(side="bottom", fill="x")

        self.selected_ride_label = tk.Label(
            footer,
            text=f"Selected ride: {self.selected_vehicle}",
            bg=self.SURFACE,
            fg=self.GREEN_DARK,
            anchor="w",
            font=("Helvetica", 9, "bold"),
        )
        self.selected_ride_label.pack(fill="x", padx=18, pady=(11, 3))

        self.fare_summary = tk.Frame(footer, bg="#F6F7F8", padx=12, pady=9)
        self.fare_summary.pack(fill="x", padx=18, pady=(0, 8))

        self.summary_route = tk.Label(
            self.fare_summary,
            text="Select a destination",
            bg="#F6F7F8",
            fg=self.MUTED,
            anchor="w",
            justify="left",
            wraplength=285,
            font=("Helvetica", 9),
        )
        self.summary_route.pack(fill="x")

        self.summary_price = tk.Label(
            self.fare_summary,
            text="Estimated fare: —",
            bg="#F6F7F8",
            fg=self.TEXT,
            anchor="w",
            font=("Helvetica", 16, "bold"),
        )
        self.summary_price.pack(fill="x", pady=(3, 0))

        self.request_button = tk.Button(
            footer,
            text="CHOOSE DESTINATION",
            command=self.request_ride,
            bg="#9CA3AF",
            fg="white",
            activebackground="#6B7280",
            activeforeground="white",
            disabledforeground="#F3F4F6",
            relief="flat",
            cursor="hand2",
            font=("Helvetica", 11, "bold"),
            pady=12,
            state="disabled",
        )
        self.request_button.pack(fill="x", padx=18, pady=(0, 7))

        self.reset_button = tk.Button(
            footer,
            text="RESET SIMULATION",
            command=self.reset_simulation,
            bg="#E5E7EB",
            fg=self.TEXT,
            activebackground="#D1D5DB",
            relief="flat",
            cursor="hand2",
            font=("Helvetica", 9, "bold"),
            pady=8,
        )
        self.reset_button.pack(fill="x", padx=18, pady=(0, 12))

        # Everything above the fixed footer is scrollable.
        scroll_host = tk.Frame(panel, bg=self.SURFACE)
        scroll_host.pack(side="top", fill="both", expand=True)

        self.sidebar_canvas = tk.Canvas(
            scroll_host,
            bg=self.SURFACE,
            highlightthickness=0,
            bd=0,
        )
        sidebar_scrollbar = ttk.Scrollbar(
            scroll_host,
            orient="vertical",
            command=self.sidebar_canvas.yview,
        )
        self.sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)

        sidebar_scrollbar.pack(side="right", fill="y")
        self.sidebar_canvas.pack(side="left", fill="both", expand=True)

        self.sidebar_inner = tk.Frame(self.sidebar_canvas, bg=self.SURFACE)
        self.sidebar_window = self.sidebar_canvas.create_window(
            (0, 0),
            window=self.sidebar_inner,
            anchor="nw",
        )

        self.sidebar_inner.bind(
            "<Configure>",
            lambda _event: self.sidebar_canvas.configure(
                scrollregion=self.sidebar_canvas.bbox("all")
            ),
        )
        self.sidebar_canvas.bind(
            "<Configure>",
            lambda event: self.sidebar_canvas.itemconfigure(
                self.sidebar_window,
                width=event.width,
            ),
        )

        self.sidebar_canvas.bind("<Enter>", self._activate_sidebar_scroll)
        self.sidebar_canvas.bind("<Leave>", self._deactivate_sidebar_scroll)
        self.sidebar_inner.bind("<Enter>", self._activate_sidebar_scroll)
        self.sidebar_inner.bind("<Leave>", self._deactivate_sidebar_scroll)

        content = self.sidebar_inner

        top = tk.Frame(content, bg=self.SURFACE)
        top.pack(fill="x", padx=20, pady=(18, 10))

        self._label(top, "Where to?", size=23, bold=True).pack(anchor="w")
        self._label(
            top,
            "Choose a place or drop a destination pin on the map.",
            size=9,
            color=self.MUTED,
        ).pack(anchor="w", pady=(3, 0))

        form = tk.Frame(content, bg=self.SURFACE)
        form.pack(fill="x", padx=20)

        self._field_title(form, "PASSENGER")
        self.passenger_entry = tk.Entry(
            form,
            textvariable=self.passenger_name,
            bg="#F9FAFB",
            fg=self.TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.BLACK,
            font=("Helvetica", 11),
        )
        self.passenger_entry.pack(fill="x", ipady=8, pady=(0, 9))

        self._field_title(form, "PICKUP")
        self.pickup_combo = ttk.Combobox(
            form,
            textvariable=self.pickup_name,
            values=list(self.LOCATIONS.keys()),
            state="readonly",
            style="Modern.TCombobox",
            font=("Helvetica", 10),
        )
        self.pickup_combo.pack(fill="x", pady=(0, 9))
        self.pickup_combo.bind("<<ComboboxSelected>>", self._on_pickup_selected)

        self._field_title(form, "DESTINATION")
        destination_values = ["Choose on map"] + list(self.LOCATIONS.keys())
        self.destination_combo = ttk.Combobox(
            form,
            textvariable=self.destination_name,
            values=destination_values,
            state="readonly",
            style="Modern.TCombobox",
            font=("Helvetica", 10),
        )
        self.destination_combo.pack(fill="x", pady=(0, 9))
        self.destination_combo.bind("<<ComboboxSelected>>", self._on_destination_selected)

        self.drop_hint = tk.Label(
            form,
            text="Click anywhere on the map to drop the destination pin.",
            bg="#EFF6FF",
            fg=self.BLUE,
            anchor="w",
            justify="left",
            wraplength=285,
            font=("Helvetica", 9),
            padx=10,
            pady=7,
        )
        self.drop_hint.pack(fill="x", pady=(0, 10))

        self._field_title(form, "PAYMENT")
        self.payment_combo = ttk.Combobox(
            form,
            textvariable=self.payment_method,
            values=("Cash", "Card", "Mobile Banking"),
            state="readonly",
            style="Modern.TCombobox",
            font=("Helvetica", 10),
        )
        self.payment_combo.pack(fill="x", pady=(0, 10))

        line = tk.Frame(content, bg=self.BORDER, height=1)
        line.pack(fill="x", padx=20, pady=(1, 10))

        vehicle_header = tk.Frame(content, bg=self.SURFACE)
        vehicle_header.pack(fill="x", padx=20)
        self._label(vehicle_header, "Choose a ride", size=13, bold=True).pack(side="left")
        self.live_label = self._label(
            vehicle_header,
            "Live prices",
            size=9,
            color=self.GREEN,
            bold=True,
        )
        self.live_label.pack(side="right")

        self.vehicle_list = tk.Frame(content, bg=self.SURFACE)
        self.vehicle_list.pack(fill="x", padx=16, pady=(6, 14))

        for vehicle_name in self.VEHICLE_QUOTES:
            self._create_vehicle_card(vehicle_name)

        self.sidebar_canvas.after_idle(
            lambda: self.sidebar_canvas.configure(
                scrollregion=self.sidebar_canvas.bbox("all")
            )
        )

    def _activate_sidebar_scroll(self, _event=None):
        self.bind_all("<MouseWheel>", self._on_sidebar_mousewheel)
        self.bind_all("<Button-4>", self._on_sidebar_mousewheel)
        self.bind_all("<Button-5>", self._on_sidebar_mousewheel)

    def _deactivate_sidebar_scroll(self, _event=None):
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

    def _on_sidebar_mousewheel(self, event):
        if getattr(event, "num", None) == 4:
            units = -3
        elif getattr(event, "num", None) == 5:
            units = 3
        else:
            delta = getattr(event, "delta", 0)
            if delta == 0:
                return
            units = -1 if delta > 0 else 1
            if abs(delta) >= 120:
                units = int(-delta / 120)

        self.sidebar_canvas.yview_scroll(units, "units")

    def _field_title(self, parent, text):
        self._label(parent, text, size=8, bold=True, color=self.MUTED).pack(anchor="w", pady=(0, 4))


    def _create_vehicle_card(self, vehicle_name):
        quote = self.VEHICLE_QUOTES[vehicle_name]

        card = tk.Frame(
            self.vehicle_list,
            bg=self.SURFACE,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            cursor="hand2",
        )
        card.pack(fill="x", pady=4)

        icon_canvas = tk.Canvas(
            card,
            width=52,
            height=46,
            bg=self.SURFACE,
            highlightthickness=0,
            cursor="hand2",
        )
        icon_canvas.pack(side="left", padx=(8, 4), pady=4)
        self._draw_car_icon(
            icon_canvas,
            26,
            23,
            quote.color,
            quote.code,
            scale=1.0,
        )

        middle = tk.Frame(card, bg=self.SURFACE, cursor="hand2")
        middle.pack(side="left", fill="both", expand=True, pady=6)

        name_label = tk.Label(
            middle,
            text=f"{quote.name}  ·  {quote.capacity} seats",
            bg=self.SURFACE,
            fg=self.TEXT,
            anchor="w",
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
        )
        name_label.pack(fill="x")

        eta_label = tk.Label(
            middle,
            text=f"{quote.eta_min} min away",
            bg=self.SURFACE,
            fg=self.MUTED,
            anchor="w",
            cursor="hand2",
            font=("Helvetica", 8),
        )
        eta_label.pack(fill="x", pady=(3, 0))

        right = tk.Frame(card, bg=self.SURFACE, cursor="hand2")
        right.pack(side="right", padx=11, pady=5)

        price_label = tk.Label(
            right,
            text="—",
            bg=self.SURFACE,
            fg=self.TEXT,
            anchor="e",
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
        )
        price_label.pack(anchor="e")

        selected_label = tk.Label(
            right,
            text="",
            bg=self.SURFACE,
            fg=self.GREEN_DARK,
            anchor="e",
            cursor="hand2",
            font=("Helvetica", 7, "bold"),
        )
        selected_label.pack(anchor="e", pady=(3, 0))

        elements = [
            card,
            icon_canvas,
            middle,
            name_label,
            eta_label,
            right,
            price_label,
            selected_label,
        ]
        for widget in elements:
            widget.bind(
                "<Button-1>",
                lambda _event, vehicle=vehicle_name: self.select_vehicle(vehicle),
            )

        self.vehicle_cards[vehicle_name] = {
            "frame": card,
            "canvas": icon_canvas,
            "middle": middle,
            "right": right,
            "name": name_label,
            "eta": eta_label,
            "price": price_label,
            "selected": selected_label,
        }

        self._style_vehicle_card(
            vehicle_name,
            selected=(vehicle_name == self.selected_vehicle),
        )

    def _build_map_shell(self):
        topbar = tk.Frame(self.map_shell, bg=self.SURFACE, height=54)
        topbar.pack(fill="x", padx=16, pady=(12, 8))
        topbar.pack_propagate(False)

        self.map_status_badge = tk.Label(
            topbar,
            text="● READY",
            bg="#EAF8F0",
            fg=self.GREEN_DARK,
            font=("Helvetica", 9, "bold"),
            padx=10,
            pady=6,
        )
        self.map_status_badge.pack(side="left", pady=7)

        self.map_status_text = tk.Label(
            topbar,
            text="Tap the map to choose where you want to go.",
            bg=self.SURFACE,
            fg=self.TEXT,
            font=("Helvetica", 11, "bold"),
        )
        self.map_status_text.pack(side="left", padx=10, pady=7)

        self.map_info_text = tk.Label(
            topbar,
            text="Nearby drivers updating live",
            bg=self.SURFACE,
            fg=self.MUTED,
            font=("Helvetica", 9),
        )
        self.map_info_text.pack(side="right", pady=7)

        canvas_wrap = tk.Frame(self.map_shell, bg=self.MAP_BG)
        canvas_wrap.pack(fill="both", expand=True, padx=16)

        self.canvas = tk.Canvas(
            canvas_wrap,
            bg=self.MAP_BG,
            highlightthickness=0,
            width=self.MAP_WIDTH,
            height=self.MAP_HEIGHT,
            cursor="crosshair",
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_map_click)

        tripbar = tk.Frame(self.map_shell, bg=self.SURFACE)
        tripbar.pack(fill="x", padx=16, pady=(10, 14))

        self.progress = ttk.Progressbar(
            tripbar,
            orient="horizontal",
            mode="determinate",
            style="Ride.Horizontal.TProgressbar",
        )
        self.progress.pack(fill="x", pady=(0, 8))

        details = tk.Frame(tripbar, bg=self.SURFACE)
        details.pack(fill="x")

        self.driver_detail = tk.Label(
            details,
            text="Driver: not assigned",
            bg=self.SURFACE,
            fg=self.MUTED,
            font=("Helvetica", 9),
        )
        self.driver_detail.pack(side="left")

        self.trip_detail = tk.Label(
            details,
            text="Trip not started",
            bg=self.SURFACE,
            fg=self.MUTED,
            font=("Helvetica", 9),
        )
        self.trip_detail.pack(side="right")

    # ------------------------------------------------------------------
    # Map drawing
    # ------------------------------------------------------------------

    def _draw_map(self):
        c = self.canvas
        c.delete("all")

        # City blocks
        blocks = [
            (30, 25, 190, 110, "#DCE8D8"),
            (270, 30, 425, 90, "#E8DFD2"),
            (535, 28, 750, 87, "#E7E2D5"),
            (785, 35, 940, 105, "#DDE9D9"),
            (30, 235, 180, 405, "#E6DFEA"),
            (705, 365, 940, 570, "#E7DED3"),
            (260, 465, 445, 600, "#E2E8DE"),
        ]
        for x1, y1, x2, y2, color in blocks:
            c.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Water
        c.create_polygon(
            0, 570, 120, 540, 250, 575, 390, 550, 560, 588,
            720, 555, 980, 580, 980, 650, 0, 650,
            fill=self.WATER,
            outline="",
        )
        c.create_text(760, 610, text="Buriganga River", fill="#5A89A7", font=("Helvetica", 10, "italic"))

        # Roads
        for start, end in self.ROAD_SEGMENTS:
            self._draw_road(start, end)

        # Park
        c.create_oval(485, 245, 585, 345, fill=self.PARK, outline="")
        c.create_text(535, 295, text="CITY\nPARK", fill="#4D7A49", font=("Helvetica", 9, "bold"), justify="center")

        # Landmark blocks
        c.create_rectangle(90, 475, 185, 530, fill="#D8C8A8", outline="")
        c.create_text(137, 502, text="Museum", fill="#67583E", font=("Helvetica", 9, "bold"))

        c.create_rectangle(705, 245, 770, 290, fill="#D9D9E8", outline="")
        c.create_text(738, 267, text="Mall", fill="#57576B", font=("Helvetica", 9, "bold"))

        # Location markers
        for name, (x, y) in self.LOCATIONS.items():
            c.create_oval(x - 5, y - 5, x + 5, y + 5, fill="#66717B", outline="white", width=2)
            c.create_text(x, y + 15, text=name, fill="#4B5563", font=("Helvetica", 8, "bold"))

        self.route_item = None
        self.pickup_pin_items = []
        self.destination_pin_items = []
        self.assigned_driver_items = []

        self._draw_pickup_pin()
        if self.destination_point is not None:
            self._draw_destination_pin()
            self._draw_route_preview()

    def _draw_road(self, start, end):
        x1, y1 = start
        x2, y2 = end
        self.canvas.create_line(x1, y1, x2, y2, fill=self.ROAD_EDGE, width=30, capstyle=tk.ROUND)
        self.canvas.create_line(x1, y1, x2, y2, fill=self.ROAD, width=26, capstyle=tk.ROUND)
        self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2, dash=(11, 11))

    def _draw_pickup_pin(self):
        x, y = self.LOCATIONS[self.pickup_name.get()]
        ring = self.canvas.create_oval(x - 13, y - 13, x + 13, y + 13, fill="white", outline=self.GREEN, width=4)
        dot = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=self.GREEN, outline="")
        label_bg = self.canvas.create_rectangle(x - 31, y - 39, x + 31, y - 20, fill=self.GREEN, outline="")
        label = self.canvas.create_text(x, y - 30, text="PICKUP", fill="white", font=("Helvetica", 8, "bold"))
        self.pickup_pin_items = [ring, dot, label_bg, label]

    def _draw_destination_pin(self):
        x, y = self.destination_point
        stem = self.canvas.create_line(x, y - 4, x, y - 28, fill=self.BLACK, width=3)
        pin = self.canvas.create_oval(x - 10, y - 39, x + 10, y - 19, fill=self.BLACK, outline="white", width=2)
        dot = self.canvas.create_oval(x - 3, y - 32, x + 3, y - 26, fill="white", outline="")
        label_width = min(150, max(72, len(self.destination_label) * 6))
        bg = self.canvas.create_rectangle(
            x - label_width / 2, y + 7, x + label_width / 2, y + 29,
            fill="white", outline=self.BORDER
        )
        label = self.canvas.create_text(
            x, y + 18,
            text=self.destination_label,
            fill=self.TEXT,
            font=("Helvetica", 8, "bold"),
        )
        self.destination_pin_items = [stem, pin, dot, bg, label]

    def _draw_route_preview(self):
        if self.destination_point is None:
            return

        pickup = self.LOCATIONS[self.pickup_name.get()]
        self.route_points = self._build_manhattan_route(pickup, self.destination_point)

        flattened = []
        for point in self.route_points:
            flattened.extend(point)

        self.route_item = self.canvas.create_line(
            *flattened,
            fill=self.BLUE,
            width=5,
            capstyle=tk.ROUND,
            joinstyle=tk.ROUND,
            arrow=tk.LAST,
        )
        self.canvas.tag_lower(self.route_item)

    def _build_manhattan_route(self, start, end):
        sx, sy = start
        ex, ey = end

        if abs(ex - sx) > abs(ey - sy):
            middle_x = (sx + ex) / 2
            return [(sx, sy), (middle_x, sy), (middle_x, ey), (ex, ey)]
        middle_y = (sy + ey) / 2
        return [(sx, sy), (sx, middle_y), (ex, middle_y), (ex, ey)]

    # ------------------------------------------------------------------
    # Vehicle drawing and live motion
    # ------------------------------------------------------------------

    def _draw_car_icon(self, canvas, x, y, color, code, scale=1.0):
        w = 30 * scale
        h = 18 * scale
        canvas.create_rectangle(
            x - w / 2, y - h / 2, x + w / 2, y + h / 2,
            fill=color, outline="white", width=2
        )
        canvas.create_rectangle(
            x - w * 0.24, y - h * 0.38, x + w * 0.24, y + h * 0.38,
            fill="#E5E7EB", outline=""
        )
        canvas.create_oval(x - w * 0.38, y + h * 0.34, x - w * 0.18, y + h * 0.62, fill="#222", outline="")
        canvas.create_oval(x + w * 0.18, y + h * 0.34, x + w * 0.38, y + h * 0.62, fill="#222", outline="")
        canvas.create_text(x, y, text=code, fill="white", font=("Helvetica", max(6, int(7 * scale)), "bold"))

    def _spawn_live_vehicles(self):
        self.live_vehicles.clear()
        vehicle_names = ["UberX", "Bike", "Comfort", "UberX", "XL", "Bike", "UberX", "Comfort"]

        positions = [
            (105, 175), (300, 305), (520, 175), (750, 305),
            (235, 455), (645, 455), (455, 95), (820, 400)
        ]

        for idx, (vehicle_name, position) in enumerate(zip(vehicle_names, positions), start=1):
            quote = self.VEHICLE_QUOTES[vehicle_name]
            x, y = position
            price = self._quote_for_vehicle(vehicle_name)

            body = self.canvas.create_rectangle(
                x - 13, y - 8, x + 13, y + 8,
                fill=quote.color, outline="white", width=2
            )
            windshield = self.canvas.create_rectangle(
                x - 4, y - 5, x + 4, y + 5,
                fill="#E5E7EB", outline=""
            )
            code = self.canvas.create_text(
                x, y, text=quote.code, fill="white",
                font=("Helvetica", 7, "bold")
            )

            bubble = self.canvas.create_rectangle(
                x - 28, y - 35, x + 28, y - 18,
                fill="white", outline=self.BORDER
            )
            bubble_text = self.canvas.create_text(
                x, y - 26,
                text=f"৳{price:,.0f}",
                fill=self.TEXT,
                font=("Helvetica", 8, "bold")
            )

            self.live_vehicles[idx] = {
                "type": vehicle_name,
                "x": x,
                "y": y,
                "dx": random.choice([-1.2, -0.9, 0.9, 1.2]),
                "dy": random.choice([-0.5, 0, 0.5]),
                "items": [body, windshield, code, bubble, bubble_text],
                "price_item": bubble_text,
                "price": price,
            }

    def _start_live_vehicle_loop(self):
        def loop():
            if not self.ride_active:
                for vehicle_id, vehicle in list(self.live_vehicles.items()):
                    self._move_live_vehicle(vehicle_id, vehicle)
            self.live_vehicle_job = self.after(75, loop)

        loop()

    def _move_live_vehicle(self, vehicle_id, vehicle):
        x = vehicle["x"]
        y = vehicle["y"]
        dx = vehicle["dx"]
        dy = vehicle["dy"]

        new_x = x + dx
        new_y = y + dy

        # Keep cars inside useful map space.
        if new_x < 55 or new_x > 925:
            dx *= -1
            new_x = x + dx
        if new_y < 65 or new_y > 535:
            dy *= -1
            new_y = y + dy

        # Slightly random direction changes create more organic motion.
        if random.random() < 0.012:
            dx = random.choice([-1.3, -1.0, 1.0, 1.3])
        if random.random() < 0.008:
            dy = random.choice([-0.45, 0, 0.45])

        delta_x = new_x - x
        delta_y = new_y - y
        for item in vehicle["items"]:
            self.canvas.move(item, delta_x, delta_y)

        vehicle["x"] = new_x
        vehicle["y"] = new_y
        vehicle["dx"] = dx
        vehicle["dy"] = dy

        for item in vehicle["items"]:
            self.canvas.tag_raise(item)

    # ------------------------------------------------------------------
    # Selection and pricing
    # ------------------------------------------------------------------

    def _on_pickup_selected(self, _event=None):
        if self.ride_active:
            return
        self._draw_map()
        self._spawn_live_vehicles()
        self._refresh_quotes()

    def _on_destination_selected(self, _event=None):
        if self.ride_active:
            return
        self._refresh_destination_from_dropdown()

    def _refresh_destination_from_dropdown(self):
        name = self.destination_name.get()
        if name == "Choose on map":
            self.destination_point = None
            self.destination_label = "Choose on map"
        else:
            self.destination_point = self.LOCATIONS[name]
            self.destination_label = name

        self._draw_map()
        self._spawn_live_vehicles()
        self._refresh_quotes()

    def _on_map_click(self, event):
        if self.ride_active:
            return

        x = max(35, min(event.x, self.MAP_WIDTH - 35))
        y = max(45, min(event.y, self.MAP_HEIGHT - 75))

        nearest_name, nearest_distance = self._nearest_location(x, y)
        if nearest_distance <= 45:
            self.destination_label = nearest_name
            self.destination_name.set(nearest_name)
            self.destination_point = self.LOCATIONS[nearest_name]
        else:
            self.destination_label = f"Dropped pin ({int(x)}, {int(y)})"
            self.destination_name.set("Choose on map")
            self.destination_point = (x, y)

        pickup = self.LOCATIONS[self.pickup_name.get()]
        if math.hypot(self.destination_point[0] - pickup[0], self.destination_point[1] - pickup[1]) < 35:
            messagebox.showwarning("Destination too close", "Please choose a destination farther from the pickup point.")
            self.destination_point = None
            self.destination_label = "Choose on map"
            self.destination_name.set("Choose on map")
            self._draw_map()
            self._spawn_live_vehicles()
            self._refresh_quotes()
            return

        self._draw_map()
        self._spawn_live_vehicles()
        self._refresh_quotes()
        self._set_map_status(
            "Destination selected",
            "● DESTINATION SET",
            "#EAF8F0",
            self.GREEN_DARK,
        )

    def _nearest_location(self, x, y):
        best_name = ""
        best_distance = float("inf")
        for name, point in self.LOCATIONS.items():
            distance = math.hypot(point[0] - x, point[1] - y)
            if distance < best_distance:
                best_name = name
                best_distance = distance
        return best_name, best_distance


    def select_vehicle(self, vehicle_name):
        if self.ride_active:
            return

        old_vehicle = self.selected_vehicle
        self.selected_vehicle = vehicle_name

        self._style_vehicle_card(old_vehicle, selected=False)
        self._style_vehicle_card(vehicle_name, selected=True)

        self.selected_ride_label.config(
            text=f"Selected ride: {vehicle_name}"
        )

        self._refresh_quotes()

        if self.destination_point is None:
            status_text = (
                f"{vehicle_name} selected. Now choose a destination."
            )
        else:
            status_text = (
                f"{vehicle_name} selected. Press the Request Ride button to continue."
            )

        self._set_map_status(
            status_text,
            f"● {vehicle_name.upper()} SELECTED",
            "#EAF8F0",
            self.GREEN_DARK,
        )

        # Brief visual feedback makes the next action obvious.
        if self.destination_point is not None:
            self.request_button.config(bg=self.GREEN_DARK)
            self.after(
                260,
                lambda: (
                    self.request_button.config(bg=self.BLACK)
                    if not self.ride_active
                    else None
                ),
            )

    def _style_vehicle_card(self, vehicle_name, selected):
        card_data = self.vehicle_cards.get(vehicle_name)
        if not card_data:
            return

        background = "#F0FDF4" if selected else self.SURFACE
        border = self.GREEN if selected else self.BORDER

        card_data["frame"].config(
            bg=background,
            highlightbackground=border,
            highlightthickness=2 if selected else 1,
        )
        card_data["canvas"].config(bg=background)
        card_data["middle"].config(bg=background)
        card_data["right"].config(bg=background)
        card_data["name"].config(bg=background)
        card_data["eta"].config(bg=background)
        card_data["price"].config(bg=background)
        card_data["selected"].config(
            bg=background,
            text="SELECTED" if selected else "",
        )

    def _distance_for_current_route(self):
        if self.destination_point is None:
            return 0.0

        pickup = self.LOCATIONS[self.pickup_name.get()]
        pixel_distance = math.hypot(
            self.destination_point[0] - pickup[0],
            self.destination_point[1] - pickup[1],
        )
        return max(1.2, pixel_distance / 53.0)

    def _quote_for_vehicle(self, vehicle_name):
        quote = self.VEHICLE_QUOTES[vehicle_name]
        distance = self._distance_for_current_route()

        if distance <= 0:
            distance = 4.5

        booking_fee = 25
        dynamic_demand = 1.0 + random.uniform(-0.025, 0.045)
        total = (quote.base_fare + distance * quote.per_km + booking_fee) * quote.multiplier * dynamic_demand
        return max(70, total)


    def _refresh_quotes(self):
        distance = self._distance_for_current_route()
        self.route_distance_km = distance

        for vehicle_name, quote in self.VEHICLE_QUOTES.items():
            price = self._quote_for_vehicle(vehicle_name)
            eta = max(
                1,
                quote.eta_min + random.choice([-1, 0, 0, 1]),
            )

            card = self.vehicle_cards[vehicle_name]
            card["price"].config(text=f"৳{price:,.0f}")
            card["eta"].config(text=f"{eta} min away")

            if vehicle_name == self.selected_vehicle:
                self.current_fare = price
                self.selected_ride_label.config(
                    text=f"Selected ride: {vehicle_name}  ·  {eta} min away"
                )

        if self.destination_point is None:
            self.summary_route.config(text="Select a destination")
            self.summary_price.config(text="Estimated fare: —")
            self.map_info_text.config(text="Nearby drivers updating live")

            if not self.ride_active:
                self.request_button.config(
                    text="CHOOSE DESTINATION",
                    state="disabled",
                    bg="#9CA3AF",
                )
        else:
            self.summary_route.config(
                text=(
                    f"{self.pickup_name.get()} → "
                    f"{self.destination_label}  ·  {distance:.1f} km"
                )
            )
            self.summary_price.config(
                text=f"Estimated fare: ৳{self.current_fare:,.0f}"
            )

            selected_eta = self.VEHICLE_QUOTES[
                self.selected_vehicle
            ].eta_min
            self.map_info_text.config(
                text=(
                    f"{self.selected_vehicle} available "
                    f"in about {selected_eta} min"
                )
            )

            if not self.ride_active:
                self.request_button.config(
                    text=(
                        f"REQUEST {self.selected_vehicle.upper()}"
                        f"  •  ৳{self.current_fare:,.0f}"
                    ),
                    state="normal",
                    bg=self.BLACK,
                )

        # Update live price bubbles on the map.
        for vehicle in self.live_vehicles.values():
            price = self._quote_for_vehicle(vehicle["type"])
            vehicle["price"] = price
            self.canvas.itemconfig(
                vehicle["price_item"],
                text=f"৳{price:,.0f}",
            )

        if self.quote_job:
            try:
                self.after_cancel(self.quote_job)
            except tk.TclError:
                pass
            self.quote_job = None

        if not self.ride_active:
            self.quote_job = self.after(
                2800,
                self._refresh_quotes,
            )

    # ------------------------------------------------------------------
    # Ride workflow
    # ------------------------------------------------------------------

    def request_ride(self):
        if self.ride_active:
            return

        passenger = self.passenger_name.get().strip()
        if not passenger:
            messagebox.showwarning("Passenger required", "Please enter the passenger name.")
            return

        if self.destination_point is None:
            messagebox.showwarning(
                "Destination required",
                "Choose a destination from the list or click on the map to drop a pin.",
            )
            return

        if self.quote_job:
            try:
                self.after_cancel(self.quote_job)
            except tk.TclError:
                pass
            self.quote_job = None

        self.ride_active = True
        self.trip_completed = False
        self.progress["value"] = 0
        self._set_controls_enabled(False)
        self.request_button.config(text="SEARCHING FOR DRIVER", state="disabled")
        self.header_status.config(text="● MATCHING", bg="#3D3318", fg="#FFD166")

        self._set_map_status(
            f"Finding a nearby {self.selected_vehicle}...",
            "● MATCHING",
            "#FFF6DE",
            "#A76200",
        )
        self.trip_detail.config(text="Matching with a nearby driver")
        self.map_info_text.config(text="Checking driver availability")

        self.after(1000, self._assign_driver)

    def _assign_driver(self):
        if not self.ride_active:
            return

        self.driver_record = random.choice(self.DRIVERS)

        candidates = [
            (vehicle_id, data)
            for vehicle_id, data in self.live_vehicles.items()
            if data["type"] == self.selected_vehicle
        ]
        if not candidates:
            candidates = list(self.live_vehicles.items())

        pickup = self.LOCATIONS[self.pickup_name.get()]
        self.assigned_live_id, chosen_data = min(
            candidates,
            key=lambda item: math.hypot(item[1]["x"] - pickup[0], item[1]["y"] - pickup[1]),
        )
        self.assigned_vehicle = chosen_data

        # Remove all live vehicles and redraw static map before trip animation.
        for data in self.live_vehicles.values():
            for item in data["items"]:
                self.canvas.delete(item)
        self.live_vehicles.clear()

        self.driver_detail.config(
            text=(
                f"{self.driver_record['name']}  ·  ★ {self.driver_record['rating']}  ·  "
                f"{self.driver_record['car']}  ·  {self.driver_record['plate']}"
            )
        )
        self.trip_detail.config(text="Driver is heading to pickup")
        self.request_button.config(text="DRIVER ON THE WAY")

        self._set_map_status(
            f"{self.driver_record['name']} accepted your request.",
            "● DRIVER ASSIGNED",
            "#EAF2FF",
            self.BLUE,
        )
        self.map_info_text.config(text="Pickup ETA: 3 min")

        start = (chosen_data["x"], chosen_data["y"])
        self._create_assigned_driver_marker(start)
        pickup_route = self._build_manhattan_route(start, pickup)
        self._animate_along_route(
            pickup_route,
            total_steps=115,
            progress_start=0,
            progress_end=35,
            on_complete=self._pickup_arrived,
            eta_label="Pickup ETA",
        )

    def _create_assigned_driver_marker(self, point):
        x, y = point
        quote = self.VEHICLE_QUOTES[self.selected_vehicle]

        shadow = self.canvas.create_oval(x - 17, y - 12, x + 17, y + 12, fill="#9CA3AF", outline="")
        body = self.canvas.create_rectangle(
            x - 15, y - 9, x + 15, y + 9,
            fill=quote.color, outline="white", width=2
        )
        windshield = self.canvas.create_rectangle(
            x - 4, y - 6, x + 4, y + 6,
            fill="#E5E7EB", outline=""
        )
        code = self.canvas.create_text(
            x, y, text=quote.code, fill="white",
            font=("Helvetica", 8, "bold")
        )

        self.assigned_driver_items = [shadow, body, windshield, code]

    def _move_assigned_driver(self, point):
        x, y = point
        if not self.assigned_driver_items:
            return

        shadow, body, windshield, code = self.assigned_driver_items
        self.canvas.coords(shadow, x - 17, y - 12, x + 17, y + 12)
        self.canvas.coords(body, x - 15, y - 9, x + 15, y + 9)
        self.canvas.coords(windshield, x - 4, y - 6, x + 4, y + 6)
        self.canvas.coords(code, x, y)

        for item in self.assigned_driver_items:
            self.canvas.tag_raise(item)

    def _animate_along_route(
        self,
        points,
        total_steps,
        progress_start,
        progress_end,
        on_complete,
        eta_label,
    ):
        if len(points) < 2:
            on_complete()
            return

        segment_lengths = []
        total_length = 0.0
        for a, b in zip(points, points[1:]):
            length = math.hypot(b[0] - a[0], b[1] - a[1])
            segment_lengths.append(length)
            total_length += length

        elapsed_step = 0

        def point_at_fraction(fraction):
            target = total_length * fraction
            traveled = 0.0

            for index, segment_length in enumerate(segment_lengths):
                if traveled + segment_length >= target:
                    local = (target - traveled) / max(segment_length, 1)
                    a = points[index]
                    b = points[index + 1]
                    return (
                        a[0] + (b[0] - a[0]) * local,
                        a[1] + (b[1] - a[1]) * local,
                    )
                traveled += segment_length

            return points[-1]

        def step():
            nonlocal elapsed_step
            if not self.ride_active:
                return

            elapsed_step += 1
            fraction = min(1.0, elapsed_step / total_steps)
            eased = 3 * fraction * fraction - 2 * fraction * fraction * fraction
            point = point_at_fraction(eased)
            self._move_assigned_driver(point)

            progress = progress_start + (progress_end - progress_start) * fraction
            self.progress["value"] = progress

            eta = max(0, math.ceil((1 - fraction) * 4))
            self.map_info_text.config(text=f"{eta_label}: {eta} min")

            if elapsed_step < total_steps:
                self.animation_job = self.after(28, step)
            else:
                on_complete()

        step()

    def _pickup_arrived(self):
        if not self.ride_active:
            return

        self.progress["value"] = 35
        self.trip_detail.config(text="Driver has reached the passenger")
        self.request_button.config(text="DRIVER HAS ARRIVED")
        self._set_map_status(
            f"{self.driver_record['name']} is waiting at {self.pickup_name.get()}.",
            "● PICKUP",
            "#EAF8F0",
            self.GREEN_DARK,
        )
        self.map_info_text.config(text="Passenger boarding")
        self.after(1600, self._begin_trip)

    def _begin_trip(self):
        if not self.ride_active:
            return

        pickup = self.LOCATIONS[self.pickup_name.get()]
        destination = self.destination_point
        route = self._build_manhattan_route(pickup, destination)

        self.trip_detail.config(text=f"On trip to {self.destination_label}")
        self.request_button.config(text="ON TRIP")
        self._set_map_status(
            f"Trip started toward {self.destination_label}.",
            "● ON TRIP",
            "#EAF8F0",
            self.GREEN_DARK,
        )
        self.header_status.config(text="● ON TRIP", bg="#183C2A", fg="#45E991")

        # Redraw route in green.
        if self.route_item:
            self.canvas.itemconfig(self.route_item, fill=self.GREEN, width=6)

        trip_steps = int(max(150, min(230, self.route_distance_km * 27)))
        self._animate_along_route(
            route,
            total_steps=trip_steps,
            progress_start=35,
            progress_end=100,
            on_complete=self._finish_trip,
            eta_label="Destination ETA",
        )

    def _finish_trip(self):
        self.ride_active = False
        self.trip_completed = True
        self.progress["value"] = 100

        final_fare = self.current_fare * random.uniform(0.98, 1.04)
        self.current_fare = final_fare

        self._set_map_status(
            f"You arrived at {self.destination_label}.",
            "● COMPLETED",
            "#EAF8F0",
            self.GREEN_DARK,
        )
        self.header_status.config(text="● COMPLETED", bg="#183C2A", fg="#45E991")
        self.map_info_text.config(text="Ride completed")
        self.trip_detail.config(text=f"Paid ৳{final_fare:,.0f} via {self.payment_method.get()}")
        self.request_button.config(text="RIDE COMPLETED", state="disabled")

        messagebox.showinfo(
            "Ride completed",
            (
                f"Passenger: {self.passenger_name.get().strip()}\n"
                f"Driver: {self.driver_record['name']}\n"
                f"Vehicle: {self.selected_vehicle}\n"
                f"Route: {self.pickup_name.get()} → {self.destination_label}\n"
                f"Distance: {self.route_distance_km:.1f} km\n"
                f"Final fare: ৳{final_fare:,.0f}\n"
                f"Payment: {self.payment_method.get()}\n\n"
                "Thank you for riding."
            ),
        )

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------

    def _set_controls_enabled(self, enabled):
        entry_state = "normal" if enabled else "disabled"
        combo_state = "readonly" if enabled else "disabled"

        self.passenger_entry.config(state=entry_state)
        self.pickup_combo.config(state=combo_state)
        self.destination_combo.config(state=combo_state)
        self.payment_combo.config(state=combo_state)

    def _set_map_status(self, text, badge_text, badge_bg, badge_fg):
        self.map_status_text.config(text=text)
        self.map_status_badge.config(
            text=badge_text,
            bg=badge_bg,
            fg=badge_fg,
        )

    def reset_simulation(self):
        if self.animation_job:
            try:
                self.after_cancel(self.animation_job)
            except tk.TclError:
                pass
            self.animation_job = None

        self.ride_active = False
        self.trip_completed = False
        self.driver_record = None
        self.assigned_vehicle = None
        self.assigned_live_id = None
        self.assigned_driver_items = []
        self.progress["value"] = 0

        self._set_controls_enabled(True)
        self.header_status.config(text="● ONLINE", bg="#183C2A", fg="#45E991")
        self.driver_detail.config(text="Driver: not assigned")
        self.trip_detail.config(text="Trip not started")
        self._set_map_status(
            "Tap the map to choose where you want to go.",
            "● READY",
            "#EAF8F0",
            self.GREEN_DARK,
        )

        self._draw_map()
        self._spawn_live_vehicles()
        self._refresh_quotes()

    def _on_close(self):
        for job in (self.animation_job, self.live_vehicle_job, self.quote_job):
            if job:
                try:
                    self.after_cancel(job)
                except tk.TclError:
                    pass
        self.destroy()


if __name__ == "__main__":
    app = UberLiveSimulation()
    app.mainloop()
