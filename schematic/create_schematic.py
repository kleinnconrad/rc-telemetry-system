import json

svg_content = []

def add(s):
    svg_content.append(s)

def header():
    add('<?xml version="1.0" encoding="UTF-8"?>')
    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" style="background-color: #f0f2f5; font-family: \'Segoe UI\', Arial, sans-serif;">')
    
    # Grid pattern
    add('<defs>')
    add('<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">')
    add('<path d="M 20 0 L 0 0 0 20" fill="none" stroke="#e0e0e0" stroke-width="1"/>')
    add('</pattern>')
    add('<filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">')
    add('<feDropShadow dx="3" dy="3" stdDeviation="4" flood-opacity="0.3"/>')
    add('</filter>')
    add('</defs>')
    add('<rect width="100%" height="100%" fill="url(#grid)" />')

def footer():
    add('</svg>')

def draw_wire(x1, y1, x2, y2, color, stroke_width=4, curvature=0.5, is_vert=False):
    if is_vert:
        cx1, cy1 = x1, y1 + (y2-y1)*curvature
        cx2, cy2 = x2, y2 - (y2-y1)*curvature
    else:
        cx1, cy1 = x1 + (x2-x1)*curvature, y1
        cx2, cy2 = x2 - (x2-x1)*curvature, y2
        
    path = f'<path d="M {x1} {y1} C {cx1} {cy1}, {cx2} {cy2}, {x2} {y2}" fill="none" stroke="{color}" stroke-width="{stroke_width}" filter="url(#shadow)" stroke-linecap="round"/>'
    add(path)
    
def draw_esp32(cx, cy):
    # Board
    add(f'<rect x="{cx-90}" y="{cy-180}" width="180" height="360" rx="10" fill="#2d2d2d" filter="url(#shadow)"/>')
    # Chip
    add(f'<rect x="{cx-45}" y="{cy-160}" width="90" height="110" rx="4" fill="#555" stroke="#777" stroke-width="2"/>')
    add(f'<text x="{cx}" y="{cy-100}" fill="#ddd" font-size="10" text-anchor="middle" font-family="monospace">ESP-WROOM-32</text>')
    add(f'<text x="{cx}" y="{cy-80}" fill="#aaa" font-size="8" text-anchor="middle">FREENOVE 30-PIN</text>')
    
    # USB
    add(f'<rect x="{cx-20}" y="{cy+170}" width="40" height="15" rx="2" fill="#c0c0c0"/>')
    
    # Left Pins
    left_labels = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND", "VIN"]
    pins = {}
    for i, label in enumerate(left_labels):
        px, py = cx - 80, cy - 140 + i*20
        add(f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="#ffd700" rx="2"/>')
        add(f'<circle cx="{px}" cy="{py}" r="2" fill="#222"/>')
        add(f'<text x="{px+15}" y="{py+4}" fill="white" font-size="12" text-anchor="start">{label}</text>')
        pins[f"L_{label}"] = (px, py)
        
    # Right Pins
    right_labels = ["D23", "D22", "TX0", "RX0", "D21", "D19", "D18", "D5", "TX2", "RX2", "D4", "D2", "D15", "GND", "3V3"]
    for i, label in enumerate(right_labels):
        px, py = cx + 80, cy - 140 + i*20
        add(f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="#ffd700" rx="2"/>')
        add(f'<circle cx="{px}" cy="{py}" r="2" fill="#222"/>')
        add(f'<text x="{px-15}" y="{py+4}" fill="white" font-size="12" text-anchor="end">{label}</text>')
        pins[f"R_{label}"] = (px, py)
        
    return pins

def draw_wago(x, y, ports, label, color):
    w = 20 + ports*20
    h = 40
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#f0f0f0" stroke="#bbb" stroke-width="2" filter="url(#shadow)"/>')
    add(f'<rect x="{x}" y="{y}" width="{w}" height="15" rx="5" fill="#ff7f00"/>')
    add(f'<text x="{x+w/2}" y="{y+11}" fill="white" font-size="10" text-anchor="middle" font-weight="bold">WAGO {label}</text>')
    
    pin_coords = []
    for i in range(ports):
        px, py = x + 20 + i*20, y + 25
        add(f'<rect x="{px-6}" y="{py-6}" width="12" height="15" rx="2" fill="#d0d0d0" stroke="#999"/>')
        add(f'<circle cx="{px}" cy="{py+2}" r="3" fill="#333"/>')
        pin_coords.append((px, y+h))
    return pin_coords

def draw_module(x, y, w, h, title, pins, bg_color="#1e90ff"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{bg_color}" filter="url(#shadow)"/>')
    add(f'<text x="{x+w/2}" y="{y+20}" fill="white" font-size="14" text-anchor="middle" font-weight="bold">{title}</text>')
    
    pin_coords = {}
    total = len(pins)
    spacing = min(20, (h - 40) / max(1, (total - 1))) if total > 1 else 20
    start_y = y + (h - (total-1)*spacing) / 2
    
    for i, label in enumerate(pins):
        px, py = x + 10, start_y + i*spacing
        add(f'<rect x="{px-5}" y="{py-5}" width="10" height="10" fill="#ffd700" rx="2"/>')
        add(f'<circle cx="{px}" cy="{py}" r="2" fill="#222"/>')
        add(f'<text x="{px+15}" y="{py+4}" fill="white" font-size="12" text-anchor="start">{label}</text>')
        pin_coords[label] = (px-5, py)
        
    return pin_coords

def draw_to92(x, y, title):
    # A simple TO-92 front view
    add(f'<rect x="{x-15}" y="{y-15}" width="30" height="25" rx="5" fill="#222" filter="url(#shadow)"/>')
    add(f'<text x="{x}" y="{y+5}" fill="#ccc" font-size="8" text-anchor="middle">{title}</text>')
    # Legs
    pins = {}
    labels = ["1", "2", "3"]
    for i, lbl in enumerate(labels):
        px = x - 10 + i*10
        py = y + 10
        add(f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py+20}" stroke="#c0c0c0" stroke-width="4"/>')
        pins[lbl] = (px, py+20)
    return pins

def draw_rc_receiver(x, y):
    w, h = 80, 140
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#444" stroke="#222" stroke-width="2" filter="url(#shadow)"/>')
    add(f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" rx="2" fill="#32cd32"/>')
    add(f'<text x="{x+w/2}" y="{y+30}" fill="white" font-size="14" text-anchor="middle" font-weight="bold">RC Empf.</text>')
    
    # Antenna
    add(f'<path d="M {x+w} {y+10} C {x+w+30} {y-20}, {x+w+50} {y+40}, {x+w+80} {y-10}" fill="none" stroke="#222" stroke-width="2"/>')
    
    # Pins (Right side)
    labels = ["Signal", "5V", "GND"]
    pins = {}
    for i, lbl in enumerate(labels):
        px, py = x + w - 10, y + 80 + i*20
        add(f'<rect x="{px-5}" y="{py-5}" width="15" height="10" fill="#ffd700" rx="1"/>')
        add(f'<text x="{px-15}" y="{py+4}" fill="black" font-size="12" text-anchor="end" font-weight="bold">{lbl}</text>')
        pins[lbl] = (px+10, py)
        
    return pins

def main():
    header()
    
    # Coordinates
    ESP_X, ESP_Y = 600, 450
    WAGO3_X, WAGO3_Y = 850, 150
    WAGOG_X, WAGOG_Y = 850, 250
    
    MOD_X = 1100
    
    # Draw ESP32
    esp_pins = draw_esp32(ESP_X, ESP_Y)
    
    # Draw WAGOs (8 ports to fit everything)
    wago3_pins = draw_wago(WAGO3_X, WAGO3_Y, 8, "3.3V", "#ff0000")
    wagog_pins = draw_wago(WAGOG_X, WAGOG_Y, 8, "GND", "#000000")
    
    # Draw Modules
    rc_pins = draw_rc_receiver(150, 400)
    sd_pins = draw_module(MOD_X, 100, 120, 160, "MicroSD", ["CS", "SCK", "MISO", "MOSI", "VCC", "GND"], bg_color="#4b0082")
    gps_pins = draw_module(MOD_X, 300, 120, 120, "GPS BN-220", ["GND", "TX", "RX", "VCC"], bg_color="#1e90ff")
    
    # Adding antenna on GPS
    add(f'<rect x="{MOD_X+60}" y="{330}" width="50" height="50" rx="2" fill="white" stroke="#ccc"/>')
    add(f'<circle cx="{MOD_X+100}" cy="{340}" r="3" fill="#8b4513"/>')
    
    ds_motor = draw_to92(MOD_X + 60, 500, "DS18B20 (Motor)")
    ds_esc = draw_to92(MOD_X + 60, 650, "DS18B20 (ESC)")
    hall = draw_to92(MOD_X + 60, 800, "A3144 (Hall)")
    
    # Draw Wires
    wires = []
    
    # RC -> ESP32
    wires.append((rc_pins["5V"], esp_pins["L_VIN"], "red", 0.3))
    wires.append((rc_pins["GND"], esp_pins["L_GND"], "black", 0.3))
    
    # ESP32 -> WAGOs
    wires.append((esp_pins["R_3V3"], wago3_pins[0], "red", 0.5, True))
    wires.append((esp_pins["R_GND"], wagog_pins[0], "black", 0.5, True))
    
    # SD Module
    wires.append((sd_pins["VCC"], wago3_pins[1], "red", 0.4, True))
    wires.append((sd_pins["GND"], wagog_pins[1], "black", 0.4, True))
    wires.append((sd_pins["MOSI"], esp_pins["R_D23"], "#0000ff", 0.6))
    wires.append((sd_pins["MISO"], esp_pins["R_D19"], "#00aa00", 0.6))
    wires.append((sd_pins["SCK"], esp_pins["R_D18"], "#ffaa00", 0.6))
    wires.append((sd_pins["CS"], esp_pins["R_D5"], "#ff5500", 0.6))
    
    # GPS
    wires.append((gps_pins["VCC"], wago3_pins[2], "red", 0.4, True))
    wires.append((gps_pins["GND"], wagog_pins[2], "black", 0.4, True))
    wires.append((gps_pins["TX"], esp_pins["R_RX2"], "#ff00ff", 0.6))
    wires.append((gps_pins["RX"], esp_pins["R_TX2"], "#aa00ff", 0.6))
    
    # DS18B20 Motor (1:GND, 2:DQ, 3:VDD)
    wires.append((ds_motor["1"], wagog_pins[3], "black", 0.5, True))
    wires.append((ds_motor["2"], esp_pins["R_D4"], "#00aaaa", 0.7))
    wires.append((ds_motor["3"], wago3_pins[3], "red", 0.5, True))
    
    # DS18B20 ESC (1:GND, 2:DQ, 3:VDD)
    wires.append((ds_esc["1"], wagog_pins[4], "black", 0.5, True))
    wires.append((ds_esc["2"], esp_pins["R_D4"], "#00aaaa", 0.7)) # sharing D4
    wires.append((ds_esc["3"], wago3_pins[4], "red", 0.5, True))
    
    # A3144 Hall Sensor (1:VCC, 2:GND, 3:DOUT)
    wires.append((hall["1"], wago3_pins[5], "red", 0.5, True))
    wires.append((hall["2"], wagog_pins[5], "black", 0.5, True))
    wires.append((hall["3"], esp_pins["R_D2"], "#55ff55", 0.7))
    
    for w in wires:
        if len(w) == 5:
            draw_wire(w[0][0], w[0][1], w[1][0], w[1][1], w[2], curvature=w[3], is_vert=w[4])
        else:
            draw_wire(w[0][0], w[0][1], w[1][0], w[1][1], w[2], curvature=w[3])
            
    footer()
    
    with open("Schaltplan_Graphical.svg", "w") as f:
        f.write("\\n".join(svg_content))
        
if __name__ == "__main__":
    main()
