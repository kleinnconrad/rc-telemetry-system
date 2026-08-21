import graphviz

def create_perfect_offline_schematic_30pin():
    dot = graphviz.Digraph('Offline_Schematic', filename='Schematic_Offline_30Pin', format='png')
    
    # rankdir='LR' forces horizontal flow.
    dot.attr(rankdir='LR', splines='polyline', nodesep='1.0', ranksep='4.0')
    dot.attr('node', shape='none', fontname='Helvetica', fontsize='12')

    # 1. ESP32 CENTRAL (Now in correct 30-Pin Design!)
    esp32_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD COLSPAN="3" BGCOLOR="#add8e6"><B>ESP32 30-Pin (FREENOVE Board)</B></TD></TR>
      <TR><TD BGCOLOR="#d3d3d3"><B>Left Pins</B></TD><TD BGCOLOR="#e0e0e0" ROWSPAN="11"> ESP32 <br/> Core </TD><TD BGCOLOR="#d3d3d3"><B>Right Pins</B></TD></TR>
      <TR><TD PORT="vin">VIN (5V In)</TD><TD PORT="3v3">3V3 (3.3V Out)</TD></TR>
      <TR><TD PORT="gnd_l">GND</TD><TD PORT="gnd_r">GND</TD></TR>
      <TR><TD>---</TD><TD PORT="d2">D2 (Hall Sensor)</TD></TR>
      <TR><TD>---</TD><TD PORT="d4">D4 (1-Wire Temp)</TD></TR>
      <TR><TD>---</TD><TD PORT="rx2">RX2 / GPIO16</TD></TR>
      <TR><TD>---</TD><TD PORT="tx2">TX2 / GPIO17</TD></TR>
      <TR><TD>---</TD><TD PORT="d5">D5 (SD CS)</TD></TR>
      <TR><TD>---</TD><TD PORT="d18">D18 (SD SCK)</TD></TR>
      <TR><TD>---</TD><TD PORT="d19">D19 (SD MISO)</TD></TR>
      <TR><TD>---</TD><TD PORT="d23">D23 (SD MOSI)</TD></TR>
    </TABLE>>'''
    dot.node('ESP', label=esp32_html)

    # 2. COMPONENTS LEFT SIDE (Power supply only)
    rx_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#90ee90"><B>RC Receiver (BEC)</B></TD></TR>
      <TR><TD PORT="v5">5V (Red)</TD></TR>
      <TR><TD PORT="gnd">GND (Black)</TD></TR>
      <TR><TD PORT="signal">Signal (Unused)</TD></TR>
    </TABLE>>'''

    with dot.subgraph() as s_left:
        s_left.attr(rank='same')
        s_left.node('RX', label=rx_html)

    # 3. COMPONENTS RIGHT SIDE (All sensors + SD Card)
    sd_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#d3d3d3"><B>MicroSD (SPI)</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="mosi">MOSI</TD></TR>
      <TR><TD PORT="miso">MISO</TD></TR>
      <TR><TD PORT="sck">SCK</TD></TR>
      <TR><TD PORT="cs">CS</TD></TR>
    </TABLE>>'''

    gps_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#87cefa"><B>GPS BN-220</B></TD></TR>
      <TR><TD PORT="vcc">VCC (3.3V via WAGO)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="tx">TX (Send)</TD></TR>
      <TR><TD PORT="rx">RX (Receive)</TD></TR>
    </TABLE>>'''

    temp_mot_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 (Motor)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (3.3V via WAGO)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="dq">Data (Yellow/Blue)</TD></TR>
    </TABLE>>'''

    temp_esc_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffffe0"><B>DS18B20 (ESC)</B></TD></TR>
      <TR><TD PORT="vcc">VDD (3.3V via WAGO)</TD></TR>
      <TR><TD PORT="gnd">GND</TD></TR>
      <TR><TD PORT="dq">Data (Yellow/Blue)</TD></TR>
    </TABLE>>'''

    hall_html = '''<
    <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
      <TR><TD BGCOLOR="#ffb6c1"><B>A3144 Hall Sensor</B></TD></TR>
      <TR><TD PORT="vcc">1: VCC (3.3V via WAGO)</TD></TR>
      <TR><TD PORT="gnd">2: GND</TD></TR>
      <TR><TD PORT="out">3: DOUT (Signal)</TD></TR>
    </TABLE>>'''

    with dot.subgraph() as s_right:
        s_right.attr(rank='same')
        s_right.node('SD', label=sd_html)
        s_right.node('GPS', label=gps_html)
        s_right.node('TEMP_MOT', label=temp_mot_html)
        s_right.node('TEMP_ESC', label=temp_esc_html)
        s_right.node('HALL', label=hall_html)
        s_right.edge('SD', 'GPS', style='invis')
        s_right.edge('GPS', 'TEMP_MOT', style='invis')
        s_right.edge('TEMP_MOT', 'TEMP_ESC', style='invis')
        s_right.edge('TEMP_ESC', 'HALL', style='invis')

    # --- WIRING ---

    # LEFT SIDE -> Power from RC to ESP
    dot.edge('RX:v5:e', 'ESP:vin:w', color='red', penwidth='3', dir='none')
    dot.edge('RX:gnd:e', 'ESP:gnd_l:w', color='black', penwidth='3', dir='none')
    
    # RIGHT SIDE -> Data & 3.3V Routing
    
    # SD Card (VCC to 3.3V)
    dot.edge('ESP:3v3:e', 'SD:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'SD:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:d23:e', 'SD:mosi:w', color='blue', penwidth='2', dir='none')
    dot.edge('ESP:d19:e', 'SD:miso:w', color='blue', penwidth='2', dir='none')
    dot.edge('ESP:d18:e', 'SD:sck:w', color='blue', penwidth='2', dir='none')
    dot.edge('ESP:d5:e', 'SD:cs:w', color='blue', penwidth='2', dir='none')

    # GPS (UART crossed)
    dot.edge('ESP:3v3:e', 'GPS:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'GPS:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:rx2:e', 'GPS:tx:w', color='magenta', penwidth='2', dir='none') 
    dot.edge('ESP:tx2:e', 'GPS:rx:w', color='purple', penwidth='2', dir='none')  

    # Motor Temp
    dot.edge('ESP:3v3:e', 'TEMP_MOT:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'TEMP_MOT:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:d4:e', 'TEMP_MOT:dq:w', color='orange', penwidth='2', dir='none')

    # ESC Temp
    dot.edge('ESP:3v3:e', 'TEMP_ESC:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'TEMP_ESC:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:d4:e', 'TEMP_ESC:dq:w', color='orange', penwidth='2', dir='none')

    # Hall Sensor
    dot.edge('ESP:3v3:e', 'HALL:vcc:w', color='red', style='dashed', penwidth='2', dir='none')
    dot.edge('ESP:gnd_r:e', 'HALL:gnd:w', color='black', penwidth='2', dir='none')
    dot.edge('ESP:d2:e', 'HALL:out:w', color='green', penwidth='2', dir='none')

    dot.render(view=False)
    print("Updated 30-Pin Schematic (SD Card at 3.3V!) generated!")

if __name__ == '__main__':
    create_perfect_offline_schematic_30pin()
