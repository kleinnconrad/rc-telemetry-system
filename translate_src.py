import os

blink = """#include <Arduino.h>

// For the ESP32, the internal blue LED is often on pin 2
const int LED_PIN = 2; 

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ESP32 is alive and starting the test!");
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // LED on
  Serial.println("LED ON");
  delay(1000);                 // Wait 1 second
  
  digitalWrite(LED_PIN, LOW);  // LED off
  Serial.println("LED OFF");
  delay(1000);
}
"""

gps_test = """#include <Arduino.h>
#include <HardwareSerial.h>

const int GPS_RX_PIN = 16;
const int GPS_TX_PIN = 17;

HardwareSerial SerialGPS(2); // UART 2

void setup() {
  Serial.begin(115200);
  SerialGPS.begin(9600, SERIAL_8N1, GPS_RX_PIN, GPS_TX_PIN); // 9600 is standard for GPS
  Serial.println("Waiting for GPS raw data...");
}

void loop() {
  // If the GPS module sends data, print it immediately to the monitor
  while (SerialGPS.available()) {
    char c = SerialGPS.read();
    Serial.print(c);
  }
}
"""

hall = """#include <Arduino.h>

const int HALL_PIN = 2; // Your pin according to the schematic
volatile int magnetDetected = 0;

// This function is called in milliseconds when the magnet flies by
void IRAM_ATTR countPulse() {
  magnetDetected++;
}

void setup() {
  Serial.begin(115200);
  pinMode(HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(HALL_PIN), countPulse, FALLING);
  Serial.println("Waiting for magnet...");
}

void loop() {
  if (magnetDetected > 0) {
    Serial.print("Magnet detected! Counter: ");
    Serial.println(magnetDetected);
    magnetDetected = 0; // Reset counter for the next pass
  }
  delay(100);
}
"""

micro_sd = """#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

const int SD_CS_PIN = 5;

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing SD card...");

  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("Error: SD card not found or wired incorrectly!");
    return;
  }
  Serial.println("SD card found.");

  // Create and write test file
  File dataFile = SD.open("/test.txt", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Hello from the ESP32! The card is working.");
    dataFile.close();
    Serial.println("Successfully written to test.txt.");
  } else {
    Serial.println("Error opening the file.");
  }
}

void loop() {
  // Nothing else happens here
}
"""

temp_test = """#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const int ONE_WIRE_BUS = 4; // Your pin according to the schematic

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin();
  Serial.println("Temperature test started.");
}

void loop() {
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  
  Serial.print("Current temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  
  delay(1000);
}
"""

fetch_reddit = """import feedparser
from bs4 import BeautifulSoup
import os
from datetime import datetime

# RSS Feed URL of the specific Reddit thread
RSS_URL = 'https://www.reddit.com/r/rccars/comments/xyz123/my_custom_telemetry_system/.rss'

# Parse Feed
feed = feedparser.parse(RSS_URL)

if feed.bozo:
    print("Error fetching the feed!")
    exit(1)

# Assemble Markdown Header
md_content = "# Reddit Feedback: Live Telemetry System (RSS Sync)\\n\\n"
md_content += f"**Last Sync:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\\n\\n"
md_content += "---\\n\\n"

# Iterate through entries. The first entry is often the post itself, followed by comments.
for entry in feed.entries:
    # Read author (Reddit formats this as /u/username)
    author = entry.get('author', '[Unknown]').replace('/u/', '')
    link = entry.get('link', '')
    
    # The actual text is inside "summary" as HTML
    raw_html = entry.get('summary', '')
    
    # Use BeautifulSoup to remove HTML tags (like <p>, <a>)
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Extract text and keep line breaks
    text = soup.get_text(separator='\\n').strip()
    
    # Add Markdown Blockquote formatting (> )
    text_formatted = text.replace('\\n', '\\n> ')
    
    md_content += f"**u/{author}** [wrote]({link}):\\n"
    md_content += f"> {text_formatted}\\n\\n"
    md_content += "---\\n\\n"

# Create target folder and save
os.makedirs('reddit', exist_ok=True)
file_path = 'reddit/reddit_feedback.md'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(md_content)
    
print(f"Successfully saved {len(feed.entries)} entries to {file_path}!")
"""

schematic_without_lte = """import graphviz

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
"""

with open("src/tests/blink.cpp", "w", encoding="utf-8") as f: f.write(blink)
with open("src/tests/gps.cpp", "w", encoding="utf-8") as f: f.write(gps_test)
with open("src/tests/hall.cpp", "w", encoding="utf-8") as f: f.write(hall)
with open("src/tests/micro_sd.cpp", "w", encoding="utf-8") as f: f.write(micro_sd)
with open("src/tests/temp.cpp", "w", encoding="utf-8") as f: f.write(temp_test)
with open("scripts/fetch_reddit.py", "w", encoding="utf-8") as f: f.write(fetch_reddit)
with open("schematic/schematic_without_lte.py", "w", encoding="utf-8") as f: f.write(schematic_without_lte)
