#!/usr/bin/env python3
"""
Uber Ride Simulator - A full ride-hailing experience with interactive map,
vehicle selection, fare estimation, and real-time animations.
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import math
import time

# ═══════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════

class Theme:
    # Polished dark palette with strong contrast on macOS, Windows and Linux.
    BG = "#090A0F"
    SURFACE = "#11131A"
    SURFACE2 = "#181B24"
    CARD = "#151821"
    CARD_HOVER = "#1D2230"
    PRIMARY = "#276EF1"
    PRIMARY_LIGHT = "#4D8BFF"
    SECONDARY = "#EF476F"
    SUCCESS = "#12B76A"
    WARNING = "#F5B942"
    TEXT = "#F8FAFC"
    TEXT_SEC = "#B7C0D0"
    TEXT_MUTED = "#758096"
    BORDER = "#293043"
    SHADOW = "#05060A"

    # Map colours
    MAP_BG = "#111925"
    MAP_STREET = "#273345"
    MAP_STREET_LINE = "#58677B"
    MAP_BUILDING_1 = "#243244"
    MAP_BUILDING_2 = "#2E3D50"
    MAP_BUILDING_3 = "#374A60"
    MAP_PARK = "#24543A"
    MAP_PARK_TREE = "#3A8A5D"
    MAP_WATER = "#163A5F"
    PICKUP_COLOR = "#12B76A"
    DEST_COLOR = "#EF476F"
    CAR_COLOR = "#276EF1"

    FONT_FAMILY = "Helvetica"


# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

VEHICLES = [
    {
        "id": "uberx",
        "name": "UberX",
        "icon": "🚗",
        "desc": "Affordable rides for 1-4",
        "capacity": 4,
        "base_fare": 5.00,
        "per_km": 1.50,
        "per_min": 0.25,
        "color": "#276EF1",
        "eta": "2 min",
    },
    {
        "id": "uberxl",
        "name": "UberXL",
        "icon": "🚙",
        "desc": "Spacious rides for 1-6",
        "capacity": 6,
        "base_fare": 8.00,
        "per_km": 2.00,
        "per_min": 0.30,
        "color": "#6C5CE7",
        "eta": "4 min",
    },
    {
        "id": "uberblack",
        "name": "Uber Black",
        "icon": "🏎️",
        "desc": "Premium luxury rides",
        "capacity": 4,
        "base_fare": 15.00,
        "per_km": 3.50,
        "per_min": 0.50,
        "color": "#3B4148",
        "eta": "6 min",
    },
    {
        "id": "uberpool",
        "name": "Uber Pool",
        "icon": "🚐",
        "desc": "Shared rides, lower fare",
        "capacity": 3,
        "base_fare": 3.00,
        "per_km": 1.00,
        "per_min": 0.15,
        "color": "#00B894",
        "eta": "3 min",
    },
]

DRIVERS = [
    {"name": "Marcus J.", "car": "Toyota Camry", "plate": "ABC-1234",
     "color": "#E0E0E0", "rating": 4.9, "trips": 1250},
    {"name": "Sarah L.", "car": "Honda Accord", "plate": "XYZ-5678",
     "color": "#2C3E50", "rating": 4.8, "trips": 980},
    {"name": "David K.", "car": "Tesla Model 3", "plate": "EV-2024",
     "color": "#E74C3C", "rating": 4.95, "trips": 2100},
    {"name": "Emily R.", "car": "Toyota Prius", "plate": "ECO-789",
     "color": "#3498DB", "rating": 4.85, "trips": 1560},
    {"name": "James W.", "car": "Ford Explorer", "plate": "XLR-8901",
     "color": "#F39C12", "rating": 4.92, "trips": 1820},
]

DESTINATIONS = [
    "Central Park", "Downtown", "Airport", "Shopping Mall",
    "Harbor View", "Tech Hub", "Grand Station", "Riverside",
    "University", "Stadium"
]

PICKUP_SPOTS = [
    "Current Location", "Home", "Office", "Gym",
    "Coffee Shop", "Library", "Hotel", "Restaurant"
]

# Map city layout
CITY_BLOCKS = [
    # (x, y, w, h, colour, label=None)
    # Parks
    (220, 70, 100, 80, Theme.MAP_PARK, "Central Park"),
    (440, 310, 80, 70, Theme.MAP_PARK, None),
    (80, 340, 70, 60, Theme.MAP_PARK, None),
    # Water
    (540, 70, 120, 90, Theme.MAP_WATER, "Lakeview"),
    # Buildings
    (20, 20, 80, 60, Theme.MAP_BUILDING_1, None),
    (110, 20, 80, 60, Theme.MAP_BUILDING_2, None),
    (330, 20, 80, 60, Theme.MAP_BUILDING_1, None),
    (420, 20, 80, 60, Theme.MAP_BUILDING_3, None),
    (20, 110, 80, 60, Theme.MAP_BUILDING_2, None),
    (110, 110, 80, 60, Theme.MAP_BUILDING_3, None),
    (330, 110, 80, 80, Theme.MAP_BUILDING_1, None),
    (420, 110, 80, 80, Theme.MAP_BUILDING_2, None),
    (670, 20, 70, 60, Theme.MAP_BUILDING_1, None),
    (670, 100, 70, 70, Theme.MAP_BUILDING_2, None),
    (20, 210, 80, 60, Theme.MAP_BUILDING_3, None),
    (110, 210, 80, 60, Theme.MAP_BG, "Parking"),
    (220, 210, 100, 60, Theme.MAP_BUILDING_2, None),
    (330, 210, 80, 60, Theme.MAP_BUILDING_1, None),
    (420, 210, 80, 60, Theme.MAP_BUILDING_3, None),
    (540, 210, 80, 60, Theme.MAP_BUILDING_2, None),
    (670, 210, 70, 60, Theme.MAP_BUILDING_1, None),
    (20, 310, 80, 60, Theme.MAP_BUILDING_1, None),
    (220, 310, 80, 80, Theme.MAP_BUILDING_3, None),
    (330, 310, 80, 80, Theme.MAP_BUILDING_1, None),
    (540, 310, 80, 70, Theme.MAP_BUILDING_2, None),
    (670, 310, 70, 70, Theme.MAP_BUILDING_3, None),
    (20, 400, 80, 60, Theme.MAP_BUILDING_2, None),
    (110, 400, 80, 60, Theme.MAP_BUILDING_1, None),
    (220, 400, 100, 60, Theme.MAP_BUILDING_2, None),
    (330, 400, 80, 60, Theme.MAP_BUILDING_3, None),
    (420, 400, 80, 60, Theme.MAP_BUILDING_1, None),
    (540, 400, 80, 60, Theme.MAP_BUILDING_2, None),
    (670, 400, 70, 60, Theme.MAP_BUILDING_1, None),
]

# Connections between map key points for car path
# (x1, y1, x2, y2)
MAP_ROADS_H = [
    (50, 100, 720, 100),
    (50, 190, 720, 190),
    (80, 290, 720, 290),
    (50, 380, 720, 380),
    (50, 460, 720, 460),
]
MAP_ROADS_V = [
    (80, 40, 80, 480),
    (180, 40, 180, 480),
    (290, 40, 290, 480),
    (400, 40, 400, 480),
    (510, 40, 510, 480),
    (620, 40, 620, 480),
]

# Location keypoints (for pickup/dropoff)
LOCATION_POINTS = {
    "Current Location": (180, 100),
    "Home": (80, 380),
    "Office": (400, 100),
    "Central Park": (250, 100),
    "Downtown": (510, 190),
    "Airport": (620, 380),
    "Shopping Mall": (290, 380),
    "Harbor View": (620, 100),
    "Tech Hub": (400, 290),
    "Grand Station": (80, 190),
    "Riverside": (180, 290),
    "University": (80, 100),
    "Stadium": (510, 460),
    "Gym": (290, 190),
    "Coffee Shop": (180, 190),
    "Library": (510, 100),
    "Hotel": (400, 460),
    "Restaurant": (290, 460),
}

# ═══════════════════════════════════════════════════════════════
# UTILITY HELPERS
# ═══════════════════════════════════════════════════════════════

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = ''.join([c * 2 for c in h])
    if len(h) != 6:
        raise ValueError(f"Invalid hex color: #{h}")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return rgb_to_hex(r, g, b)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calc_fare(vehicle, dist_km, time_min):
    return vehicle["base_fare"] + vehicle["per_km"] * dist_km + vehicle["per_min"] * time_min


class ModernButton(tk.Canvas):
    """A reliable rounded button that keeps its colours on every OS.

    Tk's native Button widget can be rendered by the operating system and may
    ignore custom background colours, especially on macOS.  This canvas-based
    button avoids that problem while supporting hover, click and keyboard use.
    """

    def __init__(self, parent, text, command, width, height, bg, fg, font,
                 hover_bg=None, radius=12, border_color=None, border_width=1,
                 **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent.cget("bg"),
                         highlightthickness=0, bd=0, cursor="hand2",
                         takefocus=1, **kwargs)
        self._text = text
        self._command = command
        self._width = int(width)
        self._height = int(height)
        self._bg = bg
        self._hover_bg = hover_bg or lerp_color(bg, "#FFFFFF", 0.14)
        self._pressed_bg = lerp_color(bg, "#000000", 0.12)
        self._fg = fg
        self._font = font
        self._radius = min(radius, self._height // 2)
        self._border_color = border_color or lerp_color(bg, "#FFFFFF", 0.16)
        self._border_width = border_width
        self._enabled = True

        self.bind("<Enter>", lambda _e: self._draw(self._hover_bg))
        self.bind("<Leave>", lambda _e: self._draw(self._bg))
        self.bind("<ButtonPress-1>", lambda _e: self._draw(self._pressed_bg))
        self.bind("<ButtonRelease-1>", self._release)
        self.bind("<Return>", lambda _e: self.invoke())
        self.bind("<space>", lambda _e: self.invoke())
        self.bind("<FocusIn>", lambda _e: self._draw(self._hover_bg, focused=True))
        self.bind("<FocusOut>", lambda _e: self._draw(self._bg))
        self._draw(self._bg)

    def _rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, splinesteps=24, **kwargs)

    def _draw(self, fill, focused=False):
        self.delete("all")
        inset = 2
        outline = Theme.TEXT if focused else self._border_color
        self._rounded_rect(
            inset, inset, self._width - inset, self._height - inset,
            self._radius, fill=fill, outline=outline,
            width=2 if focused else self._border_width
        )
        self.create_text(
            self._width / 2, self._height / 2, text=self._text,
            fill=self._fg, font=self._font, anchor="center"
        )

    def _release(self, event):
        inside = 0 <= event.x <= self._width and 0 <= event.y <= self._height
        self._draw(self._hover_bg if inside else self._bg)
        if inside:
            self.invoke()

    def invoke(self):
        if self._enabled and callable(self._command):
            self.focus_set()
            self.after(1, self._command)


# ═══════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

class UberRideSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Uber Ride Simulator")
        self.root.configure(bg=Theme.BG)
        self.root.resizable(False, False)

        # Window size
        self.WIN_W = 920
        self.WIN_H = 680
        self.root.geometry(f"{self.WIN_W}x{self.WIN_H}")

        # Centre the window
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - self.WIN_W) // 2
        y = (sh - self.WIN_H) // 2
        self.root.geometry(f"+{x}+{y}")

        # State
        self.pickup = "Current Location"
        self.destination = "Central Park"
        self.selected_vehicle = None
        self.driver = None
        self.fare = 0
        self.trip_distance = 5.0  # km
        self.trip_time = 12  # minutes
        self.rating = 0
        self.trip_phase = "welcome"

        # Fonts
        self._setup_fonts()

        # Build UI
        self._build_ui()

        # Show welcome by default
        self.show_welcome()

    # ── Font setup ──────────────────────────────────────────

    def _setup_fonts(self):
        self.font_logo = tkfont.Font(family=Theme.FONT_FAMILY, size=25, weight="bold")
        self.font_hero_logo = tkfont.Font(family=Theme.FONT_FAMILY, size=42, weight="bold")
        self.font_title = tkfont.Font(family=Theme.FONT_FAMILY, size=22, weight="bold")
        self.font_subtitle = tkfont.Font(family=Theme.FONT_FAMILY, size=14)
        self.font_body = tkfont.Font(family=Theme.FONT_FAMILY, size=12)
        self.font_small = tkfont.Font(family=Theme.FONT_FAMILY, size=10)
        self.font_btn = tkfont.Font(family=Theme.FONT_FAMILY, size=13, weight="bold")
        self.font_vehicle_name = tkfont.Font(family=Theme.FONT_FAMILY, size=15, weight="bold")
        self.font_price = tkfont.Font(family=Theme.FONT_FAMILY, size=18, weight="bold")
        self.font_icon = tkfont.Font(family=Theme.FONT_FAMILY, size=28)

    # ── Root UI Structure ──────────────────────────────────

    def _build_ui(self):
        # Top bar
        self.top_bar = tk.Frame(self.root, bg=Theme.SURFACE, height=56)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        brand_wrap = tk.Frame(self.top_bar, bg=Theme.SURFACE)
        brand_wrap.pack(side="left", padx=22)
        tk.Label(brand_wrap, text="UBER", font=self.font_logo,
                 fg=Theme.TEXT, bg=Theme.SURFACE).pack(side="left")
        tk.Frame(brand_wrap, width=3, height=24, bg=Theme.PRIMARY).pack(
            side="left", padx=(12, 0)
        )

        self.phase_label = tk.Label(self.top_bar, text="",
                                    font=self.font_subtitle, fg=Theme.TEXT_SEC, bg=Theme.SURFACE)
        self.phase_label.pack(side="right", padx=24)

        # Main content
        self.content = tk.Frame(self.root, bg=Theme.BG)
        self.content.pack(fill="both", expand=True)

        # Bottom status bar
        self.status_bar = tk.Frame(self.root, bg=Theme.SURFACE, height=36)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)

        self.status_label = tk.Label(self.status_bar, text="Ready",
                                     font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.SURFACE)
        self.status_label.pack(side="left", padx=16)

        # Safety message
        tk.Label(self.status_bar, text="🔒 Safety Check • 24/7 Support",
                 font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.SURFACE).pack(side="right", padx=16)

    # ── Screen management ──────────────────────────────────

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def set_status(self, msg):
        self.status_label.config(text=msg)

    def set_phase(self, msg):
        self.phase_label.config(text=msg)

    # ── Button factory ─────────────────────────────────────

    def _make_btn(self, parent, text, command, bg=Theme.PRIMARY, fg=Theme.TEXT,
                  width=None, height=None, font=None, padx=28, pady=12, **kw):
        button_font = font or self.font_btn
        # Width/height are pixels here, making the result consistent on all OSes.
        measured_w = button_font.measure(text) + (padx * 2)
        measured_h = button_font.metrics("linespace") + (pady * 2)
        width_px = int(width) if width else max(190, measured_w)
        height_px = int(height) if height else max(48, measured_h)

        return ModernButton(
            parent, text=text, command=command, width=width_px, height=height_px,
            bg=bg, fg=fg, font=button_font,
            hover_bg=lerp_color(bg, "#FFFFFF", 0.14),
            border_color=lerp_color(bg, "#FFFFFF", 0.18),
            **kw
        )

    def _make_card(self, parent, bg=Theme.CARD, **kw):
        frame = tk.Frame(parent, bg=bg, **kw)
        frame.config(highlightbackground=Theme.BORDER, highlightthickness=1,
                     highlightcolor=Theme.BORDER)
        return frame

    # ═══════════════════════════════════════════════════════════
    # SCREEN: WELCOME
    # ═══════════════════════════════════════════════════════════

    def show_welcome(self):
        self.trip_phase = "welcome"
        self.selected_vehicle = None
        self.driver = None
        self.fare = 0
        self.rating = 0
        self.set_phase("")
        self.set_status("Welcome to Uber Ride Simulator")
        self._clear_content()

        # Centred container
        container = tk.Frame(self.content, bg=Theme.BG)
        container.place(relx=0.5, rely=0.45, anchor="center")

        # Logo area
        logo_frame = tk.Frame(container, bg=Theme.BG)
        logo_frame.pack(pady=(0, 10))

        # Uber logo mark
        logo_box = tk.Frame(logo_frame, bg=Theme.BG)
        logo_box.pack()

        # The word "UBER" in thick letters
        for ch in "UBER":
            lbl = tk.Label(logo_box, text=ch, font=self.font_hero_logo,
                           fg=Theme.TEXT, bg=Theme.BG)
            lbl.pack(side="left")

        # Subtle accent line
        accent_line = tk.Frame(container, bg=Theme.PRIMARY, height=3, width=120)
        accent_line.pack(pady=(0, 16))
        accent_line.pack_propagate(False)

        # Tagline
        tk.Label(container, text="Your ride, your way. ✦",
                 font=self.font_subtitle, fg=Theme.TEXT_SEC, bg=Theme.BG).pack(pady=(0, 8))
        tk.Label(container, text="Experience the full Uber journey — from booking to destination",
                 font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.BG).pack(pady=(0, 40))

        # Main CTA
        btn = self._make_btn(container, "Set a destination", self.show_booking,
                             padx=48, pady=16, bg=Theme.PRIMARY)
        btn.pack(pady=(0, 20))

        # Quick tips
        tip_frame = tk.Frame(container, bg=Theme.BG)
        tip_frame.pack(pady=10)

        tips = ["📍 Choose pickup & destination", "🚗 Pick your ride",
                "💰 See fare estimates", "🎯 Watch the live simulation"]
        for i, tip in enumerate(tips):
            tk.Label(tip_frame, text=tip, font=self.font_small,
                     fg=Theme.TEXT_MUTED, bg=Theme.BG).pack(side="left", padx=16)

        self.set_status("Ready to ride. Click 'Set a destination' to begin.")

    # ═══════════════════════════════════════════════════════════
    # SCREEN: BOOKING (destination + vehicle selection)
    # ═══════════════════════════════════════════════════════════

    def show_booking(self):
        self.trip_phase = "booking"
        self.set_phase("Where to?")
        self.set_status("Select your pickup and destination")
        self._clear_content()

        # Split layout
        left = tk.Frame(self.content, bg=Theme.BG, width=300)
        left.pack(side="left", fill="y", padx=(20, 10), pady=20)
        left.pack_propagate(False)

        right = tk.Frame(self.content, bg=Theme.SURFACE, width=580)
        right.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=20)
        right.pack_propagate(False)

        # ── LEFT: Destination inputs ──
        step1 = tk.Frame(left, bg=Theme.BG)
        step1.pack(fill="x", pady=(0, 16))
        tk.Label(step1, text="📍 Where are you going?",
                 font=self.font_subtitle, fg=Theme.TEXT, bg=Theme.BG).pack(anchor="w")

        # Pickup
        pickup_frame = self._make_card(left, bg=Theme.CARD)
        pickup_frame.pack(fill="x", pady=(16, 4))
        tk.Label(pickup_frame, text="PICKUP", font=self.font_small,
                 fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack(anchor="w", padx=14, pady=(10, 2))
        self.pickup_var = tk.StringVar(value=self.pickup)
        pickup_menu = tk.OptionMenu(pickup_frame, self.pickup_var, *PICKUP_SPOTS)
        pickup_menu.config(bg=Theme.CARD, fg=Theme.TEXT, font=self.font_body,
                           relief="flat", bd=0, activebackground=Theme.CARD_HOVER,
                           activeforeground=Theme.TEXT, highlightthickness=0)
        pickup_menu["menu"].config(bg=Theme.SURFACE2, fg=Theme.TEXT,
                                    font=self.font_body, bd=0)
        pickup_menu.pack(fill="x", padx=14, pady=(0, 10))

        # Connector dots
        conn = tk.Frame(left, bg=Theme.BG, height=24)
        conn.pack(fill="x")
        tk.Label(conn, text="  ↓", font=self.font_body,
                 fg=Theme.TEXT_MUTED, bg=Theme.BG).pack()

        # Destination
        dest_frame = self._make_card(left, bg=Theme.CARD)
        dest_frame.pack(fill="x", pady=(4, 16))
        tk.Label(dest_frame, text="DESTINATION", font=self.font_small,
                 fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack(anchor="w", padx=14, pady=(10, 2))
        self.dest_var = tk.StringVar(value=self.destination)
        dest_menu = tk.OptionMenu(dest_frame, self.dest_var, *DESTINATIONS)
        dest_menu.config(bg=Theme.CARD, fg=Theme.TEXT, font=self.font_body,
                         relief="flat", bd=0, activebackground=Theme.CARD_HOVER,
                         activeforeground=Theme.TEXT, highlightthickness=0)
        dest_menu["menu"].config(bg=Theme.SURFACE2, fg=Theme.TEXT,
                                  font=self.font_body, bd=0)
        dest_menu.pack(fill="x", padx=14, pady=(0, 10))

        # Confirm button
        confirm_btn = self._make_btn(
            left, "✓ Confirm locations", self._on_locations_confirmed,
            bg=Theme.SUCCESS, padx=20, pady=12)
        confirm_btn.pack(pady=(8, 0))

        # Mini info
        info_lbl = tk.Label(left, text="", font=self.font_small,
                            fg=Theme.TEXT_MUTED, bg=Theme.BG)
        info_lbl.pack(pady=(16, 0))
        self._booking_info = info_lbl

        # ── RIGHT: Map ──
        self.booking_map = RideMap(right, width=560, height=470, bg=Theme.SURFACE)
        self.booking_map.pack(padx=10, pady=10)

        # Draw locations on map
        pickup_pt = LOCATION_POINTS.get(self.pickup_var.get(), (180, 190))
        dest_pt = LOCATION_POINTS.get(self.dest_var.get(), (400, 290))
        self.booking_map.set_points(pickup_pt, dest_pt)
        self.booking_map.draw_city()

        # Update map when selections change
        self.pickup_var.trace_add("write", lambda *a: self._update_booking_map())
        self.dest_var.trace_add("write", lambda *a: self._update_booking_map())

    def _update_booking_map(self):
        if hasattr(self, 'booking_map') and self.booking_map.winfo_exists():
            pickup_pt = LOCATION_POINTS.get(self.pickup_var.get(), (180, 190))
            dest_pt = LOCATION_POINTS.get(self.dest_var.get(), (400, 290))
            self.booking_map.set_points(pickup_pt, dest_pt)
            self.booking_map.draw_city()

    def _on_locations_confirmed(self):
        self.pickup = self.pickup_var.get()
        self.destination = self.dest_var.get()

        # Calculate simulated distance and time
        p1 = LOCATION_POINTS.get(self.pickup, (100, 100))
        p2 = LOCATION_POINTS.get(self.destination, (500, 300))
        pixel_dist = distance(p1, p2)
        self.trip_distance = round(pixel_dist / 35 + random.uniform(0.5, 2.0), 1)
        self.trip_time = round(self.trip_distance / 0.4 + random.uniform(1, 4), 0)

        self.set_status(f"{self.pickup} → {self.destination} · ~{self.trip_distance} km")
        self.show_vehicle_selection()

    # ═══════════════════════════════════════════════════════════
    # SCREEN: VEHICLE SELECTION
    # ═══════════════════════════════════════════════════════════

    def show_vehicle_selection(self):
        self.trip_phase = "vehicle"
        self.set_phase("Choose a ride")
        self.set_status(f"{self.pickup} → {self.destination} · {self.trip_distance} km")
        self._clear_content()

        # Header
        header = tk.Frame(self.content, bg=Theme.BG)
        header.pack(fill="x", padx=24, pady=(20, 4))
        tk.Label(header, text="Choose a ride type",
                 font=self.font_title, fg=Theme.TEXT, bg=Theme.BG).pack(anchor="w")
        tk.Label(header, text=f"From: {self.pickup}  →  To: {self.destination}",
                 font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.BG).pack(anchor="w")

        # Route info mini
        info_bar = tk.Frame(self.content, bg=Theme.SURFACE)
        info_bar.pack(fill="x", padx=24, pady=8)
        info_bar.config(highlightbackground=Theme.BORDER, highlightthickness=1)
        items = [
            f"📍 {self.pickup}",
            f"🎯 {self.destination}",
            f"📏 {self.trip_distance} km",
            f"⏱️ ~{int(self.trip_time)} min",
        ]
        for item in items:
            tk.Label(info_bar, text=item, font=self.font_small,
                     fg=Theme.TEXT_SEC, bg=Theme.SURFACE).pack(side="left", padx=18, pady=10)

        # Vehicle cards container
        cards_container = tk.Frame(self.content, bg=Theme.BG)
        cards_container.pack(fill="both", expand=True, padx=24, pady=16)

        # Grid of 2x2 for vehicle cards
        for i, vehicle in enumerate(VEHICLES):
            row = i // 2
            col = i % 2
            card = self._create_vehicle_card(cards_container, vehicle)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            cards_container.grid_rowconfigure(row, weight=1)
            cards_container.grid_columnconfigure(col, weight=1)

    def _create_vehicle_card(self, parent, vehicle):
        """Create a single vehicle selection card."""
        fare = calc_fare(vehicle, self.trip_distance, self.trip_time)

        card = tk.Frame(parent, bg=Theme.CARD)
        card.config(highlightbackground=Theme.BORDER, highlightthickness=1)
        card.pack_propagate(False)

        # Row 1: Icon + Name + Price
        row1 = tk.Frame(card, bg=Theme.CARD)
        row1.pack(fill="x", padx=20, pady=(18, 4))

        # Vehicle colour indicator
        color_dot = tk.Frame(row1, bg=vehicle["color"], width=10, height=10)
        color_dot.pack(side="left", padx=(0, 10))
        color_dot.pack_propagate(False)

        tk.Label(row1, text=f"{vehicle['icon']}  {vehicle['name']}",
                 font=self.font_vehicle_name, fg=Theme.TEXT, bg=Theme.CARD).pack(side="left")

        tk.Label(row1, text=f"${fare:.2f}",
                 font=self.font_price, fg=Theme.TEXT, bg=Theme.CARD).pack(side="right")

        # Row 2: Description
        row2 = tk.Frame(card, bg=Theme.CARD)
        row2.pack(fill="x", padx=20, pady=(2, 4))
        tk.Label(row2, text=vehicle["desc"],
                 font=self.font_small, fg=Theme.TEXT_SEC, bg=Theme.CARD).pack(anchor="w")

        # Row 3: Details
        row3 = tk.Frame(card, bg=Theme.CARD)
        row3.pack(fill="x", padx=20, pady=(4, 12))
        details = f"👤 {vehicle['capacity']} seats  ·  ⏱ {vehicle['eta']} away  ·  ${vehicle['base_fare']:.2f} base"
        tk.Label(row3, text=details,
                 font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack(anchor="w")

        # Row 4: Fare breakdown
        row4 = tk.Frame(card, bg=Theme.CARD)
        row4.pack(fill="x", padx=20, pady=(0, 12))
        breakdown = f"${vehicle['base_fare']:.2f} + ${vehicle['per_km']:.2f}/km × {self.trip_distance}km + ${vehicle['per_min']:.2f}/min × {int(self.trip_time)}min"
        tk.Label(row4, text=breakdown,
                 font=("Helvetica", 8), fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack(anchor="w")

        # Select button
        select_btn = self._make_btn(
            card, f"Select {vehicle['name']}",
            lambda v=vehicle, f=fare: self._on_vehicle_selected(v, f),
            bg=vehicle["color"], padx=20, pady=10)
        select_btn.pack(pady=(4, 14))

        # Hover effect for card
        def on_enter(e):
            card.config(highlightbackground=vehicle["color"])
        def on_leave(e):
            card.config(highlightbackground=Theme.BORDER)
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        return card

    def _on_vehicle_selected(self, vehicle, fare):
        self.selected_vehicle = vehicle
        self.fare = fare
        self.driver = random.choice(DRIVERS)
        self.set_status(f"{vehicle['name']} selected · ${fare:.2f} · Driver: {self.driver['name']}")
        self.show_driver_matching()

    # ═══════════════════════════════════════════════════════════
    # SCREEN: DRIVER MATCHING
    # ═══════════════════════════════════════════════════════════

    def show_driver_matching(self):
        self.trip_phase = "matching"
        self.set_phase("Finding your driver...")
        self.set_status("Searching for nearby drivers...")
        self._clear_content()

        container = tk.Frame(self.content, bg=Theme.BG)
        container.place(relx=0.5, rely=0.4, anchor="center")

        # Searching animation (dots)
        self.search_frame = tk.Frame(container, bg=Theme.BG)
        self.search_frame.pack(pady=20)

        tk.Label(self.search_frame, text="Finding your driver",
                 font=self.font_title, fg=Theme.TEXT, bg=Theme.BG).pack()

        self.search_dots = tk.Label(self.search_frame, text="",
                                    font=self.font_title, fg=Theme.PRIMARY_LIGHT, bg=Theme.BG)
        self.search_dots.pack()

        # Spinner
        spinner_canvas = tk.Canvas(self.search_frame, width=80, height=80,
                                    bg=Theme.BG, highlightthickness=0)
        spinner_canvas.pack(pady=14)
        self._spinner_angle = 0
        self._spinner_canvas = spinner_canvas
        self._animate_spinner(spinner_canvas)

        tk.Label(self.search_frame, text="Scanning nearby areas...",
                 font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.BG).pack()

        # After 2.5 seconds, show driver found
        self.root.after(2500, self._show_driver_found)

    def _animate_spinner(self, canvas):
        if self.trip_phase != "matching":
            return
        if not canvas.winfo_exists():
            return
        canvas.delete("all")
        self._spinner_angle = (self._spinner_angle + 8) % 360
        cx, cy = 40, 40
        for i in range(12):
            angle = self._spinner_angle + i * 30
            rad = math.radians(angle)
            x = cx + 28 * math.cos(rad)
            y = cy + 28 * math.sin(rad)
            alpha = 0.3 + 0.7 * (1 - i / 12)
            color = lerp_color(Theme.PRIMARY, Theme.TEXT, alpha)
            size = 5 + 3 * (1 - i / 12)
            canvas.create_oval(x - size, y - size, x + size, y + size,
                               fill=color, outline="")
        self.root.after(40, lambda: self._animate_spinner(canvas))

    def _show_driver_found(self):
        if self.trip_phase != "matching":
            return
        self.trip_phase = "driver_found"
        self.search_frame.destroy()

        container = tk.Frame(self.content, bg=Theme.BG)
        container.place(relx=0.5, rely=0.35, anchor="center")

        # Success animation
        tk.Label(container, text="✓ Driver Found!",
                 font=self.font_title, fg=Theme.SUCCESS, bg=Theme.BG).pack(pady=10)

        # Driver card
        driver_card = self._make_card(container, bg=Theme.CARD)
        driver_card.pack(pady=10, ipadx=30, ipady=16)

        # Driver info
        d = self.driver
        info_frame = tk.Frame(driver_card, bg=Theme.CARD)
        info_frame.pack()

        # Avatar placeholder
        avatar = tk.Frame(info_frame, bg=Theme.PRIMARY, width=56, height=56)
        avatar.pack(side="left", padx=(0, 16))
        avatar.pack_propagate(False)
        avatar_lbl = tk.Label(avatar, text=d["name"][0],
                              font=self.font_title, fg=Theme.TEXT, bg=Theme.PRIMARY)
        avatar_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Info text
        info_text = tk.Frame(info_frame, bg=Theme.CARD)
        info_text.pack(side="left")
        tk.Label(info_text, text=d["name"], font=self.font_vehicle_name,
                 fg=Theme.TEXT, bg=Theme.CARD).pack(anchor="w")

        # Car info with color indicator
        car_row = tk.Frame(info_text, bg=Theme.CARD)
        car_row.pack(anchor="w")
        color_swatch = tk.Frame(car_row, bg=d["color"], width=12, height=12)
        color_swatch.pack(side="left", padx=(0, 6))
        color_swatch.pack_propagate(False)
        tk.Label(car_row, text=f"{d['car']} · {d['plate']}",
                 font=self.font_body, fg=Theme.TEXT_SEC, bg=Theme.CARD).pack(side="left")

        # Rating
        tk.Label(info_text, text=f"★ {d['rating']} · {d['trips']} trips",
                 font=self.font_small, fg=Theme.WARNING, bg=Theme.CARD).pack(anchor="w")

        # Vehicle info
        v = self.selected_vehicle
        tk.Label(driver_card, text=f"{v['icon']} {v['name']} · ${self.fare:.2f}",
                 font=self.font_body, fg=Theme.TEXT_SEC, bg=Theme.CARD).pack(pady=(8, 0))

        # ETA and continue
        eta_frame = tk.Frame(container, bg=Theme.BG)
        eta_frame.pack(pady=20)
        tk.Label(eta_frame, text=f"Driver is {v['eta']} away",
                 font=self.font_subtitle, fg=Theme.TEXT, bg=Theme.BG).pack()

        continue_btn = self._make_btn(container, "Watch driver arrive →",
                                      self.show_driver_arriving, bg=Theme.PRIMARY,
                                      padx=36, pady=12)
        continue_btn.pack(pady=10)

        self.set_status(f"Driver {d['name']} found · {v['eta']} away · {v['name']}")

    # ═══════════════════════════════════════════════════════════
    # SCREEN: DRIVER ARRIVING (animation)
    # ═══════════════════════════════════════════════════════════

    def show_driver_arriving(self):
        self.trip_phase = "arriving"
        self.set_phase("Driver arriving")
        self._clear_content()

        # Top info bar
        info_bar = tk.Frame(self.content, bg=Theme.SURFACE, height=60)
        info_bar.pack(fill="x")
        info_bar.pack_propagate(False)
        self.arrival_info_bar = info_bar

        d = self.driver
        v = self.selected_vehicle

        tk.Label(info_bar, text=f"{d['name']} · {v['eta']} away",
                 font=self.font_subtitle, fg=Theme.TEXT, bg=Theme.SURFACE).pack(side="left", padx=20, pady=10)
        tk.Label(info_bar, text=f"{d['car']} · {d['plate']}",
                 font=self.font_small, fg=Theme.TEXT_SEC, bg=Theme.SURFACE).pack(side="left", padx=10, pady=10)
        tk.Label(info_bar, text=f"★ {d['rating']}",
                 font=self.font_body, fg=Theme.WARNING, bg=Theme.SURFACE).pack(side="right", padx=20, pady=10)
        tk.Label(info_bar, text=f"${self.fare:.2f}",
                 font=self.font_price, fg=Theme.TEXT, bg=Theme.SURFACE).pack(side="right", padx=10, pady=10)

        # Map
        map_container = tk.Frame(self.content, bg=Theme.BG)
        map_container.pack(fill="both", expand=True)
        self.trip_map_container = map_container

        # Create the trip map.  The height is chosen to fit the complete window.
        self.trip_map = RideMap(map_container, width=880, height=430, bg=Theme.SURFACE)
        self.trip_map.pack(padx=14, pady=14)

        # Get points
        # Driver starts from a random point
        all_points = list(LOCATION_POINTS.values())
        driver_start = random.choice(all_points)
        pickup_pt = LOCATION_POINTS.get(self.pickup, (180, 190))
        dest_pt = LOCATION_POINTS.get(self.destination, (400, 290))

        # Draw initial city
        self.trip_map.set_points(pickup_pt, dest_pt)
        self.trip_map.draw_city()

        # Calculate path from driver to pickup
        driver_path = self._calc_path(driver_start, pickup_pt)
        trip_path = self._calc_path(pickup_pt, dest_pt)

        # Start driver arriving animation
        self._animation_step = 0
        self._driver_path = driver_path
        self._trip_path = trip_path
        self._is_arriving = True

        # Status label
        self.map_status = tk.Label(map_container, text="Driver is on the way...",
                                   font=self.font_body, fg=Theme.TEXT_SEC, bg=Theme.BG)
        self.map_status.pack(pady=(0, 8))

        self.root.after(500, lambda: self._animate_car_to_pickup())

    def _calc_path(self, start, end):
        """Calculate a path from start to end using the road grid."""
        # Find nearest road points
        road_points = list(LOCATION_POINTS.values())

        # Find nearest road points to start and end
        start_near = min(road_points, key=lambda p: distance(start, p))
        end_near = min(road_points, key=lambda p: distance(end, p))

        # Simple BFS through grid points
        grid = list(set(LOCATION_POINTS.values()))

        # Build adjacency list (connect points that share x or y and are close)
        adj = {p: [] for p in grid}
        for p1 in grid:
            for p2 in grid:
                if p1 == p2:
                    continue
                # Same x or same y, and within reasonable distance
                if (p1[0] == p2[0] and abs(p1[1] - p2[1]) < 200) or \
                   (p1[1] == p2[1] and abs(p1[0] - p2[0]) < 200):
                    adj[p1].append(p2)

        # BFS
        queue = [start_near]
        visited = {start_near}
        parent = {start_near: None}
        while queue:
            current = queue.pop(0)
            if current == end_near:
                break
            for neighbor in adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        # Reconstruct path
        path = []
        node = end_near
        while node is not None:
            path.append(node)
            node = parent.get(node)
        path.reverse()

        # Add exact start/end points
        if path:
            path[0] = start
            path[-1] = end

        return path if len(path) > 1 else [start, end]

    def _animate_car_to_pickup(self):
        if self.trip_phase not in ("arriving",):
            return

        path = self._driver_path
        step = self._animation_step
        total_steps = max(1, (len(path) - 1) * 10)  # 10 frames per segment

        if step < total_steps:
            seg = step // 10
            frac = (step % 10) / 10
            seg = min(seg, len(path) - 2)

            if seg < len(path) - 1:
                x1, y1 = path[seg]
                x2, y2 = path[seg + 1]
                cx = x1 + (x2 - x1) * self._smoothstep(frac)
                cy = y1 + (y2 - y1) * self._smoothstep(frac)

                self.trip_map.move_car(cx, cy)
                self._animation_step += 1
                self.root.after(50, self._animate_car_to_pickup)
            else:
                # Arrived at pickup!
                self._on_car_arrived_at_pickup()
        else:
            self._on_car_arrived_at_pickup()

    def _on_car_arrived_at_pickup(self):
        if self.trip_phase != "arriving":
            return
        self.map_status.config(text="✓ Driver has arrived! Getting in...",
                               fg=Theme.SUCCESS)

        # Flash the car
        self._flash_car(0)
        self.set_status("Driver arrived · Passenger boarding")

        # After a brief pause, start the trip
        self.root.after(1500, self._start_trip_phase)

    def _flash_car(self, count):
        if self.trip_phase not in ("arriving", "in_transit"):
            return
        if count < 6:
            color = Theme.WARNING if count % 2 == 0 else Theme.CAR_COLOR
            self.trip_map.set_car_color(color)
            self.root.after(200, lambda: self._flash_car(count + 1))
        else:
            self.trip_map.set_car_color(Theme.CAR_COLOR)

    def _start_trip_phase(self):
        if self.trip_phase != "arriving":
            return
        self.trip_phase = "in_transit"
        self.set_phase("En route")
        self.set_status(f"Heading to {self.destination}")
        self.map_status.config(text=f"📍 En route to {self.destination}")

        # Reset animation for trip
        self._animation_step = 0
        self._is_arriving = False

        # Hide the driver information bar and replace it with trip progress.
        if hasattr(self, "arrival_info_bar") and self.arrival_info_bar.winfo_exists():
            self.arrival_info_bar.destroy()

        # Trip progress bar at top
        self._trip_progress = tk.Frame(self.content, bg=Theme.SURFACE, height=50)
        if hasattr(self, "trip_map_container") and self.trip_map_container.winfo_exists():
            self._trip_progress.pack(fill="x", before=self.trip_map_container)
        else:
            self._trip_progress.pack(fill="x")
        self._trip_progress.pack_propagate(False)

        inner = tk.Frame(self._trip_progress, bg=Theme.SURFACE)
        inner.pack(fill="x", padx=20, pady=8)

        tk.Label(inner, text=f"→ {self.destination}", font=self.font_subtitle,
                 fg=Theme.TEXT, bg=Theme.SURFACE).pack(side="left")

        self.eta_label = tk.Label(inner, text=f"ETA: {int(self.trip_time)} min",
                                  font=self.font_body, fg=Theme.TEXT_SEC, bg=Theme.SURFACE)
        self.eta_label.pack(side="right")

        # Progress bar
        self.progress_canvas = tk.Canvas(inner, height=4, bg=Theme.BORDER,
                                          highlightthickness=0)
        self.progress_canvas.pack(fill="x", pady=(2, 0))
        self._progress_val = 0

        self.root.after(500, self._animate_car_to_destination)

    def _animate_car_to_destination(self):
        if self.trip_phase != "in_transit":
            return

        path = self._trip_path
        step = self._animation_step
        total_steps = max(1, (len(path) - 1) * 12)

        if step < total_steps:
            seg = step // 12
            frac = (step % 12) / 12
            seg = min(seg, len(path) - 2)

            if seg < len(path) - 1:
                x1, y1 = path[seg]
                x2, y2 = path[seg + 1]
                cx = x1 + (x2 - x1) * self._smoothstep(frac)
                cy = y1 + (y2 - y1) * self._smoothstep(frac)

                self.trip_map.move_car(cx, cy)

                # Update progress
                self._animation_step += 1
                progress = self._animation_step / total_steps
                self._update_trip_progress(progress)

                self.root.after(50, self._animate_car_to_destination)
            else:
                self._on_trip_complete()
        else:
            self._on_trip_complete()

    def _update_trip_progress(self, progress):
        if not hasattr(self, 'progress_canvas'):
            return
        self.progress_canvas.delete("all")
        w = self.progress_canvas.winfo_width()
        if w > 0:
            fill_w = w * min(progress, 1.0)
            # Gradient colour
            color = lerp_color(Theme.PRIMARY, Theme.SUCCESS, progress)
            self.progress_canvas.create_rectangle(0, 0, fill_w, 4, fill=color, outline="")

        remaining = max(0, int(self.trip_time * (1 - progress)))
        if hasattr(self, 'eta_label'):
            self.eta_label.config(text=f"ETA: {remaining} min")

        # Update status text
        pct = int(progress * 100)
        self.set_status(f"En route to {self.destination} · {pct}% complete")

    def _on_trip_complete(self):
        if self.trip_phase != "in_transit":
            return
        self.trip_phase = "complete"
        self.set_status("Trip completed!")
        self.show_trip_complete()

    # ═══════════════════════════════════════════════════════════
    # SCREEN: TRIP COMPLETE
    # ═══════════════════════════════════════════════════════════

    def show_trip_complete(self):
        self.set_phase("Trip complete")
        self._clear_content()

        container = tk.Frame(self.content, bg=Theme.BG)
        container.place(relx=0.5, rely=0.4, anchor="center")

        # Success indicator
        success_canvas = tk.Canvas(container, width=80, height=80,
                                    bg=Theme.BG, highlightthickness=0)
        success_canvas.pack(pady=(0, 10))

        # Draw checkmark circle
        success_canvas.create_oval(5, 5, 75, 75, fill=Theme.SUCCESS, outline="")
        success_canvas.create_line(25, 40, 37, 52, 58, 28,
                                    fill=Theme.TEXT, width=5, capstyle="round",
                                    joinstyle="round")

        tk.Label(container, text="Trip Complete!",
                 font=self.font_title, fg=Theme.TEXT, bg=Theme.BG).pack(pady=(0, 4))
        tk.Label(container, text=f"{self.pickup} → {self.destination}",
                 font=self.font_subtitle, fg=Theme.TEXT_SEC, bg=Theme.BG).pack()

        # Trip summary card
        summary = self._make_card(container, bg=Theme.CARD)
        summary.pack(pady=20, ipadx=24, ipady=16)

        v = self.selected_vehicle
        d = self.driver

        summary_inner = tk.Frame(summary, bg=Theme.CARD)
        summary_inner.pack()

        # Trip stats in a row
        stats = [
            f"📏 {self.trip_distance} km",
            f"⏱️ {int(self.trip_time)} min",
            f"🚗 {v['name']}",
            f"💰 ${self.fare:.2f}"
        ]
        stats_frame = tk.Frame(summary_inner, bg=Theme.CARD)
        stats_frame.pack(pady=4)
        for i, stat in enumerate(stats):
            tk.Label(stats_frame, text=stat, font=self.font_body,
                     fg=Theme.TEXT, bg=Theme.CARD).pack(side="left", padx=14)

        tk.Frame(summary_inner, bg=Theme.BORDER, height=1).pack(fill="x", pady=8)

        # Driver
        tk.Label(summary_inner, text=f"Driver: {d['name']} · {d['car']}",
                 font=self.font_body, fg=Theme.TEXT_SEC, bg=Theme.CARD).pack()

        # Fare breakdown
        tk.Frame(summary_inner, bg=Theme.BORDER, height=1).pack(fill="x", pady=8)

        tk.Label(summary_inner, text="Fare Breakdown",
                 font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack()
        fare_items = [
            f"Base fare: ${v['base_fare']:.2f}",
            f"Distance ({self.trip_distance}km × ${v['per_km']:.2f}): ${v['per_km'] * self.trip_distance:.2f}",
            f"Time ({int(self.trip_time)}min × ${v['per_min']:.2f}): ${v['per_min'] * self.trip_time:.2f}",
        ]
        for item in fare_items:
            tk.Label(summary_inner, text=item, font=("Helvetica", 9),
                     fg=Theme.TEXT_MUTED, bg=Theme.CARD).pack()

        tk.Frame(summary_inner, bg=Theme.SUCCESS, height=2).pack(fill="x", pady=6)

        tk.Label(summary_inner, text=f"Total: ${self.fare:.2f}",
                 font=self.font_price, fg=Theme.SUCCESS, bg=Theme.CARD).pack()

        # ═════════ RATING ═════════
        rating_frame = tk.Frame(container, bg=Theme.BG)
        rating_frame.pack(pady=10)

        tk.Label(rating_frame, text="Rate your ride",
                 font=self.font_subtitle, fg=Theme.TEXT, bg=Theme.BG).pack()

        self._rating_stars = []
        star_row = tk.Frame(rating_frame, bg=Theme.BG)
        star_row.pack(pady=6)

        for i in range(5):
            star = tk.Label(star_row, text="☆", font=self.font_icon,
                            fg=Theme.WARNING, bg=Theme.BG, cursor="hand2")
            star.pack(side="left", padx=4)
            star.bind("<Button-1>", lambda e, s=i+1: self._set_rating(s))
            star.bind("<Enter>", lambda e, s=i+1: self._preview_rating(s))
            star.bind("<Leave>", lambda e: self._reset_rating_preview())
            self._rating_stars.append(star)

        self.rating_label = tk.Label(rating_frame, text="Tap a star to rate",
                                     font=self.font_small, fg=Theme.TEXT_MUTED, bg=Theme.BG)
        self.rating_label.pack()

        # Thank you message + new trip
        self.thanks_frame = tk.Frame(container, bg=Theme.BG)
        self.thanks_frame.pack(pady=16)

        new_trip_btn = self._make_btn(
            container, "🔄 New Trip", self.show_welcome,
            bg=Theme.PRIMARY, padx=32, pady=12)
        new_trip_btn.pack(pady=10)

    def _set_rating(self, rating):
        self.rating = rating
        for i, star in enumerate(self._rating_stars):
            star.config(text="★" if i < rating else "☆", fg=Theme.WARNING)

        msgs = {
            1: "We're sorry! We'll improve.",
            2: "Thanks for your feedback.",
            3: "Thanks for riding with us!",
            4: "Great ride! We appreciate you!",
            5: "Amazing! You made our day! ⭐",
        }
        self.rating_label.config(text=msgs.get(rating, "Thanks!"), fg=Theme.SUCCESS)

        # Show thank you
        tk.Label(self.thanks_frame, text="",
                 font=self.font_subtitle, fg=Theme.TEXT, bg=Theme.BG).pack_forget()
        lbl = tk.Label(self.thanks_frame,
                       text="Thank you for riding with Uber!",
                       font=self.font_subtitle, fg=Theme.TEXT, bg=Theme.BG)
        lbl.pack(pady=6)

        self.set_status(f"Rated {rating}/5 · Thank you!")

    def _preview_rating(self, rating):
        for i, star in enumerate(self._rating_stars):
            star.config(text="★" if i < rating else "☆")

    def _reset_rating_preview(self):
        if self.rating > 0:
            for i, star in enumerate(self._rating_stars):
                star.config(text="★" if i < self.rating else "☆")
        else:
            for star in self._rating_stars:
                star.config(text="☆")

    # ═══════════════════════════════════════════════════════════
    # UTILITIES
    # ═══════════════════════════════════════════════════════════

    @staticmethod
    def _smoothstep(t):
        """Smooth interpolation."""
        return t * t * (3 - 2 * t)

    # ═══════════════════════════════════════════════════════════
    # RUN
    # ═══════════════════════════════════════════════════════════

    def run(self):
        self.root.mainloop()


# ═══════════════════════════════════════════════════════════════
# MAP CANVAS COMPONENT
# ═══════════════════════════════════════════════════════════════

class RideMap(tk.Frame):
    """Scalable city map with route markers and smooth car animation."""

    BASE_W = 760
    BASE_H = 500

    def __init__(self, parent, width=700, height=500, **kw):
        bg = kw.pop("bg", Theme.SURFACE)
        super().__init__(parent, bg=bg, width=width, height=height)
        self.config(highlightbackground=Theme.BORDER, highlightthickness=1)
        self.pack_propagate(False)

        self.map_w = width
        self.map_h = height
        self.scale = min(width / self.BASE_W, height / self.BASE_H)
        self.offset_x = (width - self.BASE_W * self.scale) / 2
        self.offset_y = (height - self.BASE_H * self.scale) / 2

        self.canvas = tk.Canvas(
            self, width=width, height=height, bg=Theme.MAP_BG,
            highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.pickup_pt = None
        self.dest_pt = None
        self.car_x = None
        self.car_y = None
        self.car_id = None
        self.car_color = Theme.CAR_COLOR

    def _xy(self, x, y):
        return self.offset_x + x * self.scale, self.offset_y + y * self.scale

    def _s(self, value):
        return max(1, value * self.scale)

    def set_points(self, pickup, dest):
        self.pickup_pt = pickup
        self.dest_pt = dest

    def set_car_color(self, color):
        self.car_color = color
        if self.car_id:
            self.canvas.itemconfig(self.car_id, fill=color)

    def draw_city(self):
        self.canvas.delete("all")
        self.car_id = None
        self._draw_background_grid()
        self._draw_roads()
        self._draw_blocks()
        self._draw_road_lines()
        self._draw_labels()
        self._draw_route_hint()

        if self.pickup_pt:
            self._draw_pin(*self.pickup_pt, Theme.PICKUP_COLOR, "PICKUP")
        if self.dest_pt:
            self._draw_pin(*self.dest_pt, Theme.DEST_COLOR, "DROP")

        # Small live-map badge.
        self.canvas.create_rectangle(12, 12, 92, 36, fill=Theme.SURFACE2,
                                     outline=Theme.BORDER, width=1)
        self.canvas.create_oval(22, 21, 28, 27, fill=Theme.SUCCESS, outline="")
        self.canvas.create_text(59, 24, text="LIVE MAP", fill=Theme.TEXT_SEC,
                                font=(Theme.FONT_FAMILY, 8, "bold"))

    def _draw_background_grid(self):
        grid_color = lerp_color(Theme.MAP_BG, "#FFFFFF", 0.035)
        spacing = max(28, int(45 * self.scale))
        for x in range(0, self.map_w, spacing):
            self.canvas.create_line(x, 0, x, self.map_h, fill=grid_color)
        for y in range(0, self.map_h, spacing):
            self.canvas.create_line(0, y, self.map_w, y, fill=grid_color)

    def _draw_roads(self):
        road_w = self._s(24)
        for x1, y1, x2, y2 in MAP_ROADS_H:
            ax1, ay1 = self._xy(x1, y1)
            ax2, ay2 = self._xy(x2, y2)
            self.canvas.create_rectangle(
                ax1, ay1 - road_w / 2, ax2, ay2 + road_w / 2,
                fill=Theme.MAP_STREET, outline=""
            )

        for x1, y1, x2, y2 in MAP_ROADS_V:
            ax1, ay1 = self._xy(x1, y1)
            ax2, ay2 = self._xy(x2, y2)
            self.canvas.create_rectangle(
                ax1 - road_w / 2, ay1, ax2 + road_w / 2, ay2,
                fill=Theme.MAP_STREET, outline=""
            )

    def _draw_road_lines(self):
        dash_step = 20
        for x1, y1, x2, y2 in MAP_ROADS_H:
            for x in range(int(x1), int(x2), dash_step):
                a1 = self._xy(x, y1)
                a2 = self._xy(min(x + 10, x2), y2)
                self.canvas.create_line(*a1, *a2, fill=Theme.MAP_STREET_LINE,
                                        width=max(1, int(self.scale)))

        for x1, y1, x2, y2 in MAP_ROADS_V:
            for y in range(int(y1), int(y2), dash_step):
                a1 = self._xy(x1, y)
                a2 = self._xy(x2, min(y + 10, y2))
                self.canvas.create_line(*a1, *a2, fill=Theme.MAP_STREET_LINE,
                                        width=max(1, int(self.scale)))

    def _draw_blocks(self):
        for bx, by, bw, bh, color, _label in CITY_BLOCKS:
            x1, y1 = self._xy(bx, by)
            x2, y2 = self._xy(bx + bw, by + bh)
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill=color,
                outline=lerp_color(color, "#000000", 0.20), width=1
            )

            if color == Theme.MAP_PARK:
                # Deterministic placement keeps the map visually stable on redraw.
                tree_positions = ((0.25, 0.35), (0.58, 0.25), (0.72, 0.68))
                for txf, tyf in tree_positions:
                    tx, ty = self._xy(bx + bw * txf, by + bh * tyf)
                    r = self._s(4)
                    self.canvas.create_oval(tx-r, ty-r, tx+r, ty+r,
                                            fill=Theme.MAP_PARK_TREE, outline="")
            elif color == Theme.MAP_WATER:
                wave_color = lerp_color(Theme.MAP_WATER, "#FFFFFF", 0.28)
                for wx in range(bx + 10, bx + bw - 10, 20):
                    p1 = self._xy(wx, by + bh / 2)
                    p2 = self._xy(wx + 10, by + bh / 2 - 4)
                    p3 = self._xy(wx + 20, by + bh / 2)
                    self.canvas.create_line(*p1, *p2, *p3, fill=wave_color,
                                            width=1, smooth=True)

    def _draw_labels(self):
        font_size = max(7, int(8 * self.scale))
        for bx, by, bw, bh, _color, label in CITY_BLOCKS:
            if label:
                x, y = self._xy(bx + bw / 2, by + bh / 2)
                self.canvas.create_text(
                    x, y, text=label, fill=Theme.TEXT_SEC,
                    font=(Theme.FONT_FAMILY, font_size, "bold")
                )

    def _draw_route_hint(self):
        if not (self.pickup_pt and self.dest_pt):
            return
        px, py = self.pickup_pt
        dx, dy = self.dest_pt
        p1 = self._xy(px, py)
        corner = self._xy(dx, py)
        p2 = self._xy(dx, dy)
        self.canvas.create_line(
            *p1, *corner, *p2, fill=lerp_color(Theme.PRIMARY, "#FFFFFF", 0.20),
            width=max(2, int(3 * self.scale)), dash=(6, 5), smooth=False
        )

    def _draw_pin(self, x, y, color, label):
        x, y = self._xy(x, y)
        glow = self._s(14)
        pin = self._s(8)
        self.canvas.create_oval(x-glow, y-glow, x+glow, y+glow,
                                fill=lerp_color(color, Theme.MAP_BG, 0.45), outline="")
        self.canvas.create_oval(x-pin, y-pin, x+pin, y+pin,
                                fill=color, outline=Theme.TEXT, width=2)
        self.canvas.create_text(
            x, y-self._s(19), text=label, fill=color,
            font=(Theme.FONT_FAMILY, max(7, int(8*self.scale)), "bold")
        )

    def move_car(self, x, y):
        """Move the car without leaving old wheel/window shapes behind."""
        self.canvas.delete("moving_car")
        self.car_x, self.car_y = x, y
        x, y = self._xy(x, y)
        size = max(10, self._s(12))

        # Soft shadow.
        self.canvas.create_oval(
            x-size, y+size*0.2, x+size, y+size*0.75,
            fill=Theme.SHADOW, outline="", tags="moving_car"
        )
        self.car_id = self.canvas.create_rectangle(
            x-size, y-size/2, x+size, y+size/2,
            fill=self.car_color, outline=Theme.TEXT, width=2,
            tags="moving_car"
        )
        self.canvas.create_rectangle(
            x-size*0.25, y-size/2+2, x+size*0.25, y+size/2-2,
            fill=lerp_color(self.car_color, "#FFFFFF", 0.45), outline="",
            tags="moving_car"
        )

        wheel = "#0B0D12"
        wr = max(2, size * 0.17)
        for wx in (x-size*0.68, x+size*0.68):
            for wy in (y-size*0.52, y+size*0.52):
                self.canvas.create_oval(wx-wr, wy-wr, wx+wr, wy+wr,
                                        fill=wheel, outline="", tags="moving_car")


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = UberRideSimulator()
    app.run()
