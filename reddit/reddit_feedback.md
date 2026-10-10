# Reddit Feedback

Comments from the r/esp32 thread [1s9dydh](https://www.reddit.com/r/esp32/comments/1s9dydh/), synchronized via RSS by `scripts/fetch_reddit.py`.

**Last sync:** 2026-10-10 16:21 UTC

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/):

> Hey r/esp32!
>
> I’m currently building a 1:10 scale RC car (Carten T410R) with my kids, trying to engineer it to reliably hit 100 km/h (62 mph).https://github.com/kleinnconrad/RC100.
>
> In my day job, I design data analytics platforms. So, naturally, I couldn't just drive the car – I needed to try to extract live data from it. The catch? While I know my way around data platforms, I am an absolute beginner when it comes to embedded programming. This is my very first hardware/C++ project.
>
> I intend to use an ESP32 to build a custom IoT telemetry device that rides inside the car. The goal is to collect live data during our speed runs and stream it back so we can analyze things like thermals and performance limits before the car melts.
>
> Since I’m completely new to the ESP32 ecosystem, I am 100% sure my first sketch is totally flawed.
>
> I uploaded the whole project to GitHub and would be incredibly grateful if some of the veterans here could take a quick look and give advice/hints or maybe you already did something similar?
>
> The Repo:
>
> https://github.com/kleinnconrad/carten\_telemetrie
>
> (Quick apology: My documentation/README is currently in German. Unfortunately this is required since this should be a family & friends project)
>
> Any tips or best practices for handling live data streams on a moving object at 100km/h would be hugely appreciated.

---

**u/Plastic_Fig9225** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odnq4e3/):

> Looks nice :)
>
> Personally, I would split the code into multiple tasks to avoid jitter in data sampling. Specifically, I'm not sure about unpredictable delays the MQTT stuff could introduce.
>
> For RPM/pulse-counting, you could look into using the ESP's PCNT ( Arduino ).
>
> Also, int rpm = pulses * (60000 / ingestionInterval); should rather be pulses * (60000 / (millis() - lastIngestionTime)) to account for jitter in the timing. Ideally, take the current timestamp as close to reading the pulses count as possible.
>
> You can also consider using a timer to do the data acquisition at fixed intervals, (quasi-)independent of the timing of other operations.

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odobii2/):

> Thanks a lot for the hint with the calc logic and the pulse counter! Makes total sense. I updated the code accordingly

---

**u/Plastic_Fig9225** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odptjd2/):

> With the PCNT, notice that "[t]he counter will reset to zero automatically when it crosses either the high or low limit." So another 'trick' to ensure accuracy and not lose any pulses would go like this:
>
> static const int16_t COUNTER_HIGH_LIMIT = 30000; static int16_t prevPulses; // Previous pulse counter value ... int16_t currentPulses = 0; // Read counter but let it keep counting: pcnt_get_counter_value( pcnt_unit, &currentPulses ); // Calculate number of pulses since last reading: int16_t deltaPulses = currentPulses - prevPulses; // update 'previous' value prevPulses = currentPulses; // Handle PCNT overflow: if(deltaPulses < 0) { // There was a PCNT overflow between the readings. // Adjust delta for the overflow: deltaPulses = deltaPulses + COUNTER_HIGH_LIMIT; }

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odqkzd8/):

> Thanks again. Discussed this with a LLM and it's def a very good hint. Would have never thought of this by myself. Just committed it.

---

**u/Plastic_Fig9225** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/ods93c3/):

> And... one more thing I noticed: Your telemetry does not include the speed?
>
> The GPS should provide a highly accurate "velocity over ground", much more accurate than you could ever infer from the position data - at least while not accelerating. You may want to include that in the telemetry data.

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odtzz1m/):

> Thank you so much for pointing out. I thought it was accidently thrown out at one point... But according to the commit history it was really never implemented.

---

**u/portugese_fruit** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoepnc/):

> that thing is a beaut

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoftb5/):

> Completely agree

---

**u/portugese_fruit** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odov0on/):

> where do you take it to race it, 100kph is possible on street?

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odovbdp/):

> Parking lots of big supermarkets when they are closed is the best

---

**u/jappiedoedelzak** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odohi8x/):

> take a look at ExpressRLS (https://www.expresslrs.org/). it's a opensource RC remote software+hardware ecosystem that also supports telemetry.

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odohx37/):

> Thanks! I'll have a look

---

**u/G-EDM** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odo9ijv/):

> What questions do you have exactly? How to stream the data? How to collect it? What type of data? Digital or Analog? As already mentioned PCNT could be of use for pulse counting while I2S ADC is the fastest option for analog data collection. To stream it back you may want to use DMA buffers and pack a batch of the data into a matching buffer the exact size of the data. If you have for example 8Bit data don't waste space and compress everything that every bit is used. On an ESP 32Bit is default and using the native size is faster then using 8 or 16Bit. If you have 8bit samples you can pack 4 of them into one 32Bit int. After packing a batch send it over the air. TL;DR DMA buffers, bit stuffing, PCNT and or I2S ADC, native 32bit int buffer for packing and bitwise operation where possible especially for packing the batch and also for math if possible. Things like (int) 10 /= 2 can be done with 10 >>= 1

---

**u/[unknown]** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoesab/):

> I'm intending to collect low frequency data (GPS, 1-Wire temperatures, and a Hall sensor) at a sample rate of 2Hz. I'm planning to then stream it over LTE via MQTT. My goal is to feed this telemetric data into a cloud. Because of that I assume that sending JSON payloads is currently the easiest route for the data ingest?! I guess I2S, DMA buffers and bit-packing are awesome suggestions but seems a bit overkill for my current 2Hz rate (on a first glance). I’ll keep the 32-bit packing trick in mind if I ever scale up to high-frequency analog sensors.

---

**u/G-EDM** [wrote](https://www.reddit.com/r/esp32/comments/1s9dydh/building_a_live_telemetry_system_for_my_100kmh_rc/odoofo8/):

> Ok. For 2hz it doesn't really need much and it could be done with DHL. :D

---
