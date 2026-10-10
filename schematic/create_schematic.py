"""Generate Schematic_Graphical.svg - a clean, orthogonal wiring schematic.

Layout idea:
  * ESP32 (U1) in the center, RC receiver (A1, power source) on the left.
  * All peripherals stacked in one column on the right; their data pins face
    the ESP32, their power pins face two vertical supply rails (the WAGO-221
    splice buses) at the far right.
  * Wires are routed orthogonally; each net has its own color and its own
    vertical channel so runs never overlap. A dot marks a junction, a
    crossing without a dot is not connected.

Run:  python create_schematic.py   (writes Schematic_Graphical.svg next to it)
"""

from pathlib import Path

# ------------------------------------------------------------------ palette
C_33V   = "#c62828"   # 3.3 V rail
C_5V    = "#e65100"   # 5 V from the receiver / BEC
C_GND   = "#263238"   # ground
C_MOSI  = "#1565c0"
C_MISO  = "#2e7d32"
C_SCK   = "#f9a825"
C_CS    = "#8e24aa"
C_GPSTX = "#00838f"   # GPS TX  -> ESP RX2
C_GPSRX = "#d81b60"   # ESP TX2 -> GPS RX
C_1W    = "#6d4c41"   # 1-Wire bus (D4)
C_HALL  = "#827717"   # Hall pulse (D2)

INK   = "#263238"     # primary text
MUTED = "#78909c"     # secondary text
FAINT = "#9aa0a6"     # unused pin labels
BODY_FILL, BODY_STROKE = "#fffbe6", "#8b1a1a"   # component bodies (KiCad-ish)
REF   = "#0b5394"     # reference designators (U1, A1, ...)
MONO  = "Consolas, 'Courier New', monospace"

# ------------------------------------------------------------------ helpers
S = []

def add(s):
    S.append(s)

def text(x, y, s, size=12, fill=INK, anchor="start", weight=None, style=None, family=None):
    t = f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
    if weight:
        t += f' font-weight="{weight}"'
    if style:
        t += f' font-style="{style}"'
    if family:
        t += f' font-family="{family}"'
    add(t + f'>{s}</text>')

def wire(points, color, width=2.5):
    d = "M " + " L ".join(f"{x} {y}" for x, y in points)
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linejoin="round" stroke-linecap="round"/>')

def dot(x, y, color):
    add(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')

def module(x, y, w, h, ref, title, sub, left=(), right=()):
    """Component box with pin stubs. left/right: list of (label, abs_y)."""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" '
        f'fill="{BODY_FILL}" stroke="{BODY_STROKE}" stroke-width="2"/>')
    text(x, y - 8, ref, 13, REF, weight="bold")
    text(x + w / 2, y + 22, title, 15, INK, anchor="middle", weight="bold")
    if sub:
        text(x + w / 2, y + 38, sub, 11, MUTED, anchor="middle")
    for label, py in left:
        add(f'<line x1="{x-20}" y1="{py}" x2="{x}" y2="{py}" stroke="#546e7a" stroke-width="2"/>')
        text(x + 8, py + 4, label, 12, INK, family=MONO)
    for label, py in right:
        add(f'<line x1="{x+w}" y1="{py}" x2="{x+w+20}" y2="{py}" stroke="#546e7a" stroke-width="2"/>')
        text(x + w - 8, py + 4, label, 12, INK, anchor="end", family=MONO)

# ------------------------------------------------------------------ ESP32
ESP_X, ESP_Y, ESP_W, ESP_H = 430, 240, 240, 584     # body 430..670 / 240..824
PIN_Y0, PIN_DY = 280, 36

LEFT_PINS  = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25",
              "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
RIGHT_PINS = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5",
              "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]
USED_LEFT  = {"GND", "VIN"}
USED_RIGHT = {"D23", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "GND", "3V3"}

def pin_y(i):
    return PIN_Y0 + i * PIN_DY

def esp32():
    x, y, w, h = ESP_X, ESP_Y, ESP_W, ESP_H
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" '
        f'fill="{BODY_FILL}" stroke="{BODY_STROKE}" stroke-width="2.5"/>')
    text(x, y - 8, "U1", 13, REF, weight="bold")
    cx = x + w / 2
    text(cx, 528, "ESP32", 20, INK, anchor="middle", weight="bold")
    text(cx, 550, "Freenove 30-pin", 12, MUTED, anchor="middle")
    text(cx, 568, "ESP-WROOM-32", 11, MUTED, anchor="middle", family=MONO)
    for i, lbl in enumerate(LEFT_PINS):
        py, used = pin_y(i), lbl in USED_LEFT
        add(f'<line x1="{x-20}" y1="{py}" x2="{x}" y2="{py}" '
            f'stroke="{"#546e7a" if used else "#c5cbd1"}" stroke-width="2"/>')
        text(x + 8, py + 4, lbl, 12, INK if used else FAINT, family=MONO,
             weight="bold" if used else None)
    for i, lbl in enumerate(RIGHT_PINS):
        py, used = pin_y(i), lbl in USED_RIGHT
        add(f'<line x1="{x+w}" y1="{py}" x2="{x+w+20}" y2="{py}" '
            f'stroke="{"#546e7a" if used else "#c5cbd1"}" stroke-width="2"/>')
        text(x + w - 8, py + 4, lbl, 12, INK if used else FAINT, anchor="end",
             family=MONO, weight="bold" if used else None)
    # USB connector hint at the bottom edge
    add(f'<rect x="{cx-25}" y="{y+h}" width="50" height="16" rx="3" '
        f'fill="#eceff1" stroke="#90a4ae" stroke-width="1.5"/>')
    text(cx, y + h + 12, "USB", 9, MUTED, anchor="middle")

# ------------------------------------------------------------------ sheet
def main():
    add('<?xml version="1.0" encoding="UTF-8"?>')
    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1150" '
        "font-family=\"'Segoe UI', Arial, sans-serif\">")
    add('<defs><pattern id="dots" width="25" height="25" patternUnits="userSpaceOnUse">'
        '<circle cx="1" cy="1" r="1" fill="#e3e7ea"/></pattern></defs>')
    add('<rect width="100%" height="100%" fill="#ffffff"/>')
    add('<rect width="100%" height="100%" fill="url(#dots)"/>')
    add('<rect x="25" y="25" width="1450" height="1100" fill="none" '
        'stroke="#78909c" stroke-width="1.5"/>')

    # --- heading + notes ------------------------------------------------
    text(45, 68, "CARTEN T410R TELEMETRY", 22, INK, weight="bold")
    text(45, 92, "Wiring schematic · ESP32 sensor node · GPS · microSD · 2× DS18B20 · Hall RPM",
         13, MUTED)
    text(950, 66, "All peripherals are powered from the ESP32 3V3 pin via WAGO-221 splice buses.", 11.5, "#607d8b")
    text(950, 84, "Both DS18B20 sensors share one 1-Wire bus on D4.", 11.5, "#607d8b")
    text(950, 102, "UART lines are crossed: GPS TX → ESP RX2, GPS RX ← ESP TX2.", 11.5, "#607d8b")

    # --- components -----------------------------------------------------
    esp32()
    module(120, 690, 230, 140, "A1", "RC Receiver", "powered from ESC / BEC",
           right=[("GND", 748), ("5 V", 784)])
    add('<path d="M 300 690 C 310 660, 330 665, 340 638" fill="none" '
        'stroke="#607d8b" stroke-width="2"/>')
    add('<circle cx="340" cy="636" r="3" fill="#607d8b"/>')

    module(950, 150, 250, 200, "U2", "MicroSD Module", "SPI card reader",
           left=[("MOSI", 215), ("MISO", 251), ("SCK", 287), ("CS", 323)],
           right=[("VCC", 215), ("GND", 251)])
    module(950, 400, 250, 140, "U3", "GPS BN-220", "UART · NMEA",
           left=[("TX", 460), ("RX", 496)],
           right=[("VCC", 460), ("GND", 496)])
    add('<rect x="1150" y="412" width="26" height="26" rx="2" '
        'fill="#eceff1" stroke="#90a4ae"/>')                 # ceramic antenna
    add('<circle cx="1171" cy="418" r="2.5" fill="#8d6e63"/>')
    module(950, 580, 250, 100, "U4", "DS18B20", "motor temperature · 1-Wire",
           left=[("DQ", 648)], right=[("VDD", 622), ("GND", 654)])
    module(950, 710, 250, 100, "U5", "DS18B20", "ESC temperature · 1-Wire",
           left=[("DQ", 778)], right=[("VDD", 752), ("GND", 784)])
    module(950, 840, 250, 100, "U6", "A3144 Hall", "RPM pulses → PCNT",
           left=[("DO", 908)], right=[("VCC", 882), ("GND", 914)])

    # --- supply rails (WAGO buses) --------------------------------------
    text(1360, 120, "WAGO-221 splice buses", 11, MUTED, anchor="middle", style="italic")
    text(1330, 142, "3.3 V", 13, C_33V, anchor="middle", weight="bold")
    text(1390, 142, "GND", 13, C_GND, anchor="middle", weight="bold")
    wire([(1330, 150), (1330, 970)], C_33V, 4)
    wire([(1390, 150), (1390, 995)], C_GND, 4)
    # ground symbol at the bottom of the GND rail
    wire([(1390, 995), (1390, 1002)], C_GND, 2.5)
    wire([(1378, 1002), (1402, 1002)], C_GND, 2.5)
    wire([(1383, 1007), (1397, 1007)], C_GND, 2.5)
    wire([(1388, 1012), (1392, 1012)], C_GND, 2.5)

    # --- power wiring ---------------------------------------------------
    wire([(370, 748), (410, 748)], C_GND, 3)                 # RC GND -> ESP GND
    wire([(370, 784), (410, 784)], C_5V, 3)                  # RC 5V  -> ESP VIN
    wire([(690, 784), (700, 784), (700, 970), (1330, 970)], C_33V, 3)   # 3V3 -> rail
    wire([(690, 748), (715, 748), (715, 995), (1390, 995)], C_GND, 3)   # GND -> rail
    for py in (215, 460, 622, 752, 882):                     # VCC taps
        wire([(1220, py), (1330, py)], C_33V, 3)
        dot(1330, py, C_33V)
    for py in (251, 496, 654, 784, 914):                     # GND taps
        wire([(1220, py), (1390, py)], C_GND, 3)
        dot(1390, py, C_GND)

    # --- data wiring (one vertical channel per net) ---------------------
    wire([(690, 280), (740, 280), (740, 215), (930, 215)], C_MOSI)   # D23 -> MOSI
    wire([(690, 460), (770, 460), (770, 251), (930, 251)], C_MISO)   # D19 -> MISO
    wire([(690, 496), (800, 496), (800, 287), (930, 287)], C_SCK)    # D18 -> SCK
    wire([(690, 532), (830, 532), (830, 323), (930, 323)], C_CS)     # D5  -> CS
    wire([(690, 568), (860, 568), (860, 496), (930, 496)], C_GPSRX)  # TX2 -> GPS RX
    wire([(690, 604), (890, 604), (890, 460), (930, 460)], C_GPSTX)  # RX2 <- GPS TX
    wire([(690, 640), (905, 640), (905, 778), (930, 778)], C_1W)     # D4 1-Wire bus
    wire([(905, 648), (930, 648)], C_1W)                             # tap to U4
    dot(905, 648, C_1W)
    wire([(690, 676), (730, 676), (730, 908), (930, 908)], C_HALL)   # D2 <- Hall DO

    # net labels at the module ends
    for lx, ly, lbl, col in [(924, 210, "D23", C_MOSI), (924, 246, "D19", C_MISO),
                             (924, 282, "D18", C_SCK),  (924, 318, "D5", C_CS),
                             (924, 455, "RX2", C_GPSTX), (924, 491, "TX2", C_GPSRX),
                             (924, 643, "D4", C_1W),    (924, 773, "D4", C_1W),
                             (924, 903, "D2", C_HALL)]:
        text(lx, ly, lbl, 10, col, anchor="end", family=MONO, weight="bold")

    # bus group labels
    text(860, 207, "SPI", 11, MUTED, anchor="middle", style="italic")
    text(862, 452, "UART2", 11, MUTED, anchor="middle", style="italic")
    text(820, 632, "1-Wire", 11, MUTED, anchor="middle", style="italic")
    text(810, 900, "PCNT (RPM)", 11, MUTED, anchor="middle", style="italic")

    # --- legend ---------------------------------------------------------
    text(45, 1055, "NET COLORS", 11, INK, weight="bold")
    text(140, 1055, "· a dot marks a junction — crossings without a dot are not connected",
         10, MUTED)
    legend = [("3.3 V rail", C_33V), ("5 V (BEC)", C_5V), ("GND", C_GND),
              ("MOSI — D23", C_MOSI), ("MISO — D19", C_MISO), ("SCK — D18", C_SCK),
              ("CS — D5", C_CS), ("GPS TX → RX2", C_GPSTX), ("TX2 → GPS RX", C_GPSRX),
              ("1-Wire — D4", C_1W), ("Hall — D2", C_HALL)]
    for i, (lbl, col) in enumerate(legend):
        lx, ly = 45 + (i % 6) * 150, 1075 + (i // 6) * 23
        wire([(lx, ly - 4), (lx + 22, ly - 4)], col, 3)
        text(lx + 28, ly, lbl, 11, INK)

    # --- title block ----------------------------------------------------
    add('<rect x="1015" y="1035" width="460" height="90" fill="#ffffff" '
        'stroke="#78909c" stroke-width="1.5"/>')
    text(1035, 1062, "CARTEN T410R TELEMETRY", 15, INK, weight="bold")
    text(1035, 1081, "Wiring schematic — ESP32 telemetry node", 11.5, MUTED)
    add('<line x1="1015" y1="1092" x2="1475" y2="1092" stroke="#78909c" stroke-width="1"/>')
    text(1035, 1111, "Date 2026-10-10", 10.5, MUTED)
    text(1210, 1111, "Rev 2.0", 10.5, MUTED)
    text(1330, 1111, "Sheet 1 / 1", 10.5, MUTED)

    add('</svg>')

    out = Path(__file__).parent / "Schematic_Graphical.svg"
    out.write_text("\n".join(S), encoding="utf-8")
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
