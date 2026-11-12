# Daily Data Ingestion & Quality Audit Report

**Run Timestamp**: 2026-11-12 15:32:11  
**Ingestion Window**: 2026-10-13 to 2026-11-12 (Last 30 Days up to Today 12 Nov 2026)  
**Total Records Processed**: 17,846 | **Accepted**: 17,664 | **Quarantined**: 182

---

## 1. Per-Source Ingestion & Policy Execution Status

| Source ID | Name | Type | Status | Fetched | Accepted | Quarantined | Key Reasons / Directives |
|---|---|---|---|---|---|---|---|
| `data_gov_in` | Open Government Data (OGD) Agmarknet API | api | **success** | 17319 | 17149 | 170 | Price Rs 72000.0/qtl outside plausible bounds [100.0, 25000.... |
| `agmarknet_portal` | Agmarknet Directorate of Marketing & Inspection Portal | csv_download | **success** | 432 | 420 | 12 | Price Rs 28743.64/qtl outside plausible bounds [100.0, 25000... |
| `raita_mitra_karnataka` | Karnataka Agriculture Dept / KSAMB (Raita Mitra) | html | **returned_no_data** | 0 | 0 | 0 | Clean ingest... |
| `enam_portal` | National Agriculture Market (e-NAM) | html | **blocked_by_policy** | 0 | 0 | 0 | policy: Blocked by policy: automated access restricted by e-... |
| `weather_open_meteo` | Open-Meteo High-Resolution Agro-Meteorology API | api | **success** | 93 | 93 | 0 | Clean ingest... |
| `weather_nasa_power` | NASA POWER Global Agroclimatology API | api | **returned_no_data** | 0 | 0 | 0 | Clean ingest... |
| `diesel_ppac` | Petroleum Planning & Analysis Cell (PPAC) Retail Fuel | csv_download | **success** | 2 | 2 | 0 | Clean ingest... |

---

## 2. Ingested Data Distribution by Mandi (Last 30 Days)

| Mandi Location | Verified Real Rows | First Trade Date | Last Trade Date | Commodities Observed |
|---|---|---|---|---|
| **A lot APMC** | 4 | 2026-11-03 | 2026-11-03 | onion, wheat, soyabean, maize |
| **A.Jattihalli(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | coriander(leaves), ginger(green), cabbage, capsicum |
| **APMC  Chimur** | 2 | 2026-11-03 | 2026-11-03 | soyabean, paddy(common) |
| **APMC  Latur** | 6 | 2026-11-03 | 2026-11-03 | safflower, soyabean, red gram/arhar/tur(whole), bengal gram(gram)(whole) |
| **APMC  Rajura** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC  Yawal** | 2 | 2026-11-03 | 2026-11-03 | banana, maize |
| **APMC Ahmedpur** | 6 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), wheat, green gram(moong)(whole), bengal gram(gram)(whole) |
| **APMC Akola** | 12 | 2026-11-03 | 2026-11-03 | cotton, onion, garlic, soyabean |
| **APMC Alibagh** | 1 | 2026-11-03 | 2026-11-03 | rice |
| **APMC Amalner** | 7 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), bajra(pearl millet/cumbu), wheat, jowar(sorghum) |
| **APMC Amarawati** | 10 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), red gram/arhar/tur(whole), jowar(sorghum), bengal gram(gram)(whole) |
| **APMC Ambad (Vadigodri)** | 3 | 2026-11-03 | 2026-11-03 | jowar(sorghum), soyabean, wheat |
| **APMC Ambejogai** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Amgaon** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Anajngaon** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), wheat |
| **APMC Arvi** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Ashti** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Aurad Shahajani** | 7 | 2026-11-03 | 2026-11-03 | soyabean, wheat, green gram(moong)(whole), black gram(urd beans)(whole) |
| **APMC Azadpur** | 54 | 2026-11-03 | 2026-11-03 | apple, banana, garlic, ginger(green) |
| **APMC Babhulgaon** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Bagasara** | 8 | 2026-11-03 | 2026-11-03 | wheat, corriander seed, black gram(urd beans)(whole), soyabean |
| **APMC Baramati** | 3 | 2026-11-03 | 2026-11-03 | groundnut, sunflower/sunflower seed, soyabean |
| **APMC Barshi** | 6 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), maize, green gram(moong)(whole), soyabean |
| **APMC Barshi Takli** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Beed** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), soyabean |
| **APMC Bhandara** | 2 | 2026-11-03 | 2026-11-03 | rice, bengal gram(gram)(whole) |
| **APMC Bhokar** | 3 | 2026-11-03 | 2026-11-03 | soyabean, sesamum(sesame,gingelly,til), bengal gram(gram)(whole) |
| **APMC Bhusaval** | 24 | 2026-11-03 | 2026-11-03 | guar, cabbage, methi(leaves), lime |
| **APMC Brahmpuri** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Chamorshi** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Chandrapur** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Chandwad** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **APMC Chattrapati Sambhajinagar** | 31 | 2026-11-03 | 2026-11-03 | wheat, pomegranate, guava, seetapal |
| **APMC Chikali** | 4 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), soyabean, red gram/arhar/tur(whole), bengal gram(gram)(whole) |
| **APMC Daryapur** | 4 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), bengal gram(gram)(whole), red gram/arhar/tur(whole), soyabean |
| **APMC Deoulgaon Raja** | 5 | 2026-11-03 | 2026-11-03 | jowar(sorghum), maize, black gram(urd beans)(whole), wheat |
| **APMC Devala** | 7 | 2026-11-03 | 2026-11-03 | wheat, bengal gram(gram)(whole), red gram/arhar/tur(whole), maize |
| **APMC Dhadgaon** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), maize |
| **APMC Digras** | 4 | 2026-11-03 | 2026-11-03 | wheat, bengal gram(gram)(whole), red gram/arhar/tur(whole), soyabean |
| **APMC Dondaicha** | 6 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), jowar(sorghum), maize, chili red |
| **APMC Dudhani** | 8 | 2026-11-03 | 2026-11-03 | wheat, bengal gram(gram)(whole), red gram/arhar/tur(whole), jowar(sorghum) |
| **APMC Gadchiroli** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Gangakhed** | 2 | 2026-11-03 | 2026-11-03 | wheat, soyabean |
| **APMC Gangapur** | 6 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), wheat, red gram/arhar/tur(whole), green gram(moong)(whole) |
| **APMC Ghatanji** | 2 | 2026-11-03 | 2026-11-03 | cotton, soyabean |
| **APMC Ghoti** | 5 | 2026-11-03 | 2026-11-03 | cauliflower, cucumbar(kheera), cabbage, chilly capsicum |
| **APMC Gondiya** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Gondpimpri** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC HALVAD** | 10 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), soyabean, groundnut, castor seed |
| **APMC Hingna** | 26 | 2026-11-03 | 2026-11-03 | lime, bhindi(ladies finger), bottle gourd, cucumbar(kheera) |
| **APMC Hingoli** | 3 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), soyabean, turmeric |
| **APMC Indapur** | 2 | 2026-11-03 | 2026-11-03 | onion, seetapal |
| **APMC Islampur** | 11 | 2026-11-03 | 2026-11-03 | ginger(green), bhindi(ladies finger), bottle gourd, tomato |
| **APMC Jalana** | 10 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), bengal gram(gram)(whole), green gram(moong)(whole), red gram/arhar/tur(whole) |
| **APMC Jalgaon** | 32 | 2026-11-03 | 2026-11-03 | wheat, jowar(sorghum), bengal gram(gram)(whole), bhindi(ladies finger) |
| **APMC Jamkhed** | 5 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), soyabean, black gram(urd beans)(whole), onion |
| **APMC Jamner** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **APMC Jintur** | 2 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), soyabean |
| **APMC Kalmeshwar** | 12 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cauliflower, cabbage, methi(leaves) |
| **APMC Kalvan** | 2 | 2026-11-03 | 2026-11-03 | maize, onion |
| **APMC Kalyan** | 21 | 2026-11-03 | 2026-11-03 | onion, rice, black gram(urd beans)(whole), green peas |
| **APMC Kamthi** | 16 | 2026-11-03 | 2026-11-03 | tomato, green chilli, seetapal, bhindi(ladies finger) |
| **APMC Karanja** | 6 | 2026-11-03 | 2026-11-03 | soyabean, green gram(moong)(whole), red gram/arhar/tur(whole), bengal gram(gram)(whole) |
| **APMC Karjat** | 4 | 2026-11-03 | 2026-11-03 | jowar(sorghum), wheat, maize, onion |
| **APMC Karjat(Raigad)** | 2 | 2026-11-03 | 2026-11-03 | rice, paddy(common) |
| **APMC Karmala** | 4 | 2026-11-03 | 2026-11-03 | jowar(sorghum), maize, sunflower/sunflower seed, wheat |
| **APMC Katol** | 6 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), wheat, groundnut, cotton |
| **APMC Keshopur** | 24 | 2026-11-03 | 2026-11-03 | pomegranate, bottle gourd, bitter gourd, brinjal |
| **APMC Khamgaon** | 9 | 2026-11-03 | 2026-11-03 | wheat, red gram/arhar/tur(whole), bengal gram(gram)(whole), maize |
| **APMC Khed** | 14 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), chilly capsicum, brinjal, potato |
| **APMC Kille Dharur** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), soyabean |
| **APMC Kinwat** | 2 | 2026-11-03 | 2026-11-03 | soyabean, cotton |
| **APMC Kolhapur** | 7 | 2026-11-03 | 2026-11-03 | onion, green chilli, brinjal, cauliflower |
| **APMC Kopargaon** | 5 | 2026-11-03 | 2026-11-03 | onion, bengal gram(gram)(whole), wheat, maize |
| **APMC Lasalgaon** | 4 | 2026-11-03 | 2026-11-03 | maize, soyabean, onion, wheat |
| **APMC Mahagaon** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Majalgaon** | 8 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), soyabean, wheat, red gram/arhar/tur(whole) |
| **APMC Malegaon** | 8 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), green gram(moong)(whole), bajra(pearl millet/cumbu), maize |
| **APMC Mandhal** | 1 | 2026-11-03 | 2026-11-03 | chili red |
| **APMC Mangaon** | 1 | 2026-11-03 | 2026-11-03 | rice |
| **APMC Manmad** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **APMC Manora** | 2 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), soyabean |
| **APMC Mehekar** | 4 | 2026-11-03 | 2026-11-03 | soyabean, wheat, red gram/arhar/tur(whole), bengal gram(gram)(whole) |
| **APMC Morshi** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Mudkhed** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Mul** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Mumbai** | 60 | 2026-11-03 | 2026-11-03 | green chilli, mustard, masur dal, black gram dal(urd dal) |
| **APMC Murtizapur** | 4 | 2026-11-03 | 2026-11-03 | wheat, bengal gram(gram)(whole), red gram/arhar/tur(whole), soyabean |
| **APMC Murud** | 1 | 2026-11-03 | 2026-11-03 | rice |
| **APMC Murum** | 6 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), red gram/arhar/tur(whole), black gram(urd beans)(whole), jowar(sorghum) |
| **APMC Nagbhid** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Nagpur** | 44 | 2026-11-03 | 2026-11-03 | pomegranate, mousambi(sweet lime), orange, amla(nelli kai) |
| **APMC Naigaon** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Nandgaon** | 4 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), soyabean, wheat, green gram(moong)(whole) |
| **APMC Nasik** | 21 | 2026-11-03 | 2026-11-03 | papaya, orange, bottle gourd, cucumbar(kheera) |
| **APMC Nilanga** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Paithan** | 7 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), black gram(urd beans)(whole), green gram(moong)(whole), wheat |
| **APMC Palghar** | 1 | 2026-11-03 | 2026-11-03 | rice |
| **APMC Palus** | 13 | 2026-11-03 | 2026-11-03 | tomato, soyabean, ginger(green), beans |
| **APMC Pandhakawada** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Pandharpur** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **APMC Panvel** | 10 | 2026-11-03 | 2026-11-03 | tomato, guar, little gourd(kundru), bottle gourd |
| **APMC Paranda** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **APMC Partur** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Patan** | 5 | 2026-11-03 | 2026-11-03 | green chilli, ginger(green), bhindi(ladies finger), tomato |
| **APMC Pathari** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), jowar(sorghum), soyabean |
| **APMC Pavani** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Pimpalgaon Baswant** | 2 | 2026-11-03 | 2026-11-03 | pomegranate, onion |
| **APMC Pulgaon** | 2 | 2026-11-03 | 2026-11-03 | cotton, soyabean |
| **APMC Pune** | 55 | 2026-11-03 | 2026-11-03 | ground nut seed, pineapple, banana, lime |
| **APMC Pusad** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Rahata** | 26 | 2026-11-03 | 2026-11-03 | soyabean, ginger(green), potato, guar |
| **APMC Rahuri** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **APMC Ralegaon** | 2 | 2026-11-03 | 2026-11-03 | cotton, soyabean |
| **APMC Ramtek** | 12 | 2026-11-03 | 2026-11-03 | onion, chilly capsicum, green chilli, potato |
| **APMC Ratnagiri (Nachane)** | 13 | 2026-11-03 | 2026-11-03 | ginger(green), bhindi(ladies finger), tomato, bitter gourd |
| **APMC Risod** | 3 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), red gram/arhar/tur(whole), soyabean |
| **APMC Samudrapur** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **APMC Sangamner** | 3 | 2026-11-03 | 2026-11-03 | onion, tomato, pomegranate |
| **APMC Sangli** | 9 | 2026-11-03 | 2026-11-03 | jowar(sorghum), bajra(pearl millet/cumbu), rice, maize |
| **APMC Sangola** | 1 | 2026-11-03 | 2026-11-03 | pomegranate |
| **APMC Satana** | 4 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), wheat, onion, maize |
| **APMC Satara** | 17 | 2026-11-03 | 2026-11-03 | bottle gourd, drumstick, ginger(green), carrot |
| **APMC Savali** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Savner** | 7 | 2026-11-03 | 2026-11-03 | cotton, soyabean, maize, red gram/arhar/tur(whole) |
| **APMC Sengoan** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Shevgaon** | 2 | 2026-11-03 | 2026-11-03 | wheat, soyabean |
| **APMC Shirur** | 7 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), red gram/arhar/tur(whole), wheat, bengal gram(gram)(whole) |
| **APMC Sillod** | 3 | 2026-11-03 | 2026-11-03 | maize, soyabean, wheat |
| **APMC Sindi** | 2 | 2026-11-03 | 2026-11-03 | soyabean, bengal gram(gram)(whole) |
| **APMC Sinner** | 7 | 2026-11-03 | 2026-11-03 | onion, bengal gram(gram)(whole), jowar(sorghum), bajra(pearl millet/cumbu) |
| **APMC Solapur** | 33 | 2026-11-03 | 2026-11-03 | rice, bhindi(ladies finger), cabbage, jowar(sorghum) |
| **APMC Taloda** | 2 | 2026-11-03 | 2026-11-03 | wheat, soyabean |
| **APMC Tasgaon** | 5 | 2026-11-03 | 2026-11-03 | soyabean, wheat, jowar(sorghum), bengal gram(gram)(whole) |
| **APMC Telhara** | 5 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), soyabean, wheat, jowar(sorghum) |
| **APMC Tiroda** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **APMC Tuljapur** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), soyabean |
| **APMC Udgir** | 4 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), red gram/arhar/tur(whole), green gram(moong)(whole), soyabean |
| **APMC Ulhasnagar** | 2 | 2026-11-03 | 2026-11-03 | rice, wheat |
| **APMC Umared** | 2 | 2026-11-03 | 2026-11-03 | soyabean, cotton |
| **APMC Umarga** | 4 | 2026-11-03 | 2026-11-03 | jowar(sorghum), wheat, soyabean, red gram/arhar/tur(whole) |
| **APMC Umarkhed** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **APMC Vaduj** | 4 | 2026-11-03 | 2026-11-03 | onion, brinjal, green chilli, potato |
| **APMC Vani** | 2 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), soyabean |
| **APMC Varora** | 2 | 2026-11-03 | 2026-11-03 | soyabean, cotton |
| **APMC Vita** | 4 | 2026-11-03 | 2026-11-03 | tomato, green chilli, brinjal, bhindi(ladies finger) |
| **APMC Wardha** | 5 | 2026-11-03 | 2026-11-03 | cotton, red gram/arhar/tur(whole), soyabean, wheat |
| **APMC Yavatmal** | 3 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), red gram/arhar/tur(whole), soyabean |
| **APMC/MAC Shopian** | 1 | 2026-11-03 | 2026-11-03 | apple |
| **APMCKHEDBRAHMA** | 8 | 2026-11-03 | 2026-11-03 | wheat, soyabean, maize, groundnut |
| **ARWM Muvattupuzha** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Abohar APMC** | 14 | 2026-11-03 | 2026-11-03 | green chilli, brinjal, cotton, cauliflower |
| **Achanta APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Adampur APMC** | 19 | 2026-11-03 | 2026-11-03 | sweet potato, paddy(fine/superfine/grade a), carrot, capsicum |
| **Addanki APMC** | 3 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), paddy(common), maize |
| **Adilabad (Rythu Bazar)** | 6 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cauliflower, cabbage, green chilli |
| **Adilabad APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Adimali Market** | 9 | 2026-11-03 | 2026-11-03 | ashgourd, brinjal, amaranthus, beetroot |
| **Adoni APMC** | 3 | 2026-11-03 | 2026-11-03 | castor seed, groundnut, cotton |
| **Agar APMC** | 13 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), soyabean, garlic, coriander(leaves) |
| **Agar(F&V) APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Ahmedabad APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Ahmedabad(Chimanbhai Patal Market Vasana) APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Ahmedgarh APMC** | 9 | 2026-11-03 | 2026-11-03 | raddish, potato, tomato, banana |
| **Ahwa-Dang APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Ajaygarh APMC** | 4 | 2026-11-03 | 2026-11-03 | green peas, mustard, wheat, sesamum(sesame,gingelly,til) |
| **Ajitwal (Chogawan) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Ajitwal APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Ajmer(F&V) APMC** | 33 | 2026-11-03 | 2026-11-03 | guava, kinnow, karbuja(musk melon), pineapple |
| **Akiveedu APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Akodiya APMC** | 5 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), soyabean, wheat, garlic |
| **Akodiya(F&V) APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, garlic |
| **Akola(Borgaon Manju)** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Alacode  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Alampur APMC** | 4 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), paddy(common), wheat, mustard |
| **Alamuru APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Alangudi(Uzhavar Sandhai )** | 21 | 2026-11-03 | 2026-11-03 | pumpkin, potato, green chilli, snakeguard |
| **Alengad  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Alirajpur APMC** | 5 | 2026-11-03 | 2026-11-03 | cotton, soyabean, groundnut, wheat |
| **Allagadda APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Alur APMC** | 1 | 2026-11-03 | 2026-11-03 | jowar(sorghum) |
| **Aluva Market** | 14 | 2026-11-03 | 2026-11-03 | bitter gourd, brinjal, cauliflower, drumstick |
| **Amadalavalasa APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Amargarh APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Amarpatan APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, kodo millet(varagu) |
| **Amarpur APMC** | 3 | 2026-11-03 | 2026-11-03 | brinjal, onion, potato |
| **Amarwda APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Ambaha APMC** | 1 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu) |
| **Ambajipeta APMC** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Amballur  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Ambasamudram(Uzhavar Sandhai )** | 8 | 2026-11-03 | 2026-11-03 | pumpkin, brinjal, tomato, ashgourd |
| **Ambattur(Uzhavar Sandhai )** | 9 | 2026-11-03 | 2026-11-03 | amaranthus, banana - green, bhindi(ladies finger), potato |
| **Ambikapur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Amloh APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Ammapet(Uzhavar Sandhai )** | 57 | 2026-11-03 | 2026-11-03 | cauliflower, papaya, bottle gourd, groundnut |
| **Amoda APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Amrawati(Frui & Veg. Market)** | 31 | 2026-11-03 | 2026-11-03 | chikoos(sapota), papaya, bitter gourd, pumpkin |
| **Anaiyur(Uzhavar Sandhai )** | 57 | 2026-11-03 | 2026-11-03 | water melon, groundnut, pumpkin, green chilli |
| **Anakapally APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **Anand(Veg,Yard,Anand) APMC** | 12 | 2026-11-03 | 2026-11-03 | green chilli, bhindi(ladies finger), cauliflower, tomato |
| **Anandapur APMC** | 2 | 2026-11-03 | 2026-11-03 | bitter gourd, pumpkin |
| **Anantapur APMC** | 1 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime) |
| **Anaparthy APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Anchal Market** | 21 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), elephant yam(suran)/amorphophallus, onion, carrot |
| **Anchal VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Andipatti(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | cauliflower, papaya, bitter gourd, pumpkin |
| **Angadippuram VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Angamaly Market** | 31 | 2026-11-03 | 2026-11-03 | banana, amaranthus, pineapple, brinjal |
| **Angul APMC** | 10 | 2026-11-03 | 2026-11-03 | pointed gourd(parval), onion, little gourd(kundru), ridgeguard(tori) |
| **Anjad APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, green gram(moong)(whole), cotton |
| **Anjar APMC** | 6 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), castor seed, cummin seed(jeera), sesamum(sesame,gingelly,til) |
| **Ankleshwar APMC** | 13 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), bottle gourd, ginger(green), potato |
| **Anna nagar(Uzhavar Sandhai )** | 67 | 2026-11-03 | 2026-11-03 | potato, chili red, ashgourd, amaranthus |
| **Annamanada  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Anta APMC** | 3 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal), mustard, soyabean |
| **Anuppur APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), buttery |
| **Aralamoodu Market** | 24 | 2026-11-03 | 2026-11-03 | pineapple, bhindi(ladies finger), carrot, cauliflower |
| **Arani(Uzhavar Sandhai )** | 40 | 2026-11-03 | 2026-11-03 | tomato, amaranthus, ashgourd, beans |
| **Aranthangi(Uzhavar Sandhai )** | 22 | 2026-11-03 | 2026-11-03 | onion, ashgourd, brinjal, bhindi(ladies finger) |
| **Arcot(Uzhavar Sandhai )** | 46 | 2026-11-03 | 2026-11-03 | potato, banana - green, tapioca, thondekai |
| **Ariyalur(Uzhavar Sandhai)** | 25 | 2026-11-03 | 2026-11-03 | cluster beans, bottle gourd, amaranthus, drumstick |
| **Armori(Desaiganj)** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Arnod APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Aron APMC** | 5 | 2026-11-03 | 2026-11-03 | coriander(leaves), wheat, soyabean, bengal gram(gram)(whole) |
| **Aroor Market** | 12 | 2026-11-03 | 2026-11-03 | elephant yam(suran)/amorphophallus, carrot, cabbage, bhindi(ladies finger) |
| **Aruppukottai(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | garlic, chikoos(sapota), papaya, bitter gourd |
| **Arwal APMC** | 2 | 2026-11-03 | 2026-11-03 | potato, onion |
| **Asandh APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(basmati), paddy(common) |
| **Asansol APMC** | 13 | 2026-11-03 | 2026-11-03 | brinjal, tomato, green gram dal(moong dal), peas(dry) |
| **Ashoknagar APMC** | 11 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), maize, buttery, green peas |
| **Ashta APMC** | 8 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), wheat, onion, maize |
| **Ashti(Karanja)** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Ateli APMC** | 1 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu) |
| **Athirampuzha VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | little gourd(kundru) |
| **Athur(Uzhavar Sandhai )** | 53 | 2026-11-03 | 2026-11-03 | tomato, amaranthus, beans, capsicum |
| **Atmakur (Nandyal District) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Atmakur (SPSR Nellore District) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Attabira APMC** | 7 | 2026-11-03 | 2026-11-03 | cauliflower, cabbage, bitter gourd, pumpkin |
| **Attari APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Attayampatti(Uzhavar Sandhai )** | 29 | 2026-11-03 | 2026-11-03 | papaya, bottle gourd, sweet potato, pumpkin |
| **Attili APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Attingal Market** | 9 | 2026-11-03 | 2026-11-03 | brinjal, banana, elephant yam(suran)/amorphophallus, banana - green |
| **Avallapalli(Uzhavar Sandhai )** | 44 | 2026-11-03 | 2026-11-03 | onion, potato, tomato, cluster beans |
| **B.Kothakota H/Q Angallu** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **B.N.Kandriga APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Babai (Makhan Nagar) APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), wheat |
| **Babain APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Babra APMC** | 6 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), sesamum(sesame,gingelly,til), cummin seed(jeera), cotton |
| **Babrala APMC** | 3 | 2026-11-03 | 2026-11-03 | potato, wood, paddy(basmati) |
| **Bachaibari APMC** | 4 | 2026-11-03 | 2026-11-03 | goat, brinjal, cock, potato |
| **Badamalhera APMC** | 3 | 2026-11-03 | 2026-11-03 | wheat, soyabean, groundnut |
| **Badarwas APMC** | 6 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), wheat, groundnut, maize |
| **Badepally APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, paddy(common), groundnut, castor seed |
| **Badhni Kalan APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Badhni Kallan (Bilaspur) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Badnagar APMC** | 8 | 2026-11-03 | 2026-11-03 | onion, garlic, kabuli chana(chickpeas-white), bengal gram(gram)(whole) |
| **Badnawar APMC** | 9 | 2026-11-03 | 2026-11-03 | maize, onion, soyabean, green peas |
| **Badod APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, wheat, maize |
| **Badvel APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Badwaha APMC** | 5 | 2026-11-03 | 2026-11-03 | cotton, maize, rose(loose)), soyabean |
| **Badwani APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Bagbahra APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Baghty APMC** | 3 | 2026-11-03 | 2026-11-03 | ashgourd, pumpkin, ginger(green) |
| **Bagli APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, maize |
| **Bahadajholla APMC** | 1 | 2026-11-03 | 2026-11-03 | pumpkin |
| **Bahadurgarh APMC** | 22 | 2026-11-03 | 2026-11-03 | bitter gourd, cauliflower, bhindi(ladies finger), onion |
| **Baikunthpur APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, mustard, mahua, lak(teora) |
| **Baktara APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Balaghat APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), wheat |
| **Balaramapuram  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Balarampur APMC** | 9 | 2026-11-03 | 2026-11-03 | onion, brinjal, rice, bhindi(ladies finger) |
| **Ballabhgarh APMC** | 18 | 2026-11-03 | 2026-11-03 | bottle gourd, bhindi(ladies finger), brinjal, raddish |
| **Balliah APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Balod APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Balodabazar APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Balugaon APMC** | 1 | 2026-11-03 | 2026-11-03 | bitter gourd |
| **Balurghat APMC** | 11 | 2026-11-03 | 2026-11-03 | raddish, tomato, cauliflower, onion |
| **Balwadi APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, soyabean |
| **Bamora APMC** | 10 | 2026-11-03 | 2026-11-03 | buttery, lentil(masur)(whole), paddy(common), wheat |
| **Banaganapalli APMC** | 3 | 2026-11-03 | 2026-11-03 | jowar(sorghum), paddy(common), maize |
| **Banapura APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, green gram(moong)(whole), wheat, bengal gram(gram)(whole) |
| **Banda APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, mustard, wheat, lentil(masur)(whole) |
| **Bangarupalyam APMC** | 1 | 2026-11-03 | 2026-11-03 | mango |
| **Bankhedi APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), green gram(moong)(whole), wheat |
| **Banki APMC** | 16 | 2026-11-03 | 2026-11-03 | banana - green, tomato, pointed gourd(parval), green chilli |
| **Bankura Sadar APMC** | 8 | 2026-11-03 | 2026-11-03 | brinjal, masur dal, rice(fine/superfine/grade a), onion |
| **Banmorkalan APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), bajra(pearl millet/cumbu) |
| **Bapauli APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(basmati), paddy(common) |
| **Bara Bazar (Posta Bazar) APMC** | 4 | 2026-11-03 | 2026-11-03 | onion, garlic, potato, ginger(dry) |
| **Barad APMC** | 7 | 2026-11-03 | 2026-11-03 | soyabean, groundnut, wheat, bengal gram(gram)(whole) |
| **Barahat APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Baramkela APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Barara APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Barasat APMC** | 8 | 2026-11-03 | 2026-11-03 | green chilli, bitter gourd, onion, brinjal |
| **Barbigha APMC** | 5 | 2026-11-03 | 2026-11-03 | bitter gourd, brinjal, cucumbar(kheera), bottle gourd |
| **Bardewri APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bardoli(Kadod) APMC** | 4 | 2026-11-03 | 2026-11-03 | brinjal, green chilli, bottle gourd, bhindi(ladies finger) |
| **Bardoli(Madhi) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bareli APMC** | 7 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), paddy(common), wheat, red gram/arhar/tur(whole) |
| **Bareta APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), paddy(basmati) |
| **Bargarh APMC** | 5 | 2026-11-03 | 2026-11-03 | brinjal, cabbage, bhindi(ladies finger), onion |
| **Bargarh(Barapalli) APMC** | 5 | 2026-11-03 | 2026-11-03 | onion, bhindi(ladies finger), cabbage, brinjal |
| **Baripada APMC** | 7 | 2026-11-03 | 2026-11-03 | ridgeguard(tori), bitter gourd, bhindi(ladies finger), brinjal |
| **Barpathari APMC** | 6 | 2026-11-03 | 2026-11-03 | cowpea(veg), spiny gourd / kartali(kantola), pointed gourd(parval), brinjal |
| **Barshi(Vairag)** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), soyabean |
| **Baruipur(Canning) APMC** | 10 | 2026-11-03 | 2026-11-03 | rice, sweet pumpkin, guava, onion |
| **Barwala APMC** | 7 | 2026-11-03 | 2026-11-03 | bottle gourd, onion, brinjal, potato |
| **Barwala(Hisar) APMC** | 29 | 2026-11-03 | 2026-11-03 | mustard, bitter gourd, cauliflower, carrot |
| **Bassi APMC** | 11 | 2026-11-03 | 2026-11-03 | wheat, tomato, groundnut, bajra(pearl millet/cumbu) |
| **Bassi Pathana APMC** | 28 | 2026-11-03 | 2026-11-03 | papaya, bhindi(ladies finger), cauliflower, ginger(green) |
| **Bathinda APMC** | 8 | 2026-11-03 | 2026-11-03 | potato, mousambi(sweet lime), garlic, apple |
| **Baxirhat APMC** | 4 | 2026-11-03 | 2026-11-03 | rice, brinjal, jute, potato |
| **Bayana APMC** | 3 | 2026-11-03 | 2026-11-03 | onion, tomato, potato |
| **Bazpur APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), potato, rice |
| **Beawar APMC** | 2 | 2026-11-03 | 2026-11-03 | isabgul(psyllium), bajra(pearl millet/cumbu) |
| **Begamganj APMC** | 9 | 2026-11-03 | 2026-11-03 | buttery, bengal gram(gram)(whole), soyabean, maize |
| **Begu APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Bejjenki APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Bellampally APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, cotton |
| **Bengaluru (Yeshwanthpur)** | 98 | 2026-10-13 | 2026-11-12 | bajra, barley, jowar, maize |
| **Benipatti APMC** | 6 | 2026-11-03 | 2026-11-03 | cabbage, brinjal, green chilli, bhindi(ladies finger) |
| **Beohari APMC** | 3 | 2026-11-03 | 2026-11-03 | mahua, wheat, mustard |
| **Berachha APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Berasia APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, soyabean, bengal gram(gram)(whole), paddy(common) |
| **Beri APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(basmati), bajra(pearl millet/cumbu) |
| **Bethuadahari APMC** | 6 | 2026-11-03 | 2026-11-03 | jute, ridgeguard(tori), onion, green chilli |
| **Betnoti APMC** | 7 | 2026-11-03 | 2026-11-03 | papaya(raw), cabbage, bitter gourd, pumpkin |
| **Betul APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, soyabean, wheat |
| **Betul(F&V) APMC** | 9 | 2026-11-03 | 2026-11-03 | ginger(green), onion, brinjal, potato |
| **Bhabhar APMC** | 3 | 2026-11-03 | 2026-11-03 | cummin seed(jeera), groundnut, castor seed |
| **Bhadaur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhadaur(Sehna) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhadrachalam APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), cotton |
| **Bhadrak APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Bhadson APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Bhagta Bhai Ka (Jalal) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhagta Bhai Ka APMC** | 4 | 2026-11-03 | 2026-11-03 | green chilli, potato, tomato, onion |
| **Bhagta Bhai Ka(Kotha Guru Ka) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhagwanpur Mandi APMC** | 6 | 2026-11-03 | 2026-11-03 | brinjal, bhindi(ladies finger), cauliflower, onion |
| **Bhagwanpur(Naveen Mandi Sthal) APMC** | 9 | 2026-11-03 | 2026-11-03 | brinjal, apple, banana, tomato |
| **Bhainsa APMC** | 9 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), sesamum(sesame,gingelly,til), jowar(sorghum), wheat |
| **Bhander APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), wheat, mustard |
| **Bhanjanagar APMC** | 7 | 2026-11-03 | 2026-11-03 | yam(ratalu), papaya(raw), cabbage, cowpea(veg) |
| **Bhanpura APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, maize, wheat |
| **Bhawanigarh APMC** | 21 | 2026-11-03 | 2026-11-03 | potato, mousambi(sweet lime), methi(leaves), cauliflower |
| **Bhehjoi APMC** | 2 | 2026-11-03 | 2026-11-03 | wood, potato |
| **Bhensdehi APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Bherunda (Nasrullaganj) APMC** | 7 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), maize, soyabean, paddy(common) |
| **Bhesan APMC** | 3 | 2026-11-03 | 2026-11-03 | cotton, groundnut, soyabean |
| **Bhikangaon APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, maize, wheat |
| **Bhikhi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhikhiwind APMC** | 1 | 2026-11-03 | 2026-11-03 | cauliflower |
| **Bhiloda APMC** | 6 | 2026-11-03 | 2026-11-03 | soyabean, groundnut, wheat, black gram(urd beans)(whole) |
| **Bhimadole APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhimavaram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhimunipatnam APMC** | 1 | 2026-11-03 | 2026-11-03 | ragi(finger millet) |
| **Bhind APMC** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), mustard, wheat |
| **Bhinmal APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Bhitarwar APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bhokardan(Pimpalgaon Renu)** | 3 | 2026-11-03 | 2026-11-03 | soyabean, maize, wheat |
| **Bhopal APMC** | 9 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), garlic, soyabean, wheat |
| **Bhucho APMC** | 7 | 2026-11-03 | 2026-11-03 | carrot, cabbage, potato, green chilli |
| **Bhulath (Nadala) APMC** | 6 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), spinach, potato, indian colza(sarson) |
| **Bhulath APMC** | 6 | 2026-11-03 | 2026-11-03 | potato, green chilli, indian colza(sarson), cucumbar(kheera) |
| **Bhupalapally APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Biaora APMC** | 10 | 2026-11-03 | 2026-11-03 | garlic, soyabean, wheat, bengal gram(gram)(whole) |
| **Biaora(F&V) APMC** | 4 | 2026-11-03 | 2026-11-03 | potato, ginger(green), tomato, onion |
| **Bihpur APMC** | 3 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), brinjal, bitter gourd |
| **Bijawar APMC** | 4 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), maize, soyabean, wheat |
| **Bijaynagar APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, cotton, jowar(sorghum) |
| **Bilaspur APMC** | 3 | 2026-11-03 | 2026-11-03 | banana, paddy(fine/superfine/grade a), apple |
| **Bilimora APMC** | 10 | 2026-11-03 | 2026-11-03 | brinjal, bottle gourd, cabbage, bhindi(ladies finger) |
| **Bina APMC** | 10 | 2026-11-03 | 2026-11-03 | green peas, wheat, bengal gram(gram)(whole), mustard |
| **Binaganj APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, bengal gram(gram)(whole), mustard, maize |
| **Biokhora** | 2 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), carrot |
| **Birbhum APMC** | 9 | 2026-11-03 | 2026-11-03 | potato, paddy(common), onion, mustard oil |
| **Birmaharajpur APMC** | 4 | 2026-11-03 | 2026-11-03 | tomato, brinjal, onion, potato |
| **Birpur APMC** | 2 | 2026-11-03 | 2026-11-03 | tomato, onion |
| **Bishalgarh APMC** | 8 | 2026-11-03 | 2026-11-03 | potato, cucumbar(kheera), rice(fine/superfine/grade a), sweet pumpkin |
| **Bishenpur APMC** | 11 | 2026-11-03 | 2026-11-03 | paddy(common), rice, bengal gram(gram)(whole), masur dal |
| **Bishnupur(Bankura) APMC** | 8 | 2026-11-03 | 2026-11-03 | bottle gourd, mustard, masur dal, wheat |
| **Bishramganj** | 4 | 2026-11-03 | 2026-11-03 | tomato, green chilli, brinjal, pointed gourd(parval) |
| **Boath APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Bodeliu APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Bodinayakanur(Uzhavar Sandhai )** | 30 | 2026-11-03 | 2026-11-03 | papaya, tomato, cluster beans, carrot |
| **Boha APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bolpur APMC** | 8 | 2026-11-03 | 2026-11-03 | potato, brinjal, paddy(common), green chilli |
| **Bonai APMC** | 9 | 2026-11-03 | 2026-11-03 | tomato, bitter gourd, bhindi(ladies finger), cucumbar(kheera) |
| **Bori** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Botad APMC** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), bajra(pearl millet/cumbu) |
| **Boudh APMC** | 10 | 2026-11-03 | 2026-11-03 | tomato, bhindi(ladies finger), onion, cabbage |
| **Bowenpally APMC** | 28 | 2026-11-03 | 2026-11-03 | sweet potato, tomato, bhindi(ladies finger), cabbage |
| **Bsk Krishi Bazar Private Limited, Mehkar, Dist Buldhana** | 4 | 2026-11-03 | 2026-11-03 | wheat, soyabean, bengal gram(gram)(whole), red gram/arhar/tur(whole) |
| **Budalur RM** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Budhar APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Budhlada (Phaphre Bhaike) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Bumhama Kupwara (F&V)** | 1 | 2026-11-03 | 2026-11-03 | walnut |
| **Bundi APMC** | 7 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), green gram(moong)(whole), paddy(common), wheat |
| **Burdwan APMC** | 8 | 2026-11-03 | 2026-11-03 | rice, tomato, gur(jaggery), potato |
| **Burgampadu APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Burhanpur APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, wheat, cotton, soyabean |
| **Burhanpur(F&V) APMC** | 18 | 2026-11-03 | 2026-11-03 | bottle gourd, brinjal, tomato, bitter gourd |
| **Buxur APMC** | 7 | 2026-11-03 | 2026-11-03 | cabbage, cauliflower, green chilli, pointed gourd(parval) |
| **CHHUTMALPUR APMC** | 12 | 2026-11-03 | 2026-11-03 | brinjal, raddish, french beans(frasbean), bottle gourd |
| **Chaakghat APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Chakdah APMC** | 7 | 2026-11-03 | 2026-11-03 | green chilli, brinjal, tomato, onion |
| **Chakrata APMC** | 2 | 2026-11-03 | 2026-11-03 | ginger(green), colacasia |
| **Chalakudy Market** | 1 | 2026-11-03 | 2026-11-03 | coconut seed |
| **Chamoli APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Champaknagar APMC** | 5 | 2026-11-03 | 2026-11-03 | cabbage, pointed gourd(parval), cauliflower, green chilli |
| **Chanarthal APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Chanderi APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, wheat, maize |
| **Chandigarh (Grain/F&V) APMC** | 22 | 2026-11-03 | 2026-11-03 | onion, apple, orange, carrot |
| **Chandragiri APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **Chandrapur(Ganjwad)** | 8 | 2026-11-03 | 2026-11-03 | cabbage, carrot, bitter gourd, onion |
| **Channapetta VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana - green |
| **Chansama APMC** | 2 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal), cotton |
| **Chathannoore VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana - green |
| **Chaurai APMC** | 2 | 2026-11-03 | 2026-11-03 | soyabean, maize |
| **Chavakkad Market** | 16 | 2026-11-03 | 2026-11-03 | carrot, green chilli, banana - green, brinjal |
| **Chavassery VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Cheeka APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Chelakkara Market** | 24 | 2026-11-03 | 2026-11-03 | elephant yam(suran)/amorphophallus, pumpkin, tomato, tapioca |
| **Chengalpet(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | pumpkin, garlic, banana - green, tapioca |
| **Chengam(Uzhavar Sandhai )** | 46 | 2026-11-03 | 2026-11-03 | pumpkin, banana - green, cabbage, cucumbar(kheera) |
| **Chengannur Market** | 8 | 2026-11-03 | 2026-11-03 | brinjal, beetroot, bhindi(ladies finger), ashgourd |
| **Chennithala VFPCK Market** | 2 | 2026-11-03 | 2026-11-03 | coconut seed, bitter gourd |
| **Cherial APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Cheriyanadu  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana - green |
| **Cherthala Market** | 16 | 2026-11-03 | 2026-11-03 | beetroot, cowpea(veg), onion, amaranthus |
| **Chevella APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Cheyyar(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | papaya, bottle gourd, brinjal, cluster beans |
| **Chhachrauli APMC** | 10 | 2026-11-03 | 2026-11-03 | cauliflower, raddish, spinach, onion |
| **Chhapiheda APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, soyabean, wheat, lentil(masur)(whole) |
| **Chhapra APMC** | 2 | 2026-11-03 | 2026-11-03 | potato, onion |
| **Chhatarpur APMC** | 7 | 2026-11-03 | 2026-11-03 | mustard, soyabean, sesamum(sesame,gingelly,til), black gram(urd beans)(whole) |
| **Chhindwara APMC** | 4 | 2026-11-03 | 2026-11-03 | paddy(common), maize, wheat, soyabean |
| **Chhpara APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Chidambaram(Uzhavar Sandhai )** | 10 | 2026-11-03 | 2026-11-03 | banana, onion, brinjal, tomato |
| **Chikkaballapur** | 98 | 2026-10-13 | 2026-11-12 | bajra, barley, jowar, maize |
| **Chinnalapatti(Uzhavar Sandhai )** | 35 | 2026-11-03 | 2026-11-03 | pumpkin, cluster beans, green chilli, ginger(green) |
| **Chinnamanur(Uzhavar Sandhai )** | 41 | 2026-11-03 | 2026-11-03 | papaya, cluster beans, bitter gourd, bottle gourd |
| **Chintapally APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Chipurupalli APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Chirala APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Chittoor APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **Chodavaram APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), cashewnuts |
| **Chogawan APMC** | 1 | 2026-11-03 | 2026-11-03 | bitter gourd |
| **Chokkikulam(Uzhavar Sandhai )** | 59 | 2026-11-03 | 2026-11-03 | banana, cauliflower, apple, orange |
| **Choppadandi APMC** | 5 | 2026-11-03 | 2026-11-03 | paddy(common), green gram(moong)(whole), cotton, paddy(fine/superfine/grade a) |
| **Chotila APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, cotton, groundnut, soyabean |
| **Choumahla APMC** | 4 | 2026-11-03 | 2026-11-03 | soyabean, groundnut, maize, wheat |
| **Chuliaposi APMC** | 1 | 2026-11-03 | 2026-11-03 | goat |
| **Chungathara VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Coonoor(Uzhavar Sandhai )** | 41 | 2026-11-03 | 2026-11-03 | coriander(leaves), amaranthus, beans, thondekai |
| **Cuddalore(Uzhavar Sandhai )** | 42 | 2026-11-03 | 2026-11-03 | papaya, pumpkin, carrot, chow chow |
| **Cumbum APMC** | 2 | 2026-11-03 | 2026-11-03 | cotton, bengal gram(gram)(whole) |
| **Dabra APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dag APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, soyabean |
| **Dahod APMC** | 11 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), paddy(fine/superfine/grade a), dry chillies, rice |
| **Dahod(Veg. Market) APMC** | 32 | 2026-11-03 | 2026-11-03 | bitter gourd, carrot, cowpea(veg), elephant yam(suran)/amorphophallus |
| **Daloda APMC** | 10 | 2026-11-03 | 2026-11-03 | soyabean, garlic, wheat, lentil(masur)(whole) |
| **Dammapet APMC** | 2 | 2026-11-03 | 2026-11-03 | wood, paddy(fine/superfine/grade a) |
| **Damnagar APMC** | 11 | 2026-11-03 | 2026-11-03 | lemon, brinjal, cauliflower, cabbage |
| **Damoh APMC** | 15 | 2026-11-03 | 2026-11-03 | maize, garlic, green peas, sesamum(sesame,gingelly,til) |
| **Darjeeling APMC** | 6 | 2026-11-03 | 2026-11-03 | tomato, ginger(green), squash(chappal kadoo), potato |
| **Dasda APMC** | 4 | 2026-11-03 | 2026-11-03 | onion, potato, brinjal, rice |
| **Dasuya APMC** | 15 | 2026-11-03 | 2026-11-03 | field pea, garlic, ginger(green), apple |
| **Dataganj APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Datia APMC** | 4 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), groundnut, wheat, paddy(common) |
| **Daunagar APMC** | 5 | 2026-11-03 | 2026-11-03 | garlic, potato, brinjal, bottle gourd |
| **Davgadbaria(Piplod) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Deesa APMC** | 8 | 2026-11-03 | 2026-11-03 | wheat, guar seed(cluster beans seed), castor seed, mustard |
| **Deesa(Deesa Veg Yard) APMC** | 25 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), ginger(green), apple, mousambi(sweet lime) |
| **Dehgam APMC** | 4 | 2026-11-03 | 2026-11-03 | castor seed, paddy(common), wheat, bajra(pearl millet/cumbu) |
| **Dehgam(Rekhiyal) APMC** | 4 | 2026-11-03 | 2026-11-03 | castor seed, wheat, paddy(common), bajra(pearl millet/cumbu) |
| **Dehradoon APMC** | 17 | 2026-11-03 | 2026-11-03 | apple, pineapple, potato, cabbage |
| **Dehri APMC** | 4 | 2026-11-03 | 2026-11-03 | potato, brinjal, tomato, onion |
| **Denduluru APMC** | 1 | 2026-11-03 | 2026-11-03 | lemon |
| **Denkanikottai(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | thondekai, green avare(w), drumstick, cauliflower |
| **Deogarh APMC** | 10 | 2026-11-03 | 2026-11-03 | cabbage, cauliflower, bhindi(ladies finger), brinjal |
| **Deori APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, bengal gram(gram)(whole), maize, buttery |
| **Dera Baba Nanak APMC** | 3 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, cucumbar(kheera) |
| **Dera Bassi APMC** | 5 | 2026-11-03 | 2026-11-03 | bottle gourd, tomato, onion, cauliflower |
| **Deulgaon Raja Balaji Agro Marketing Pvt Market, Deulgaon Raja, Dist Buldhana** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Devakottai (Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | pumpkin, bottle gourd, bitter gourd, elephant yam(suran)/amorphophallus |
| **Devandranagar APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Devarakadra APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Devaram(Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | banana, brinjal, amaranthus, snakeguard |
| **Devgadhbaria APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dewas APMC** | 10 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), maize, bengal gram(gram)(whole), kabuli chana(chickpeas-white) |
| **Dewas(F&V) APMC** | 9 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), potato, cauliflower, cabbage |
| **Dhamnod APMC** | 7 | 2026-11-03 | 2026-11-03 | cotton, kabuli chana(chickpeas-white), wheat, chili red |
| **Dhanaula APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dhanaura APMC** | 5 | 2026-11-03 | 2026-11-03 | cauliflower, carrot, papaya(raw), bottle gourd |
| **Dhand APMC** | 5 | 2026-11-03 | 2026-11-03 | banana, tomato, apple, onion |
| **Dhandhuka APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Dhanera APMC** | 17 | 2026-11-03 | 2026-11-03 | isabgul(psyllium), green gram(moong)(whole), mataki, bajra(pearl millet/cumbu) |
| **Dhanora APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Dhansura APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Dhar APMC** | 7 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), bengal gram(gram)(whole), kabuli chana(chickpeas-white), wheat |
| **Dhar(F&V) APMC** | 6 | 2026-11-03 | 2026-11-03 | apple, carrot, cauliflower, pea pod/pea cod/हरी मटर |
| **Dharamjaygarh APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dharapuram(Uzhavar Sandhai )** | 36 | 2026-11-03 | 2026-11-03 | brinjal, cluster beans, ashgourd, banana - green |
| **Dhari APMC** | 6 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), groundnut, soyabean, wheat |
| **Dhariwal APMC** | 6 | 2026-11-03 | 2026-11-03 | cauliflower, onion, bhindi(ladies finger), green chilli |
| **Dharmapuri(Uzhavar Sandhai )** | 53 | 2026-11-03 | 2026-11-03 | potato, pumpkin, cowpea(veg), beans |
| **Dharmaram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Dharmavaram APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), groundnut |
| **Dhenkanal APMC** | 11 | 2026-11-03 | 2026-11-03 | pointed gourd(parval), tomato, green chilli, brinjal |
| **Dhone APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Dhoraji APMC** | 6 | 2026-11-03 | 2026-11-03 | ground nut seed, cotton, black gram(urd beans)(whole), wheat |
| **Dhragradhra APMC** | 10 | 2026-11-03 | 2026-11-03 | cotton, cummin seed(jeera), groundnut, soanf |
| **Dhrol APMC** | 5 | 2026-11-03 | 2026-11-03 | groundnut, cotton, sesamum(sesame,gingelly,til), wheat |
| **Dhupguri APMC** | 7 | 2026-11-03 | 2026-11-03 | squash(chappal kadoo), green chilli, onion, cauliflower |
| **Dhuri APMC** | 6 | 2026-11-03 | 2026-11-03 | onion, banana, tomato, cauliflower |
| **Digapahandi APMC** | 3 | 2026-11-03 | 2026-11-03 | cabbage, pumpkin, bitter gourd |
| **Diglipur Vegetable Market (Subhashgram)** | 20 | 2026-11-03 | 2026-11-03 | bitter gourd, brinjal, banana, ginger(green) |
| **Dimapur APMC** | 7 | 2026-11-03 | 2026-11-03 | brinjal, leafy vegetable, beans, bhindi(ladies finger) |
| **Dinanagar APMC** | 12 | 2026-11-03 | 2026-11-03 | cauliflower, bottle gourd, brinjal, paddy(basmati) |
| **Dindigul(Uzhavar Sandhai )** | 45 | 2026-11-03 | 2026-11-03 | soyabean, bhindi(ladies finger), coconut, drumstick |
| **Dindori APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, paddy(common), wheat, mustard |
| **Ding APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Dinhata APMC** | 4 | 2026-11-03 | 2026-11-03 | brinjal, jute, potato, rice |
| **Divi (HQ-Avanigadda) APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), black gram(urd beans)(whole) |
| **Diyodar APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, castor seed, mustard, bajra(pearl millet/cumbu) |
| **Dondi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dondilohara APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Doraha APMC** | 18 | 2026-11-03 | 2026-11-03 | tomato, cauliflower, brinjal, onion |
| **Dubbak APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Dudhansadhan APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dudhawa APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Dumal APMC** | 1 | 2026-11-03 | 2026-11-03 | betal leaves |
| **Dungarpur APMC** | 1 | 2026-11-03 | 2026-11-03 | coriander(leaves) |
| **Dungurapalli APMC** | 11 | 2026-11-03 | 2026-11-03 | bitter gourd, potato, brinjal, cabbage |
| **Durg APMC** | 39 | 2026-11-03 | 2026-11-03 | orange, chikoos(sapota), bhindi(ladies finger), knool khol |
| **Durgapur APMC** | 10 | 2026-11-03 | 2026-11-03 | potato, mustard oil, tomato, onion |
| **Durgi APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, paddy(common), cotton, red gram split/arhar dal/tur dal |
| **Edackattuvayal  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | pineapple |
| **Edapadi (Uzhavar Sandhai )** | 36 | 2026-11-03 | 2026-11-03 | coriander(leaves), amaranthus, cabbage, capsicum |
| **Edathwa VFPCK Market** | 2 | 2026-11-03 | 2026-11-03 | banana - green, coconut seed |
| **Elamad  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Elamkulam VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Elampillai(Uzhavar Sandhai )** | 44 | 2026-11-03 | 2026-11-03 | garlic, mousambi(sweet lime), ashgourd, ginger(green) |
| **Elanad  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | cowpea(veg) |
| **Elevancheri VFPCK Market** | 2 | 2026-11-03 | 2026-11-03 | cowpea(veg), snakeguard |
| **Ellanabad APMC** | 4 | 2026-11-03 | 2026-11-03 | cotton, guar, mustard, bengal gram(gram)(whole) |
| **Eluru APMC** | 1 | 2026-11-03 | 2026-11-03 | lemon |
| **Ernakulam Market** | 7 | 2026-11-03 | 2026-11-03 | ashgourd, tomato, banana, tapioca |
| **Errattayar VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | cowpea(veg) |
| **Etcherla APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(fine/superfine/grade a) |
| **Ettumanoor Market** | 21 | 2026-11-03 | 2026-11-03 | bitter gourd, mango(raw-ripe), little gourd(kundru), ashgourd |
| **F.G.Churian APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, onion, tomato, raddish |
| **Fancy Bazaar APMC** | 10 | 2026-11-03 | 2026-11-03 | rice(fine/superfine/grade a), lentil(masur)(whole), green gram dal(moong dal), red gram split/arhar dal/tur dal |
| **Faridabad APMC** | 14 | 2026-11-03 | 2026-11-03 | orange, brinjal, tinda, pea pod/pea cod/हरी मटर |
| **Farukh Nagar APMC** | 3 | 2026-11-03 | 2026-11-03 | tomato, onion, potato |
| **Fatehabad APMC** | 15 | 2026-11-03 | 2026-11-03 | onion, chikoos(sapota), water melon, tomato |
| **Fatehpur APMC** | 1 | 2026-11-03 | 2026-11-03 | cowpea(lobia/karamani) |
| **Flower Market,Gazipur APMC** | 8 | 2026-11-03 | 2026-11-03 | rose(local), tube rose(single), marigold(loose), marigold(calcutta) |
| **Fruit and Vegetable Market Udhampur** | 15 | 2026-11-03 | 2026-11-03 | indian beans(seam), papaya, apple, banana |
| **Gadakota APMC** | 9 | 2026-11-03 | 2026-11-03 | maize, mustard, bengal gram(gram)(whole), black gram(urd beans)(whole) |
| **Gadarpur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Gadarwada APMC** | 7 | 2026-11-03 | 2026-11-03 | paddy(common), green gram(moong)(whole), wheat, soyabean |
| **Gaddiannaram APMC** | 21 | 2026-11-03 | 2026-11-03 | ber(zizyphus/borehannu), avocado, grapes, litchi |
| **Gadwal APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), castor seed, groundnut |
| **Gairatganj APMC** | 10 | 2026-11-03 | 2026-11-03 | wheat, lak(teora), buttery, maize |
| **Gajapathinagaram APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Gajol APMC** | 3 | 2026-11-03 | 2026-11-03 | rice, onion, potato |
| **Gajsinghpur APMC** | 5 | 2026-11-03 | 2026-11-03 | cotton, guar, mustard, green gram(moong)(whole) |
| **Gajwel APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Gamhari APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Ganaur APMC** | 26 | 2026-11-03 | 2026-11-03 | green chilli, pumpkin, onion, mousambi(sweet lime) |
| **Gandai APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Gandarvakottai(Uzhavar Sandhai )** | 26 | 2026-11-03 | 2026-11-03 | banana, ashgourd, bhindi(ladies finger), amaranthus |
| **Gandhigramam(Uzhavar Sandhai)** | 42 | 2026-11-03 | 2026-11-03 | banana, cauliflower, coriander(leaves), cowpea(veg) |
| **Gandhwani APMC** | 4 | 2026-11-03 | 2026-11-03 | soyabean, cotton, maize, wheat |
| **Gangadhara APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Gangapur City APMC** | 4 | 2026-11-03 | 2026-11-03 | mustard, wheat, sesamum(sesame,gingelly,til), bajra(pearl millet/cumbu) |
| **Gangarampur(Dakshin Dinajpur) APMC** | 11 | 2026-11-03 | 2026-11-03 | cauliflower, raddish, tomato, brinjal |
| **Ganjbasoda APMC** | 10 | 2026-11-03 | 2026-11-03 | wheat, lentil(masur)(whole), mustard, bengal gram(gram)(whole) |
| **Gannavaram APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), black gram(urd beans)(whole) |
| **Garbeta(Medinipur) APMC** | 9 | 2026-11-03 | 2026-11-03 | onion, green chilli, bhindi(ladies finger), ridge gourd(permal/hybrid gourd) |
| **Garh Shankar APMC** | 21 | 2026-11-03 | 2026-11-03 | ginger(dry), spinach, garlic, paddy(common) |
| **GarhShankar (Kotfatuhi) APMC** | 8 | 2026-11-03 | 2026-11-03 | spinach, onion, banana, potato |
| **Garoth APMC** | 9 | 2026-11-03 | 2026-11-03 | soyabean, maize, lentil(masur)(whole), methi seeds |
| **Garoth(F&V) APMC** | 2 | 2026-11-03 | 2026-11-03 | tomato, ladies finger |
| **Garudeshwal APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Gautampura APMC** | 3 | 2026-11-03 | 2026-11-03 | onion, wheat, soyabean |
| **Ghansour APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, green peas, buttery |
| **Ghantsala (HQ-Kodali) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Gharaunda APMC** | 5 | 2026-11-03 | 2026-11-03 | tomato, apple, onion, potato |
| **Gharsana APMC** | 3 | 2026-11-03 | 2026-11-03 | mustard, cotton, green gram(moong)(whole) |
| **Ghatal APMC** | 11 | 2026-11-03 | 2026-11-03 | paddy(common), rice, brinjal, green chilli |
| **Gingee(Uzhavar Sandhai )** | 40 | 2026-11-03 | 2026-11-03 | potato, cluster beans, bitter gourd, green chilli |
| **Gobichettipalayam(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | brinjal, coriander(leaves), bitter gourd, tapioca |
| **Godbhaga APMC** | 7 | 2026-11-03 | 2026-11-03 | bottle gourd, tomato, ridge gourd(permal/hybrid gourd), bhindi(ladies finger) |
| **Gogamba APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(common) |
| **Gogamba(Similiya) APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), maize |
| **Gohad APMC** | 6 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), sesamum(sesame,gingelly,til), paddy(common), mustard |
| **Gohana APMC** | 20 | 2026-11-03 | 2026-11-03 | tinda, orange, carrot, brinjal |
| **Gondal(Veg.market Gondal) APMC** | 22 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), tomato, banana, pomegranate |
| **Gondatwisa APMC** | 9 | 2026-11-03 | 2026-11-03 | onion, bitter gourd, brinjal, green chilli |
| **Gooti APMC** | 3 | 2026-11-03 | 2026-11-03 | groundnut, red gram/arhar/tur(whole), cotton |
| **Gorakhpur APMC** | 6 | 2026-11-03 | 2026-11-03 | mustard, kodo millet(varagu), lak(teora), maize |
| **Gorantla  APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Goraya APMC** | 12 | 2026-11-03 | 2026-11-03 | spinach, potato, bhindi(ladies finger), tomato |
| **Gosala APMC** | 2 | 2026-11-03 | 2026-11-03 | raddish, pumpkin |
| **Gotegaon APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, wheat |
| **Gudalur(Uzhavar Sandhai )** | 35 | 2026-11-03 | 2026-11-03 | bitter gourd, ginger(green), drumstick, cucumbar(kheera) |
| **Gudimalkapur APMC** | 25 | 2026-11-03 | 2026-11-03 | onion, carrot, field pea, banana - green |
| **Gudiyatham(Uzhavar Sandhai )** | 48 | 2026-11-03 | 2026-11-03 | onion, banana, ashgourd, tomato |
| **Gudlavalleru APMC** | 1 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal) |
| **Gudur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Guduvancheri(Uzhavar Sandhai )** | 36 | 2026-11-03 | 2026-11-03 | banana, onion, brinjal, amaranthus |
| **Gulabganj APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Gulavati APMC** | 10 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), bottle gourd, colacasia, brinjal |
| **Guna APMC** | 11 | 2026-11-03 | 2026-11-03 | wheat, black gram(urd beans)(whole), maize, mustard |
| **Gunpur APMC** | 8 | 2026-11-03 | 2026-11-03 | cauliflower, carrot, tomato, cabbage |
| **Guntakal APMC** | 3 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), groundnut, bengal gram(gram)(whole) |
| **Guntur APMC** | 1 | 2026-11-03 | 2026-11-03 | dry chillies |
| **Guramkonda Sub-yard of AMC Valmikipuram** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Gurazala APMC** | 1 | 2026-11-03 | 2026-11-03 | chili red |
| **Gurdaspur APMC** | 22 | 2026-11-03 | 2026-11-03 | apple, coriander(leaves), cucumbar(kheera), guava |
| **Gurgaon APMC** | 12 | 2026-11-03 | 2026-11-03 | carrot, onion, bitter gourd, banana |
| **Gurur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Guskara APMC** | 4 | 2026-11-03 | 2026-11-03 | rice(fine/superfine/grade a), mustard, potato, brinjal |
| **Haatpipliya APMC** | 4 | 2026-11-03 | 2026-11-03 | soyabean, maize, wheat, bengal gram(gram)(whole) |
| **Habra APMC** | 9 | 2026-11-03 | 2026-11-03 | bitter gourd, masur dal, green chilli, onion |
| **Hadad     APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Hajipur APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Haldibari APMC** | 4 | 2026-11-03 | 2026-11-03 | brinjal, jute, rice, potato |
| **Haldwani APMC** | 10 | 2026-11-03 | 2026-11-03 | apple, potato, onion, tomato |
| **Hansi APMC** | 37 | 2026-11-03 | 2026-11-03 | mango, apple, grapes, mousambi(sweet lime) |
| **Hanumana(F&V) APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Harbartganj Daily Market APMC** | 10 | 2026-11-03 | 2026-11-03 | raddish, green chilli, pumpkin, onion |
| **Harda APMC** | 8 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), black gram(urd beans)(whole), bengal gram(gram)(whole), maize |
| **Harda(F&V) APMC** | 17 | 2026-11-03 | 2026-11-03 | onion, cabbage, spinach, pineapple |
| **Haridwar Union APMC** | 18 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), brinjal, pumpkin, onion |
| **Harike APMC** | 2 | 2026-11-03 | 2026-11-03 | leafy vegetable, carrot |
| **Harippad Market** | 11 | 2026-11-03 | 2026-11-03 | ashgourd, beetroot, cabbage, bottle gourd |
| **Harnaut APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, apple, tomato, onion |
| **Harpalpur APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Harsood APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, soyabean, wheat, green gram(moong)(whole) |
| **Harur(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | ginger(green), carrot, papaya, bhindi(ladies finger) |
| **Hasanpur APMC** | 15 | 2026-11-03 | 2026-11-03 | banana - green, bhindi(ladies finger), carrot, cauliflower |
| **Hasthampatti(Uzhavar Sandhai )** | 57 | 2026-11-03 | 2026-11-03 | banana, onion, orange, bhindi(ladies finger) |
| **Hata APMC** | 2 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), wheat |
| **Himatnagar APMC** | 10 | 2026-11-03 | 2026-11-03 | maize, sesamum(sesame,gingelly,til), black gram(urd beans)(whole), green gram(moong)(whole) |
| **Himatnagar(Veg.Market Himatnagar) APMC** | 16 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), guar, cucumbar(kheera), bitter gourd |
| **Hindol APMC** | 10 | 2026-11-03 | 2026-11-03 | banana - green, brinjal, drumstick, tomato |
| **Hindupur APMC** | 2 | 2026-11-03 | 2026-11-03 | tamarind fruit, dry chillies |
| **Hinjilicut APMC** | 4 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), papaya(raw), pumpkin, cucumbar(kheera) |
| **Hiramandalam APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(common) |
| **Hissar APMC** | 4 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), groundnut, bajra(pearl millet/cumbu), cotton |
| **Hodal APMC** | 4 | 2026-11-03 | 2026-11-03 | tomato, potato, carrot, onion |
| **Hosur(Uzhavar Sandhai )** | 64 | 2026-11-03 | 2026-11-03 | grapes, garlic, brinjal, orange |
| **Husnabad APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Huzurnagar APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Huzzurabad APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Iamailabad APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Ibrahimpatnam APMC** | 4 | 2026-11-03 | 2026-11-03 | green chilli, brinjal, tomato, bhindi(ladies finger) |
| **Ichapuram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Ichhawar APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, bengal gram(gram)(whole), soyabean, wheat |
| **Idar APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, groundnut, wheat, castor seed |
| **Idar(Jadar) APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Iklera APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, maize, soyabean, mustard |
| **Imphal APMC** | 12 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal), onion, masur dal, paddy(common) |
| **Inchakkad VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Indore APMC** | 16 | 2026-11-03 | 2026-11-03 | chili red, garlic, bengal gram(gram)(whole), green peas |
| **Indore(F&V) APMC** | 27 | 2026-11-03 | 2026-11-03 | capsicum, chikoos(sapota), ginger(green), carrot |
| **Indus(Bankura Sadar) APMC** | 6 | 2026-11-03 | 2026-11-03 | rice(fine/superfine/grade a), sweet pumpkin, brinjal, paddy(fine/superfine/grade a) |
| **Ipur APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Isagarh APMC** | 2 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), maize |
| **Itarsi APMC** | 7 | 2026-11-03 | 2026-11-03 | paddy(common), maize, soyabean, bengal gram(gram)(whole) |
| **Itarsi(F&V) APMC** | 8 | 2026-11-03 | 2026-11-03 | cauliflower, potato, green chilli, cabbage |
| **JASDAN APMC** | 19 | 2026-11-03 | 2026-11-03 | ground nut seed, maize, black gram(urd beans)(whole), cummin seed(jeera) |
| **Jabalpur APMC** | 14 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), maize, red gram/arhar/tur(whole), paddy(common) |
| **Jagadhri APMC** | 18 | 2026-11-03 | 2026-11-03 | green chilli, potato, onion, tomato |
| **Jagatsinghpur APMC** | 2 | 2026-11-03 | 2026-11-03 | brinjal, potato |
| **Jagdalpur APMC** | 1 | 2026-11-03 | 2026-11-03 | mahua |
| **Jagdamba Agrocare Pvt Ltd, Pandharkawada, Dist Yeotmal** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Jaggampet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jaggayyapeta APMC** | 1 | 2026-11-03 | 2026-11-03 | wood |
| **Jagraon APMC** | 21 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), orange, ginger(green), pea pod/pea cod/हरी मटर |
| **Jagtial APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), paddy(common), maize |
| **Jainagar APMC** | 7 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), bottle gourd, bitter gourd, green chilli |
| **Jaisalmer APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Jaisinagar APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Jaitu APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jaitu(Bajakhana) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jalagandapuram(Uzhavar Sandhai )** | 45 | 2026-11-03 | 2026-11-03 | onion, tomato, groundnut, green chilli |
| **Jalalabad APMC** | 29 | 2026-11-03 | 2026-11-03 | papaya, cabbage, onion, cauliflower |
| **Jalandhar Cantt (Jamshedpur Dana Mandi) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jalandhar Cantt. APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jalandhar City APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jalandhar City(Jalandhar) APMC** | 39 | 2026-11-03 | 2026-11-03 | ginger(green), lemon, onion, peas wet |
| **Jalandhar City(Kartar Pur Dana mandi) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Jaleswar APMC** | 7 | 2026-11-03 | 2026-11-03 | bitter gourd, papaya(raw), bhindi(ladies finger), ridgeguard(tori) |
| **Jalgaon(Masawat)** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Jalore APMC** | 14 | 2026-11-03 | 2026-11-03 | brinjal, onion green, coriander(leaves), cauliflower |
| **Jalpaiguri Sadar APMC** | 7 | 2026-11-03 | 2026-11-03 | bitter gourd, brinjal, garlic, potato |
| **Jalumuru APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Jam Jodhpur APMC** | 10 | 2026-11-03 | 2026-11-03 | wheat, cotton, castor seed, black gram(urd beans)(whole) |
| **Jam Khambalia APMC** | 7 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), wheat, bengal gram(gram)(whole), ground nut seed |
| **Jameenrayapettai(Uzhavar Sandhai )** | 54 | 2026-11-03 | 2026-11-03 | papaya, bitter gourd, apple, cowpea(veg) |
| **Jammalamadugu APMC** | 2 | 2026-11-03 | 2026-11-03 | jowar(sorghum), bengal gram(gram)(whole) |
| **Jammikunta APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Jamnagar APMC** | 17 | 2026-11-03 | 2026-11-03 | castor seed, bajra(pearl millet/cumbu), cotton, soyabean |
| **Jamner(Neri)** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Jampuijala APMC** | 5 | 2026-11-03 | 2026-11-03 | ginger(green), potato, green chilli, onion |
| **Jamui APMC** | 4 | 2026-11-03 | 2026-11-03 | green chilli, tomato, cauliflower, brinjal |
| **Jangipur APMC** | 9 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), garlic, onion |
| **Jaora APMC** | 22 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), maize, wheat, groundnut |
| **Jasdan(Vichhiya) APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Jasvantnagar APMC** | 5 | 2026-11-03 | 2026-11-03 | bottle gourd, bhindi(ladies finger), brinjal, bitter gourd |
| **Jatara APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Jatni APMC** | 9 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, tomato, papaya(raw) |
| **Javad APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, wheat |
| **Javera APMC** | 3 | 2026-11-03 | 2026-11-03 | gudmar, maize, wheat |
| **Jawar APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, maize, bengal gram(gram)(whole), soyabean |
| **Jeerapur APMC** | 5 | 2026-11-03 | 2026-11-03 | soyabean, jowar(sorghum), black gram(urd beans)(whole), wheat |
| **Jetpur(Dist.Rajkot) APMC** | 13 | 2026-11-03 | 2026-11-03 | wheat, soyabean, black gram(urd beans)(whole), bengal gram(gram)(whole) |
| **Jeyankondam (Uzhavar Sandhai )** | 7 | 2026-11-03 | 2026-11-03 | raddish, onion, tomato, bhindi(ladies finger) |
| **Jhabua APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, cotton, soyabean |
| **Jhajjar APMC** | 6 | 2026-11-03 | 2026-11-03 | tomato, apple, onion, raddish |
| **Jhalod APMC** | 5 | 2026-11-03 | 2026-11-03 | maize, soyabean, wheat, paddy(common) |
| **Jharsuguda APMC** | 4 | 2026-11-03 | 2026-11-03 | onion, ginger(green), tomato, potato |
| **Jobat APMC** | 6 | 2026-11-03 | 2026-11-03 | soyabean, maize, wheat, bengal gram(gram)(whole) |
| **Jora APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Jowai APMC** | 8 | 2026-11-03 | 2026-11-03 | onion, brinjal, cabbage, potato |
| **Junagarh APMC** | 5 | 2026-11-03 | 2026-11-03 | cauliflower, cabbage, green chilli, tomato |
| **Junnar(Alephata)** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Junnar(Otur)** | 15 | 2026-11-03 | 2026-11-03 | beetroot, bhindi(ladies finger), bottle gourd, little gourd(kundru) |
| **KALANWALIAPMC** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **KISAN MARKET YARD** | 4 | 2026-11-03 | 2026-11-03 | soyabean, cotton, wheat, red gram/arhar/tur(whole) |
| **KKNagar(Uzhavar Sandhai )** | 61 | 2026-11-03 | 2026-11-03 | potato, cauliflower, papaya, banana |
| **KRISHI UPAJ MANDI SAMITI (APMC) KANKER** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kadakkal  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Kadambazhi puram  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Kadapa** | 2 | 2026-11-03 | 2026-11-03 | groundnut, turmeric |
| **Kadi APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), castor seed, bajra(pearl millet/cumbu) |
| **Kadi(Kadi cotton Yard) APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Kadiri APMC** | 1 | 2026-11-03 | 2026-11-03 | tamarind fruit |
| **Kadukutty VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Kagaznagar APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), cotton |
| **Kahithapattarai(Uzhavar Sandhai )** | 55 | 2026-11-03 | 2026-11-03 | coriander(leaves), groundnut, cowpea(veg), green chilli |
| **Kahnuwan APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kailaras APMC** | 21 | 2026-11-03 | 2026-11-03 | bottle gourd, chili red, ginger(dry), mustard |
| **Kairana APMC** | 13 | 2026-11-03 | 2026-11-03 | cabbage, pumpkin, carrot, guava |
| **Kakching Market APMC** | 12 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), ginger(green), onion, bengal gram dal(chana dal) |
| **Kakinada (Urban) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kalahandi(Dharamagarh) APMC** | 5 | 2026-11-03 | 2026-11-03 | tomato, cabbage, green chilli, brinjal |
| **Kalanaur APMC** | 3 | 2026-11-03 | 2026-11-03 | carrot, raddish, brinjal |
| **Kalapipal APMC** | 7 | 2026-11-03 | 2026-11-03 | soyabean, lentil(masur)(whole), onion, wheat |
| **Kalapipal(F&V) APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, garlic |
| **Kalawad APMC** | 5 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), wheat, black gram(urd beans)(whole), cummin seed(jeera) |
| **Kalawali(Odhan) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kalediya APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Kalidindi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kalikiri APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Kallachi Market** | 23 | 2026-11-03 | 2026-11-03 | ashgourd, cabbage, beetroot, bhindi(ladies finger) |
| **Kallakurichi(Uzhavar Sandhai )** | 46 | 2026-11-03 | 2026-11-03 | coriander(leaves), groundnut, ashgourd, bhindi(ladies finger) |
| **Kallur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kalna APMC** | 9 | 2026-11-03 | 2026-11-03 | green chilli, sweet pumpkin, tomato, brinjal |
| **Kalpetta Market** | 12 | 2026-11-03 | 2026-11-03 | brinjal, snakeguard, pumpkin, bhindi(ladies finger) |
| **Kalsi APMC** | 2 | 2026-11-03 | 2026-11-03 | cabbage, ginger(green) |
| **Kalyandurg APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Kalyanpur APMC** | 7 | 2026-11-03 | 2026-11-03 | tomato, cabbage, cucumbar(kheera), potato |
| **Kamakhyanagar APMC** | 12 | 2026-11-03 | 2026-11-03 | cauliflower, tomato, bitter gourd, brinjal |
| **Kamakshi VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | bitter gourd |
| **Kamalapur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Kamalapuram APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), groundnut |
| **Kamalghat** | 7 | 2026-11-03 | 2026-11-03 | green chilli, papaya(raw), cucumbar(kheera), cabbage |
| **Kambam(Uzhavar Sandhai )** | 43 | 2026-11-03 | 2026-11-03 | banana, brinjal, papaya, banana - green |
| **Kamuthi(Uzhavar Sandhai )** | 7 | 2026-11-03 | 2026-11-03 | coriander(leaves), brinjal, green chilli, mint(pudina) |
| **Kancheepuram(Uzhavar Sandhai )** | 26 | 2026-11-03 | 2026-11-03 | onion, bottle gourd, bhindi(ladies finger), snakeguard |
| **Kanchekacherla APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Kanchili APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kandhamal APMC** | 1 | 2026-11-03 | 2026-11-03 | brinjal |
| **Kandiyaperi(Uzhavar Sandhai )** | 11 | 2026-11-03 | 2026-11-03 | tomato, coconut, ashgourd, coriander(leaves) |
| **Kandukur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kangayam(Uzhavar Sandhai )** | 27 | 2026-11-03 | 2026-11-03 | banana, cauliflower, tomato, bottle gourd |
| **Kanigiri APMC** | 1 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole) |
| **Kanjoor VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Kankwal Chahlan APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Kannakunnu VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | cowpea(veg) |
| **Kannamangalam  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | amaranthus |
| **Kannod APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, black gram(urd beans)(whole), green gram(moong)(whole), soyabean |
| **Kannur Market** | 7 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), bitter gourd, bhindi(ladies finger), cowpea(veg) |
| **Kantabaji APMC** | 4 | 2026-11-03 | 2026-11-03 | tomato, cauliflower, cabbage, pumpkin |
| **Kapadvanj APMC** | 7 | 2026-11-03 | 2026-11-03 | tomato, onion, cabbage, cauliflower |
| **Kapasan APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Karaikudi(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | tomato, green chilli, snakeguard, potato |
| **Karambakkudi(Uzhavar Sandhai )** | 23 | 2026-11-03 | 2026-11-03 | brinjal, cluster beans, bhindi(ladies finger), green chilli |
| **Karanjia APMC** | 11 | 2026-11-03 | 2026-11-03 | sweet potato, mushroom, cauliflower, rice |
| **Karapa APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Kareli APMC** | 11 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), black gram(urd beans)(whole), gur(jaggery), paddy(common) |
| **Karera APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Karera(F&V) APMC** | 8 | 2026-11-03 | 2026-11-03 | potato, cauliflower, bottle gourd, tomato |
| **Karhi APMC** | 6 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), maize, cotton, soyabean |
| **Karimangalam(Uzhavar Sandhai)** | 41 | 2026-11-03 | 2026-11-03 | onion, brinjal, ginger(green), sweet potato |
| **Karimnagar APMC** | 3 | 2026-11-03 | 2026-11-03 | cotton, paddy(fine/superfine/grade a), maize |
| **Karimpur APMC** | 8 | 2026-11-03 | 2026-11-03 | potato, green chilli, jute, onion |
| **Kariyapatti(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, pumpkin, amaranthus |
| **Karnataka State Average** | 2 | 2026-11-01 | 2026-11-08 | diesel_exogenous |
| **Karsiyang(Matigara) APMC** | 6 | 2026-11-03 | 2026-11-03 | cabbage, carrot, squash(chappal kadoo), potato |
| **Karumaloor VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger) |
| **Karur(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | carrot, cabbage, snakeguard, chow chow |
| **Kasdol APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kashipur APMC** | 27 | 2026-11-03 | 2026-11-03 | bottle gourd, green chilli, ginger(green), bhindi(ladies finger) |
| **Kasinagar APMC** | 2 | 2026-11-03 | 2026-11-03 | seetapal, banana |
| **Kasrawad APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, cotton, wheat |
| **Katangi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kataram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Katghora APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kathua (F&V)** | 31 | 2026-11-03 | 2026-11-03 | apple, guava, pomegranate, ginger(green) |
| **Katni APMC** | 15 | 2026-11-03 | 2026-11-03 | kodo millet(varagu), green gram(moong)(whole), bengal gram(gram)(whole), paddy(common) |
| **Katpadi (Uzhavar Sandhai )** | 56 | 2026-11-03 | 2026-11-03 | banana, pumpkin, cluster beans, grapes |
| **Kattakada Market** | 4 | 2026-11-03 | 2026-11-03 | bitter gourd, amaranthus, colacasia, bottle gourd |
| **Kattakkada  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Kattappana Market** | 5 | 2026-11-03 | 2026-11-03 | apple, pineapple, water melon, banana |
| **Katwa APMC** | 5 | 2026-11-03 | 2026-11-03 | tomato, brinjal, green chilli, potato |
| **Kavali APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kaveripattinam(Uzhavar Sandhai )** | 29 | 2026-11-03 | 2026-11-03 | brinjal, cluster beans, bottle gourd, ashgourd |
| **Kayamkulam Market** | 23 | 2026-11-03 | 2026-11-03 | amaranthus, bhindi(ladies finger), carrot, ginger(green) |
| **Keelpennathur(Uzhavar Sandhai )** | 13 | 2026-11-03 | 2026-11-03 | beans, coconut, tomato, tender coconut |
| **Keerampara VFPCK Market** | 2 | 2026-11-03 | 2026-11-03 | pineapple, banana |
| **Kendupatna APMC** | 1 | 2026-11-03 | 2026-11-03 | pumpkin |
| **Kendupatna(Niali) APMC** | 2 | 2026-11-03 | 2026-11-03 | tomato, banana - green |
| **Keolari APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Keonjhar APMC** | 6 | 2026-11-03 | 2026-11-03 | bottle gourd, tomato, brinjal, bitter gourd |
| **Kesamudram APMC** | 5 | 2026-11-03 | 2026-11-03 | paddy(common), paddy(fine/superfine/grade a), maize, cotton seed |
| **Keshkal APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(common) |
| **Kesinga APMC** | 5 | 2026-11-03 | 2026-11-03 | brinjal, tomato, banana - green, bhindi(ladies finger) |
| **Kesli APMC** | 3 | 2026-11-03 | 2026-11-03 | buttery, wheat, maize |
| **Khachrod APMC** | 4 | 2026-11-03 | 2026-11-03 | soyabean, wheat, bengal gram(gram)(whole), maize |
| **Khairlangi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Khalilabad APMC** | 6 | 2026-11-03 | 2026-11-03 | cauliflower, cucumbar(kheera), pumpkin, potato |
| **Khamano (Sanghol) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Khamano APMC** | 7 | 2026-11-03 | 2026-11-03 | tomato, cauliflower, garlic, capsicum |
| **Khambhat(Veg Yard Khambhat) APMC** | 10 | 2026-11-03 | 2026-11-03 | bottle gourd, green chilli, cauliflower, methi(leaves) |
| **Khandhla APMC** | 13 | 2026-11-03 | 2026-11-03 | guava, bhindi(ladies finger), sponge gourd, bitter gourd |
| **Khandwa APMC** | 9 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), bengal gram(gram)(whole), wheat, mustard |
| **Khandwa(F&V) APMC** | 13 | 2026-11-03 | 2026-11-03 | cabbage, bitter gourd, brinjal, spinach |
| **Khaniadhana APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Khanna APMC** | 21 | 2026-11-03 | 2026-11-03 | raddish, mousambi(sweet lime), tomato, brinjal |
| **Khanpur APMC** | 7 | 2026-11-03 | 2026-11-03 | soyabean, garlic, mustard, bengal gram(gram)(whole) |
| **Kharar APMC** | 10 | 2026-11-03 | 2026-11-03 | carrot, potato, onion, raddish |
| **Khargapur APMC** | 2 | 2026-11-03 | 2026-11-03 | barley(jau), wheat |
| **Khargone APMC** | 7 | 2026-11-03 | 2026-11-03 | maize, soyabean, wheat, cotton |
| **Khariar Road APMC** | 2 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), bitter gourd |
| **Kharkhoda APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, banana, tomato, onion |
| **Khatauli APMC** | 2 | 2026-11-03 | 2026-11-03 | mustard, sesamum(sesame,gingelly,til) |
| **Khateema APMC** | 10 | 2026-11-03 | 2026-11-03 | orange, cucumbar(kheera), onion, bitter gourd |
| **Khategaon APMC** | 10 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), jowar(sorghum), wheat, mustard |
| **Khatora APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, maize |
| **Khatra APMC** | 10 | 2026-11-03 | 2026-11-03 | bottle gourd, mustard, tomato, brinjal |
| **Khed(Chakan)** | 20 | 2026-11-03 | 2026-11-03 | carrot, garlic, drumstick, tomato |
| **Khetia APMC** | 3 | 2026-11-03 | 2026-11-03 | cotton, soyabean, maize |
| **Khilchipur APMC** | 5 | 2026-11-03 | 2026-11-03 | maize, wheat, bengal gram(gram)(whole), lentil(masur)(whole) |
| **Khirkiya APMC** | 6 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), wheat, bengal gram(gram)(whole), soyabean |
| **Khujner APMC** | 6 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), lentil(masur)(whole), wheat, maize |
| **Khurai APMC** | 10 | 2026-11-03 | 2026-11-03 | wheat, soyabean, lentil(masur)(whole), green peas |
| **Khurai(F&V) APMC** | 4 | 2026-11-03 | 2026-11-03 | onion, tomato, potato, brinjal |
| **Kila Raipur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kizhakkancheri VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | little gourd(kundru) |
| **Kodaikkanal(Uzhavar Sandhai)** | 6 | 2026-11-03 | 2026-11-03 | potato, garlic, brinjal, bottle gourd |
| **Kodumur APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Koduvayoor Market** | 35 | 2026-11-03 | 2026-11-03 | cauliflower, coconut, ginger(dry), bitter gourd |
| **Kohima APMC** | 3 | 2026-11-03 | 2026-11-03 | yam(ratalu), potato, pumpkin |
| **Koilkunta APMC** | 1 | 2026-11-03 | 2026-11-03 | jowar(sorghum) |
| **Kolaghat APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, rice(fine/superfine/grade a), marigold(loose), tube rose(loose) |
| **Kolar** | 98 | 2026-10-13 | 2026-11-12 | bajra, barley, jowar, maize |
| **Kolaras APMC** | 8 | 2026-11-03 | 2026-11-03 | groundnut, soyabean, mustard, bengal gram(gram)(whole) |
| **Kolhapur(Laxmipuri)** | 3 | 2026-11-03 | 2026-11-03 | wheat, rice, jowar(sorghum) |
| **Konaraopet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Kondapi APMC** | 1 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole) |
| **Koovapadi VFPCK Market** | 3 | 2026-11-03 | 2026-11-03 | banana, ashgourd, tapioca |
| **Koraput APMC** | 5 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), cabbage, bitter gourd, banana - green |
| **Koraput(Semilguda) APMC** | 5 | 2026-11-03 | 2026-11-03 | brinjal, cucumbar(kheera), cabbage, banana - green |
| **Kosikalan APMC** | 11 | 2026-11-03 | 2026-11-03 | bottle gourd, paddy(basmati), brinjal, tomato |
| **Kosli APMC** | 8 | 2026-11-03 | 2026-11-03 | banana, potato, cauliflower, tomato |
| **Kota (F&V) APMC** | 6 | 2026-11-03 | 2026-11-03 | guava, pomegranate, apple, mousambi(sweet lime) |
| **Kotba APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kothabommali APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kothagudem APMC** | 2 | 2026-11-03 | 2026-11-03 | cotton, paddy(common) |
| **Kotma APMC** | 1 | 2026-11-03 | 2026-11-03 | dried mango |
| **Kottakkal Market** | 5 | 2026-11-03 | 2026-11-03 | amranthas red, beetroot, amaranthus, ashgourd |
| **Kottayam Market** | 20 | 2026-11-03 | 2026-11-03 | rice, cabbage, cluster beans, cowpea(veg) |
| **Kottayi VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | snakeguard |
| **Kovilpatti(Uzhavar Sandhai )** | 40 | 2026-11-03 | 2026-11-03 | banana, chikoos(sapota), bitter gourd, bottle gourd |
| **Kovur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Krishi Upaj Mandi Samiti Bichhiya** | 5 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), maize, green peas |
| **Krishnagiri(Uzhavar Sandhai )** | 48 | 2026-11-03 | 2026-11-03 | banana, cowpea(veg), sweet potato, carrot |
| **Kuchinda APMC** | 6 | 2026-11-03 | 2026-11-03 | banana - green, pumpkin, carrot, cucumbar(kheera) |
| **Kukatpally,RBZ** | 26 | 2026-11-03 | 2026-11-03 | french beans(frasbean), carrot, cauliflower, wild cucumber |
| **Kukshi APMC** | 4 | 2026-11-03 | 2026-11-03 | cotton, wheat, maize, soyabean |
| **Kulithalai(Uzhavar Sandhai )** | 47 | 2026-11-03 | 2026-11-03 | papaya, cluster beans, ashgourd, green chilli |
| **Kumarapalayam(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | banana, tomato, drumstick, lemon |
| **Kumbakonam (Uzhavar Sandhai )** | 42 | 2026-11-03 | 2026-11-03 | garlic, brinjal, coriander(leaves), cluster beans |
| **Kumbakonam RM** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kumbhraj APMC** | 5 | 2026-11-03 | 2026-11-03 | coriander(leaves), soyabean, wheat, bengal gram(gram)(whole) |
| **Kundrathur(Uzhavar Sandhai )** | 25 | 2026-11-03 | 2026-11-03 | potato, banana - green, snakeguard, green avare(w) |
| **Kunjpura APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Kunnukara  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Kuppam APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Kurali APMC** | 24 | 2026-11-03 | 2026-11-03 | paddy(common), cabbage, green chilli, cucumbar(kheera) |
| **Kurawar APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, soyabean, lentil(masur)(whole), mustard |
| **Kurichi(Uzhavar Sandhai )** | 30 | 2026-11-03 | 2026-11-03 | tomato, onion, bhindi(ladies finger), amaranthus |
| **Kurnool APMC** | 9 | 2026-11-03 | 2026-11-03 | groundnut, castor seed, bengal gram(gram)(whole), dry chillies |
| **Kurupam APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Kurwai APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Kuthuparambu Market** | 8 | 2026-11-03 | 2026-11-03 | tomato, banana, green chilli, cucumbar(kheera) |
| **Kutumba APMC** | 5 | 2026-11-03 | 2026-11-03 | onion, raddish, bitter gourd, spinach |
| **Kuzhur  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **L B Nagar APMC** | 20 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), ridgeguard(tori), bitter gourd, cabbage |
| **Lahar APMC** | 8 | 2026-11-03 | 2026-11-03 | jowar(sorghum), black gram(urd beans)(whole), bajra(pearl millet/cumbu), wheat |
| **Lakhisarai APMC** | 7 | 2026-11-03 | 2026-11-03 | wheat, onion, potato, rice |
| **Lakhnadon APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(common) |
| **Lakhtar APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Lakkireddipally APMC** | 1 | 2026-11-03 | 2026-11-03 | ground nut seed |
| **Lakshar APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Lalbagh APMC** | 3 | 2026-11-03 | 2026-11-03 | brinjal, rice, green chilli |
| **Lalganj APMC** | 4 | 2026-11-03 | 2026-11-03 | cauliflower, raddish, bottle gourd, banana - green |
| **Lalgudi(Uzhavar Sandhai )** | 45 | 2026-11-03 | 2026-11-03 | bitter gourd, onion, amaranthus, beans |
| **Lamlong Bazaar APMC** | 11 | 2026-11-03 | 2026-11-03 | banana, bengal gram(gram)(whole), ginger(green), black gram dal(urd dal) |
| **Lasalgaon(Niphad)** | 6 | 2026-11-03 | 2026-11-03 | maize, onion, wheat, green gram(moong)(whole) |
| **Lasalgaon(Vinchur)** | 3 | 2026-11-03 | 2026-11-03 | onion, soyabean, maize |
| **Lashkar APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, mustard, bajra(pearl millet/cumbu), paddy(common) |
| **Lateri APMC** | 4 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), maize, black gram(urd beans)(whole), soyabean |
| **Latur(Murud)** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **LavKush Nagar(Laundi) APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, mustard, bengal gram(gram)(whole), sesamum(sesame,gingelly,til) |
| **Lediyari APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Limkheda APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, paddy(common), wheat |
| **Loharda APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, wheat, soyabean |
| **Lohian Khas APMC** | 7 | 2026-11-03 | 2026-11-03 | turnip, cauliflower, brinjal, spinach |
| **Longleng APMC** | 7 | 2026-11-03 | 2026-11-03 | banana - green, leafy vegetable, yam(ratalu), green chilli |
| **Lunkaransar APMC** | 4 | 2026-11-03 | 2026-11-03 | guar seed(cluster beans seed), groundnut, moath dal, green gram(moong)(whole) |
| **Luxettipet APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), cotton |
| **M/S Kalpana Agri Commodities Marketing, Nagpur** | 4 | 2026-11-03 | 2026-11-03 | soyabean, cotton, bengal gram(gram)(whole), red gram/arhar/tur(whole) |
| **Macharla APMC** | 3 | 2026-11-03 | 2026-11-03 | cotton, red gram/arhar/tur(whole), paddy(fine/superfine/grade a) |
| **Machhiwara APMC** | 9 | 2026-11-03 | 2026-11-03 | ginger(green), bhindi(ladies finger), potato, garlic |
| **Machilipatnam APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Machmara** | 8 | 2026-11-03 | 2026-11-03 | brinjal, green chilli, onion, tomato |
| **Madakasira APMC** | 2 | 2026-11-03 | 2026-11-03 | groundnut, ragi(finger millet) |
| **Madanapalli APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Maddipadu APMC** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), paddy(fine/superfine/grade a), bengal gram(gram)(whole) |
| **Madhuban APMC** | 7 | 2026-11-03 | 2026-11-03 | onion, brinjal, bitter gourd, cabbage |
| **Madhubani APMC** | 6 | 2026-11-03 | 2026-11-03 | onion, brinjal, tomato, bhindi(ladies finger) |
| **Madhuranthagam(Uzhavar Sandhai )** | 22 | 2026-11-03 | 2026-11-03 | tomato, potato, bhindi(ladies finger), amaranthus |
| **Madlauda APMC** | 3 | 2026-11-03 | 2026-11-03 | tomato, onion, potato |
| **Madugula APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), cashewnuts |
| **Madurai RM** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Magroni APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), groundnut, wheat |
| **Mahabubabad APMC** | 5 | 2026-11-03 | 2026-11-03 | groundnut, cotton, maize, paddy(common) |
| **Mahabubnagar(Rythu Bazar)** | 7 | 2026-11-03 | 2026-11-03 | tomato, potato, green chilli, cabbage |
| **Maharjganj APMC** | 7 | 2026-11-03 | 2026-11-03 | cauliflower, onion, sponge gourd, brinjal |
| **Mahboob Manison APMC** | 19 | 2026-11-03 | 2026-11-03 | french beans(frasbean), cucumbar(kheera), beetroot, ginger(green) |
| **Mahbubnagar APMC** | 6 | 2026-11-03 | 2026-11-03 | groundnut, paddy(fine/superfine/grade a), ragi(finger millet), maize |
| **Mahesh Krushi Utpanna Bazar, Digras, Dist Yeotmal** | 2 | 2026-11-03 | 2026-11-03 | wheat, soyabean |
| **Mahidpur APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, green gram(moong)(whole), maize, soyabean |
| **Mahuva(Station Road) APMC** | 11 | 2026-11-03 | 2026-11-03 | onion, green gram(moong)(whole), bengal gram(gram)(whole), black gram(urd beans)(whole) |
| **Maigalganj APMC** | 11 | 2026-11-03 | 2026-11-03 | ridgeguard(tori), banana - green, cabbage, carrot |
| **Maihar APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, kodo millet(varagu) |
| **Maihar(F&V) APMC** | 6 | 2026-11-03 | 2026-11-03 | potato, tomato, bottle gourd, cucumbar(kheera) |
| **Maksi APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Maksudangarh APMC** | 3 | 2026-11-03 | 2026-11-03 | wheat, soyabean, maize |
| **Mala VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Malerkotla APMC** | 29 | 2026-11-03 | 2026-11-03 | raddish, lemon, potato, squash(chappal kadoo) |
| **Malleswaram (HQ-Bantumili) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Malout APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Malpur APMC** | 2 | 2026-11-03 | 2026-11-03 | groundnut, soyabean |
| **Malthone APMC** | 2 | 2026-11-03 | 2026-11-03 | soyabean, wheat |
| **Manachanallur(Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | banana, coriander(leaves), tomato, bottle gourd |
| **Mananthavady Market** | 12 | 2026-11-03 | 2026-11-03 | tapioca, coffee, ashgourd, banana - green |
| **Manapparai(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | onion, papaya, cluster beans, cabbage |
| **Manasa APMC** | 9 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), onion, maize, barley(jau) |
| **Manawar APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, soyabean, cotton, maize |
| **Mandapeta APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Mandawar APMC** | 7 | 2026-11-03 | 2026-11-03 | wheat, dhaincha, bajra(pearl millet/cumbu), sesamum(sesame,gingelly,til) |
| **Mandla APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), wheat, maize |
| **Mandsaur APMC** | 19 | 2026-11-03 | 2026-11-03 | groundnut, basil, black gram(urd beans)(whole), methi seeds |
| **Manendragarh APMC** | 1 | 2026-11-03 | 2026-11-03 | millets |
| **Mangalagiri APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), maize |
| **Manglaur APMC** | 19 | 2026-11-03 | 2026-11-03 | potato, capsicum, onion, pumpkin |
| **Manjeri Market** | 24 | 2026-11-03 | 2026-11-03 | bitter gourd, brinjal, apple, tomato |
| **Manjeswaram Market** | 15 | 2026-11-03 | 2026-11-03 | beetroot, amaranthus, ginger(green), coconut |
| **Mannar Market** | 19 | 2026-11-03 | 2026-11-03 | capsicum, tomato, carrot, pumpkin |
| **Mannargudi I(Uzhavar Sandhai )** | 44 | 2026-11-03 | 2026-11-03 | banana, onion, coriander(leaves), chikoos(sapota) |
| **Mannargudi II(Uzhavar Sandhai )** | 36 | 2026-11-03 | 2026-11-03 | potato, tomato, cluster beans, bhindi(ladies finger) |
| **Mansa APMC** | 33 | 2026-11-03 | 2026-11-03 | castor seed, groundnut(split), black gram(urd beans)(whole), green gram(moong)(whole) |
| **Mansa(Manas Veg Yard) APMC** | 13 | 2026-11-03 | 2026-11-03 | cauliflower, tomato, cabbage, green chilli |
| **Mansura APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Mantralayam APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Mapusa APMC** | 3 | 2026-11-03 | 2026-11-03 | potato, orange, onion |
| **Marapally APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Markapur APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Market Administrative Committee Zazna** | 1 | 2026-11-03 | 2026-11-03 | apple |
| **Masli** | 12 | 2026-11-03 | 2026-11-03 | brinjal, ridgeguard(tori), cow, cauliflower |
| **Mathabhanga APMC** | 4 | 2026-11-03 | 2026-11-03 | brinjal, potato, rice, jute |
| **Mawiong Regulated Market APMC** | 2 | 2026-11-03 | 2026-11-03 | broomstick(flower broom), bay leaf(tejpatta) |
| **Mayabander Vegetable Market** | 21 | 2026-11-03 | 2026-11-03 | tender coconut, coconut, brinjal, papaya(raw) |
| **Mayiladuthurai(Uzhavar Sandhai )** | 29 | 2026-11-03 | 2026-11-03 | onion, cluster beans, bottle gourd, bhindi(ladies finger) |
| **Mazhuvannur VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | elephant yam(suran)/amorphophallus |
| **Mecheri(Uzhavar Sandhai)** | 22 | 2026-11-03 | 2026-11-03 | tomato, amaranthus, coconut, coriander(leaves) |
| **Medavakkam(Uzhavar Sandhai )** | 19 | 2026-11-03 | 2026-11-03 | banana - green, mint(pudina), coriander(leaves), onion |
| **Medinipur(West) APMC** | 16 | 2026-11-03 | 2026-11-03 | bottle gourd, ridgeguard(tori), cucumbar(kheera), potato |
| **Meghraj APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Meghraj(Rellavada) APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Mehal Kalan APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Meham** | 13 | 2026-11-03 | 2026-11-03 | onion, spinach, banana, orange |
| **Mehatpur APMC** | 5 | 2026-11-03 | 2026-11-03 | spinach, sponge gourd, methi(leaves), raddish |
| **Mehgaon APMC** | 1 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu) |
| **Mehsana APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, mustard, castor seed, bajra(pearl millet/cumbu) |
| **Mehsana(Jornang) APMC** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), wheat, castor seed |
| **Mehsana(Mehsana Veg) APMC** | 13 | 2026-11-03 | 2026-11-03 | onion, brinjal, tomato, cabbage |
| **Mekhliganj APMC** | 4 | 2026-11-03 | 2026-11-03 | rice, brinjal, jute, potato |
| **Melaghar APMC** | 14 | 2026-11-03 | 2026-11-03 | cock, rice(fine/superfine/grade a), ridgeguard(tori), onion |
| **Melapalayam(Uzhavar Sandhai )** | 41 | 2026-11-03 | 2026-11-03 | brinjal, pumpkin, bitter gourd, potato |
| **Melechinnar VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | french beans(frasbean) |
| **Melur(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | ashgourd, banana - green, green avare(w), ridgeguard(tori) |
| **Memari APMC** | 7 | 2026-11-03 | 2026-11-03 | rice, brinjal, sweet pumpkin, tomato |
| **Merakamudidam APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Mettupalayam(Uzhavar Sandhai )** | 58 | 2026-11-03 | 2026-11-03 | onion, chikoos(sapota), water melon, mousambi(sweet lime) |
| **Mettur(Uzhavar Sandhai )** | 46 | 2026-11-03 | 2026-11-03 | cluster beans, groundnut, ginger(green), cabbage |
| **Mhow (Ambedkar Nagar) APMC** | 5 | 2026-11-03 | 2026-11-03 | kabuli chana(chickpeas-white), bengal gram(gram)(whole), soyabean, wheat |
| **Miryalguda(Rythu Bazar)** | 10 | 2026-11-03 | 2026-11-03 | tomato, green chilli, bitter gourd, potato |
| **Modasar APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Mohana APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, onion, brinjal, tomato |
| **Mohangarh APMC** | 1 | 2026-11-03 | 2026-11-03 | guar seed(cluster beans seed) |
| **Mohanpur APMC** | 7 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), raddish, indian beans(seam), papaya(raw) |
| **Mohanur(Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | tomato, banana, cluster beans, ashgourd |
| **Mohgaon APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Momanbadodiya APMC** | 3 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), soyabean, wheat |
| **Mookkannur  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Moonak APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Morbi APMC** | 18 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), cummin seed(jeera), cucumbar(kheera), lemon |
| **Morena APMC** | 8 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), sesamum(sesame,gingelly,til), bengal gram(gram)(whole), paddy(common) |
| **Morva Hafad APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), maize, wheat |
| **Motihari APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Movva (HQ-Kuchipudi) APMC** | 1 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole) |
| **Mow APMC** | 4 | 2026-11-03 | 2026-11-03 | mustard, wheat, bajra(pearl millet/cumbu), jowar(sorghum) |
| **Mukerian APMC** | 11 | 2026-11-03 | 2026-11-03 | raddish, potato, apple, brinjal |
| **Mukerian(Talwara) APMC** | 8 | 2026-11-03 | 2026-11-03 | cauliflower, potato, apple, tomato |
| **Mukhiguda APMC** | 7 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), cabbage, tomato, pointed gourd(parval) |
| **Mukkom Market** | 25 | 2026-11-03 | 2026-11-03 | cabbage, tomato, green chilli, banana - green |
| **Muktsar APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(basmati), paddy(common), cotton |
| **Mulakalacheruvu APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Mullana APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Mullana(saha) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Mullanpur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Mullanpur Dakha (Sawadi) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Multai APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Mumbai- Fruit Market** | 13 | 2026-11-03 | 2026-11-03 | apple, cherry, pomegranate, orange |
| **Mumbai-Onion & Potato Market** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Mummidivaram APMC** | 1 | 2026-11-03 | 2026-11-03 | prawn |
| **Mundi APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, soyabean, cotton, wheat |
| **Mungawali APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, wheat, black gram(urd beans)(whole), soyabean |
| **Munnar Market** | 16 | 2026-11-03 | 2026-11-03 | lemon, green avare(w), little gourd(kundru), potato |
| **Musiri(Uzhavar Sandhai )** | 49 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cowpea(veg), beans, ginger(green) |
| **Muthupettai(Uzhavar Sandhai )** | 22 | 2026-11-03 | 2026-11-03 | bottle gourd, bhindi(ladies finger), tomato, lemon |
| **Mydukur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Mylachal VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Myladi(Uzhavar Sandhai )** | 30 | 2026-11-03 | 2026-11-03 | onion, pumpkin, amaranthus, tapioca |
| **Mylavaram APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, paddy(common), paddy(fine/superfine/grade a), cotton |
| **NGO Colony(Uzhavar Sandhai )** | 31 | 2026-11-03 | 2026-11-03 | banana, potato, tomato, ashgourd |
| **Nabha APMC** | 23 | 2026-11-03 | 2026-11-03 | orange, bhindi(ladies finger), brinjal, pea pod/pea cod/हरी मटर |
| **Nadia APMC** | 10 | 2026-11-03 | 2026-11-03 | potato, onion, brinjal, mustard |
| **Nadiad APMC** | 2 | 2026-11-03 | 2026-11-03 | tomato, potato |
| **Nadiyad(Chaklasi) APMC** | 7 | 2026-11-03 | 2026-11-03 | potato, tomato, coriander(leaves), bhindi(ladies finger) |
| **Nadiyad(Piplag) APMC** | 18 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), coriander(leaves), guar, sponge gourd |
| **Nagalapuram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Nagapattinam(Uzhavar Sandhai )** | 40 | 2026-11-03 | 2026-11-03 | banana, brinjal, cabbage, snakeguard |
| **Nagarkurnool APMC** | 2 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal), maize |
| **Nagda APMC** | 5 | 2026-11-03 | 2026-11-03 | green peas, bengal gram(gram)(whole), maize, soyabean |
| **Nagod APMC** | 7 | 2026-11-03 | 2026-11-03 | barley(jau), wheat, buttery, lentil(masur)(whole) |
| **Naidupet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Naigaon(Kuntur)** | 2 | 2026-11-03 | 2026-11-03 | cotton, soyabean |
| **Nainpur APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Nakodar APMC** | 3 | 2026-11-03 | 2026-11-03 | brinjal, paddy(common), green chilli |
| **Nakodar(Sarih) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Nakrekal APMC** | 1 | 2026-11-03 | 2026-11-03 | lime |
| **Nalkheda APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, mustard, wheat, soyabean |
| **Namagiripettai RM** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Namakkal(Uzhavar Sandhai )** | 53 | 2026-11-03 | 2026-11-03 | onion, coriander(leaves), bitter gourd, groundnut |
| **Nanakmatta APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Nandigama APMC** | 4 | 2026-11-03 | 2026-11-03 | wood, dry chillies, maize, paddy(fine/superfine/grade a) |
| **Nandikotkur APMC** | 2 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), maize |
| **Nandyal APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(common) |
| **Nanganallur(Uzhavar Sandhai )** | 53 | 2026-11-03 | 2026-11-03 | grapes, cauliflower, coriander(leaves), mousambi(sweet lime) |
| **Naraingarh APMC** | 28 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), potato, ridgeguard(tori), peas wet |
| **Narasannapet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Narasinghpur APMC** | 7 | 2026-11-03 | 2026-11-03 | cauliflower, green chilli, ladies finger, cucumbar(kheera) |
| **Naravarikuppam(Uzhavar Sandhai )** | 16 | 2026-11-03 | 2026-11-03 | thondekai, marigold(calcutta), ridgeguard(tori), tomato |
| **Narayanpet APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), paddy(common) |
| **Narayanpur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Narkatiaganj APMC** | 1 | 2026-11-03 | 2026-11-03 | cauliflower |
| **Narmadapuram APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), maize |
| **Narnaul APMC** | 25 | 2026-11-03 | 2026-11-03 | garlic, raddish, cucumbar(kheera), tender coconut |
| **Narnaund APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(basmati), bajra(pearl millet/cumbu) |
| **Narsapur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Narsinghgarh APMC** | 11 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), soyabean, maize, black gram(urd beans)(whole) |
| **Narsinghpur APMC** | 10 | 2026-11-03 | 2026-11-03 | maize, lentil(masur)(whole), red gram/arhar/tur(whole), wheat |
| **Narsipatnam APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Natrampalli(Uzhavar Sandhai )** | 32 | 2026-11-03 | 2026-11-03 | potato, cluster beans, green chilli, coconut |
| **Naugachiya APMC** | 5 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cabbage, raddish, brinjal |
| **Naugaon APMC** | 5 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), mustard, sesamum(sesame,gingelly,til), wheat |
| **Naugarh APMC** | 9 | 2026-11-03 | 2026-11-03 | brinjal, bhindi(ladies finger), pointed gourd(parval), apple |
| **Navsari APMC** | 22 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), pointed gourd(parval), banana, guar |
| **Needamangalam(Uzhavar Sandhai )** | 21 | 2026-11-03 | 2026-11-03 | onion, brinjal, raddish, cluster beans |
| **Neemuch APMC** | 28 | 2026-11-03 | 2026-11-03 | amaltas, garlic, chiaseeds, basil |
| **Neemuch(F&V) APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Nekkonda APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Nelakondapally APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Neora APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Neredcherla APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **New Grain Market , Faridabad APMC** | 3 | 2026-11-03 | 2026-11-03 | onion, potato, tomato |
| **New Grain Market , Panchkula APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Neyyatinkara Market** | 19 | 2026-11-03 | 2026-11-03 | amaranthus, beetroot, banana - green, colacasia |
| **Nidadavolu APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(fine/superfine/grade a) |
| **Nihal Singh Wala APMC** | 11 | 2026-11-03 | 2026-11-03 | capsicum, green chilli, potato, carrot |
| **Nilagiri APMC** | 3 | 2026-11-03 | 2026-11-03 | brinjal, tomato, pumpkin |
| **Nilokheri APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), paddy(basmati) |
| **Nimapara APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Nimbahera APMC** | 6 | 2026-11-03 | 2026-11-03 | garlic, groundnut, soyabean, mustard |
| **Nimdhighi Market** | 11 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), rice(fine/superfine/grade a), onion, bitter gourd |
| **Nissing APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Niwadi APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, soyabean, sesamum(sesame,gingelly,til), black gram(urd beans)(whole) |
| **Nizamabad APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, turmeric, maize |
| **Nizar APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Nizar(Rumkitalav) APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Noor Mehal APMC** | 5 | 2026-11-03 | 2026-11-03 | methi(leaves), bottle gourd, raddish, cauliflower |
| **North Paravur Market** | 40 | 2026-11-03 | 2026-11-03 | amaranthus, bottle gourd, lemon, little gourd(kundru) |
| **Nuguru Charla APMC** | 2 | 2026-11-03 | 2026-11-03 | cotton, paddy(fine/superfine/grade a) |
| **Nurpurbet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Nuzvid APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Obedullaganj APMC** | 4 | 2026-11-03 | 2026-11-03 | paddy(common), wheat, maize, bengal gram(gram)(whole) |
| **Omalloor Market** | 4 | 2026-11-03 | 2026-11-03 | green chilli, bitter gourd, brinjal, bhindi(ladies finger) |
| **Omchatinya Multi State Agro Purpose Co-Op Society, Dist Ahilyanagar** | 8 | 2026-11-03 | 2026-11-03 | soyabean, maize, green gram(moong)(whole), onion |
| **Osiyan Mathania APMC** | 6 | 2026-11-03 | 2026-11-03 | cummin seed(jeera), groundnut, wheat, guar seed(cluster beans seed) |
| **PMY Bilaspur** | 13 | 2026-11-03 | 2026-11-03 | papaya, apple, pineapple, bhindi(ladies finger) |
| **PMY Chamba** | 10 | 2026-11-03 | 2026-11-03 | pomegranate, cucumbar(kheera), carrot, potato |
| **PMY Dhalli Shimla** | 2 | 2026-11-03 | 2026-11-03 | onion, peas wet |
| **PMY Hamirpur** | 17 | 2026-11-03 | 2026-11-03 | banana, bottle gourd, lemon, guava |
| **PMY Kangni Mandi** | 24 | 2026-11-03 | 2026-11-03 | banana, bottle gourd, potato, french beans(frasbean) |
| **PMY Kangra** | 38 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime), chikoos(sapota), onion, brinjal |
| **PMY Kather Solan** | 16 | 2026-11-03 | 2026-11-03 | apple, coriander(leaves), bottle gourd, cucumbar(kheera) |
| **PMY Paonta Sahib** | 24 | 2026-11-03 | 2026-11-03 | apple, pomegranate, orange, green chilli |
| **Paatan APMC** | 10 | 2026-11-03 | 2026-11-03 | paddy(common), green gram(moong)(whole), red gram/arhar/tur(whole), wheat |
| **Pabiacherra APMC** | 14 | 2026-11-03 | 2026-11-03 | cowpea(veg), tomato, potato, brinjal |
| **Pachaur APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, mustard, bengal gram(gram)(whole), lentil(masur)(whole) |
| **Pachaur(F&V) APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, corriander seed, soyabean, bengal gram(gram)(whole) |
| **Padampur APMC** | 6 | 2026-11-03 | 2026-11-03 | cotton, guar, pumpkin, mustard |
| **Padappai(Uzhavar Sandhai )** | 46 | 2026-11-03 | 2026-11-03 | potato, bitter gourd, groundnut, ashgourd |
| **Paderu APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Pai APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Pakala APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **Palacode(Uzhavar Sandhai )** | 46 | 2026-11-03 | 2026-11-03 | onion, coriander(leaves), tomato, cowpea(veg) |
| **Palakkad Market** | 43 | 2026-11-03 | 2026-11-03 | banana, black gram(urd beans)(whole), red gram/arhar/tur(whole), bhindi(ladies finger) |
| **Palakonda APMC** | 5 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), black gram(urd beans)(whole), maize, paddy(common) |
| **Palamaner APMC** | 8 | 2026-11-03 | 2026-11-03 | brinjal, cabbage, ridgeguard(tori), tomato |
| **Palanganatham(Uzhavar Sandhai )** | 51 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, coriander(leaves), amaranthus |
| **Palani(Uzhavar Sandhai )** | 45 | 2026-11-03 | 2026-11-03 | cluster beans, green chilli, banana - green, beans |
| **Palanpur APMC** | 8 | 2026-11-03 | 2026-11-03 | maize, bajra(pearl millet/cumbu), wheat, green gram dal(moong dal) |
| **Palari APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Palasa APMC** | 2 | 2026-11-03 | 2026-11-03 | cashewnuts, paddy(fine/superfine/grade a) |
| **Palayamkottai(Uzhavar Sandhai )** | 49 | 2026-11-03 | 2026-11-03 | potato, coriander(leaves), mousambi(sweet lime), tomato |
| **Palera APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Palitana APMC** | 12 | 2026-11-03 | 2026-11-03 | wheat, bajra(pearl millet/cumbu), bengal gram(gram)(whole), lemon |
| **Paliyamangalam  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | cowpea(veg) |
| **Palladam(Uzhavar Sandhai )** | 32 | 2026-11-03 | 2026-11-03 | papaya, bottle gourd, drumstick, onion green |
| **Pallahara APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Pallapatti (Uzhavar Sandhai )** | 30 | 2026-11-03 | 2026-11-03 | tapioca, coconut, sweet potato, amla(nelli kai) |
| **Pallavaram(Uzhavar Sandhai )** | 47 | 2026-11-03 | 2026-11-03 | onion, potato, brinjal, bhindi(ladies finger) |
| **Pallikonda(Uzhavar Sandhai)** | 39 | 2026-11-03 | 2026-11-03 | bitter gourd, bhindi(ladies finger), green chilli, green avare(w) |
| **Palsana APMC** | 3 | 2026-11-03 | 2026-11-03 | guar seed(cluster beans seed), bajra(pearl millet/cumbu), groundnut |
| **Palwal APMC** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), cotton, paddy(basmati) |
| **Pamarru APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Pamohi(Garchuk) APMC** | 30 | 2026-11-03 | 2026-11-03 | beetroot, brinjal, cabbage, ginger(green) |
| **Pampady Market** | 11 | 2026-11-03 | 2026-11-03 | cowpea(veg), colacasia, bhindi(ladies finger), bitter gourd |
| **Pananchery VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Panchkul(Kalka) APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Panchpedwa APMC** | 1 | 2026-11-03 | 2026-11-03 | banana - green |
| **Pandhana APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, wheat, soyabean, cotton |
| **Pandhurna APMC** | 3 | 2026-11-03 | 2026-11-03 | groundnut, soyabean, maize |
| **Pandkital APMC** | 8 | 2026-11-03 | 2026-11-03 | potato, tomato, brinjal, pumpkin |
| **Pandua APMC** | 8 | 2026-11-03 | 2026-11-03 | brinjal, rice(fine/superfine/grade a), masur dal, bhindi(ladies finger) |
| **Panichowki** | 5 | 2026-11-03 | 2026-11-03 | brinjal, cowpea(veg), green chilli, pointed gourd(parval) |
| **Panipat APMC** | 12 | 2026-11-03 | 2026-11-03 | bottle gourd, brinjal, cabbage, paddy(basmati) |
| **Panipat(Babarpur) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Panisagar APMC** | 7 | 2026-11-03 | 2026-11-03 | cabbage, potato, cucumbar(kheera), onion |
| **Panna APMC** | 7 | 2026-11-03 | 2026-11-03 | mustard, lentil(masur)(whole), buttery, wheat |
| **Panposh APMC** | 7 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), bhindi(ladies finger), bottle gourd, tomato |
| **Panruti(Uzhavar Sandhai )** | 27 | 2026-11-03 | 2026-11-03 | bottle gourd, green avare(w), snakeguard, lemon |
| **Panyam APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Papanasam(Uzhavar Sandhai )** | 25 | 2026-11-03 | 2026-11-03 | pumpkin, green chilli, banana - green, mango(raw-ripe) |
| **Pappanchani VFPCK Market** | 3 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), amranthas red, cowpea(veg) |
| **Paramakudi(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | pumpkin, tomato, bitter gourd, bhindi(ladies finger) |
| **Paramathivelur(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | potato, cauliflower, papaya, tomato |
| **Parappanangadi VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Parassala Market** | 16 | 2026-11-03 | 2026-11-03 | cowpea(veg), banana, amaranthus, drumstick |
| **Paraswada APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Pargi APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Parimpore Srinagar (F&V)** | 30 | 2026-11-03 | 2026-11-03 | brinjal, bottle gourd, cauliflower, french beans(frasbean) |
| **Parlakhemundi APMC** | 2 | 2026-11-03 | 2026-11-03 | sweet potato, tomato |
| **Parsoniya Mandi, Mahua block APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Paruthipattu(Uzhavar Sandhai )** | 23 | 2026-11-03 | 2026-11-03 | onion, capsicum, green avare(w), raddish |
| **Parvathipuram APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Pathalgaon APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Pathankot (Kanwa) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Pathapatnam APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Patharia APMC** | 9 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), black gram(urd beans)(whole), green gram(moong)(whole), mustard |
| **Patiala APMC** | 29 | 2026-11-03 | 2026-11-03 | brinjal, pumpkin, guava, kinnow |
| **Patiala(Anaj Mandi Sanaur Road) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Patiala(New Anaj Mandi) APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), paddy(basmati) |
| **Patran APMC** | 28 | 2026-11-03 | 2026-11-03 | cabbage, cauliflower, squash(chappal kadoo), green chilli |
| **Pattambi Market** | 33 | 2026-11-03 | 2026-11-03 | pumpkin, ginger(green), green chilli, onion |
| **Patti APMC** | 8 | 2026-11-03 | 2026-11-03 | capsicum, leafy vegetable, turnip, apple |
| **Pattikonda APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Pattukottai(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | banana, garlic, coriander(leaves), bitter gourd |
| **Pavilion Ground,Khammam,RBZ** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Pawai APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Payyannur Market** | 8 | 2026-11-03 | 2026-11-03 | banana - green, tapioca, amaranthus, coconut seed |
| **Pazhayannur VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | cowpea(veg) |
| **Pedana APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), black gram(urd beans)(whole) |
| **Peddapalli APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Peddapuram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Pehowa APMC** | 1 | 2026-11-03 | 2026-11-03 | bottle gourd |
| **Penamaluru (HQ-Kankipadu) APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), black gram(urd beans)(whole), maize |
| **Pendraroad APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Pendurthi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Pennagaram(Uzhavar Sandhai )** | 42 | 2026-11-03 | 2026-11-03 | green chilli, green avare(w), beetroot, lemon |
| **Penukonda APMC** | 2 | 2026-11-03 | 2026-11-03 | groundnut, maize |
| **Penumuru APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **Perambakkam(Uzhavar Sandhai )** | 11 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), snakeguard, ridgeguard(tori), brinjal |
| **Perambalur(Uzhavar Sandhai )** | 51 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime), cluster beans, bottle gourd, ashgourd |
| **Perambra Market** | 26 | 2026-11-03 | 2026-11-03 | banana, potato, snakeguard, elephant yam(suran)/amorphophallus |
| **Perampet(Uzhavar Sandhai)** | 43 | 2026-11-03 | 2026-11-03 | amaranthus, cowpea(veg), ginger(green), coconut |
| **Peravurani(Uzhavar Sandhai)** | 25 | 2026-11-03 | 2026-11-03 | carrot, ridgeguard(tori), raddish, onion |
| **Perfect Krishi Market Yard Pvt Ltd, Dist Nashik** | 1 | 2026-11-03 | 2026-11-03 | pomegranate |
| **Perfect Krushi Market Yard, Tal Madha, Dist Solapur** | 1 | 2026-11-03 | 2026-11-03 | pomegranate |
| **Perinthalmanna Market** | 22 | 2026-11-03 | 2026-11-03 | capsicum, onion, carrot, ashgourd |
| **Periyakulam(Uzhavar Sandhai )** | 36 | 2026-11-03 | 2026-11-03 | brinjal, amaranthus, cabbage, onion |
| **Periyar Nagar(Uzhavar Sandhai )** | 32 | 2026-11-03 | 2026-11-03 | coriander(leaves), bitter gourd, pumpkin, tapioca |
| **Perumbavoor Market** | 31 | 2026-11-03 | 2026-11-03 | amaranthus, elephant yam(suran)/amorphophallus, tomato, little gourd(kundru) |
| **Perundurai(Uzhavar Sandhai )** | 32 | 2026-11-03 | 2026-11-03 | onion, cluster beans, bitter gourd, beetroot |
| **Pethappampatti RM** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Petlawad APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, maize, cotton, soyabean |
| **Petlawad(F&V) APMC** | 16 | 2026-11-03 | 2026-11-03 | methi(leaves), bhindi(ladies finger), cucumbar(kheera), coriander(leaves) |
| **Phek APMC** | 4 | 2026-11-03 | 2026-11-03 | chow chow, pumpkin, banana, yam(ratalu) |
| **Phillaur APMC** | 4 | 2026-11-03 | 2026-11-03 | paddy(common), cauliflower, raddish, spinach |
| **Phillaur(Apra Mandi) APMC** | 10 | 2026-11-03 | 2026-11-03 | spinach, paddy(common), potato, brinjal |
| **Phirangipuram APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Pichhour APMC** | 2 | 2026-11-03 | 2026-11-03 | groundnut, wheat |
| **Pidugurala APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Piler APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **Pillukhera APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Pimpalgaon Baswant(Saykheda)** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Pipariya APMC** | 8 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), maize, paddy(common), bengal gram(gram)(whole) |
| **Pipariya(F&V) APMC** | 11 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), pumpkin, potato, sponge gourd |
| **Pipli APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Piplya APMC** | 12 | 2026-11-03 | 2026-11-03 | groundnut, bengal gram(gram)(whole), wheat, soyabean |
| **Piprai APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, maize, paddy(common) |
| **Pithapuram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Podili APMC** | 1 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole) |
| **Pohari APMC** | 10 | 2026-11-03 | 2026-11-03 | maize, bengal gram(gram)(whole), soyabean, groundnut |
| **Polavaram APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, paddy(common) |
| **Pollachi(Uzhavar Sandhai )** | 40 | 2026-11-03 | 2026-11-03 | coriander(leaves), pumpkin, green chilli, thondekai |
| **Polur(Uzhavar Sandhai )** | 44 | 2026-11-03 | 2026-11-03 | tomato, papaya, snakeguard, thondekai |
| **Ponduru APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Ponnamaravathi(Uzhavar Sandhai)** | 26 | 2026-11-03 | 2026-11-03 | brinjal, amaranthus, green chilli, banana |
| **Ponnur APMC** | 1 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole) |
| **Porbandar APMC** | 32 | 2026-11-03 | 2026-11-03 | seetapal, coriander(leaves), green chilli, garlic |
| **Porsa APMC** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), potato, mustard |
| **Pratapgarh APMC** | 9 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), wheat, maize, methi seeds |
| **Pratappur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Prattipadu APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Premium Krushi Utpanna Bazar, Nashik** | 3 | 2026-11-03 | 2026-11-03 | french beans(frasbean), pomegranate, bitter gourd |
| **Prithvipur APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Proddatur APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), groundnut, bengal gram(gram)(whole) |
| **Pudukottai(Uzhavar Sandhai )** | 49 | 2026-11-03 | 2026-11-03 | banana, onion, papaya, ashgourd |
| **Pugal Road Grain APMC** | 4 | 2026-11-03 | 2026-11-03 | groundnut, isabgul(psyllium), green gram(moong)(whole), moath dal |
| **Pulivendala APMC** | 1 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime) |
| **Pullur Periya  VFPCK Market** | 3 | 2026-11-03 | 2026-11-03 | ashgourd, cowpea(veg), elephant yam(suran)/amorphophallus |
| **Pulpally Market** | 14 | 2026-11-03 | 2026-11-03 | cowpea(veg), brinjal, ginger(green), pumpkin |
| **Pundri APMC** | 12 | 2026-11-03 | 2026-11-03 | paddy(basmati), tomato, brinjal, bottle gourd |
| **Pune(Khadiki)** | 17 | 2026-11-03 | 2026-11-03 | sweet pumpkin, carrot, guar, beans |
| **Pune(Manjri)** | 23 | 2026-11-03 | 2026-11-03 | carrot, beans, bitter gourd, drumstick |
| **Pune(Moshi)** | 33 | 2026-11-03 | 2026-11-03 | little gourd(kundru), mousambi(sweet lime), orange, seetapal |
| **Pune(Pimpri)** | 8 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), bhindi(ladies finger), bottle gourd, cauliflower |
| **Punganur APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Punhana APMC** | 3 | 2026-11-03 | 2026-11-03 | apple, water melon, mousambi(sweet lime) |
| **Purain APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Purulia APMC** | 8 | 2026-11-03 | 2026-11-03 | brinjal, masur dal, potato, pumpkin |
| **Pusapatirega APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Puttaparthi  APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, groundnut |
| **Puttur APMC** | 1 | 2026-11-03 | 2026-11-03 | mango |
| **Quadian APMC** | 14 | 2026-11-03 | 2026-11-03 | papaya, brinjal, cauliflower, onion |
| **Quilandy Market** | 21 | 2026-11-03 | 2026-11-03 | beetroot, bitter gourd, pumpkin, bhindi(ladies finger) |
| **RSPuram(Uzhavar Sandhai )** | 60 | 2026-11-03 | 2026-11-03 | banana, potato, water melon, mousambi(sweet lime) |
| **RYTHU BAZAR ERRAGADDA** | 23 | 2026-11-03 | 2026-11-03 | brinjal, cauliflower, ladies finger, field pea |
| **RYTHU BAZAR FALAKNUMA** | 22 | 2026-11-03 | 2026-11-03 | ladies finger, cauliflower, onion, potato |
| **Radhanpur APMC** | 6 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), ajwan, wheat, guar seed(cluster beans seed) |
| **Raghogarh APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, maize |
| **Rahama APMC** | 2 | 2026-11-03 | 2026-11-03 | pumpkin, brinjal |
| **Rahatgarh APMC** | 6 | 2026-11-03 | 2026-11-03 | soyabean, bengal gram(gram)(whole), maize, wheat |
| **Railway Koduru APMC** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Raipur Rani APMC** | 14 | 2026-11-03 | 2026-11-03 | tomato, brinjal, potato, colacasia |
| **Rairakhol APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, bhindi(ladies finger), brinjal, onion |
| **Raisen APMC** | 3 | 2026-11-03 | 2026-11-03 | wheat, maize, paddy(common) |
| **Raisingh Nagar APMC** | 7 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), green gram(moong)(whole), guar, bengal gram(gram)(whole) |
| **Rajahmundry APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rajam APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Rajampet APMC** | 1 | 2026-11-03 | 2026-11-03 | papaya |
| **Rajanagaram APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Rajapalayam(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | coriander(leaves), green chilli, guava, elephant yam(suran)/amorphophallus |
| **Rajgarh APMC** | 5 | 2026-11-03 | 2026-11-03 | soyabean, bengal gram(gram)(whole), maize, wheat |
| **Rajkot APMC** | 16 | 2026-11-03 | 2026-11-03 | cotton, bengal gram(gram)(whole), wheat, castor seed |
| **Rajkot(Veg.Sub Yard) APMC** | 11 | 2026-11-03 | 2026-11-03 | cluster beans, lemon, potato, brinjal |
| **Rajnagar APMC** | 5 | 2026-11-03 | 2026-11-03 | soyabean, bengal gram(gram)(whole), sesamum(sesame,gingelly,til), wheat |
| **Rajound APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rajouri (Phaliana) (F&V)** | 15 | 2026-11-03 | 2026-11-03 | orange, pineapple, bitter gourd, raddish |
| **Rajpipla APMC** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Rajpura APMC** | 8 | 2026-11-03 | 2026-11-03 | tomato, apple, banana, onion |
| **Rajsamand APMC** | 3 | 2026-11-03 | 2026-11-03 | tomato, potato, onion |
| **Rajula APMC** | 12 | 2026-11-03 | 2026-11-03 | wheat, kabuli chana(chickpeas-white), sesamum(sesame,gingelly,til), mustard |
| **Ramachandrapuram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Raman APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, tomato, onion, banana |
| **Ramanathapuram(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), ginger(green), onion green, pumpkin |
| **Ramdev Krushi Bazaar, Digras road, Manora, Dist Washim** | 2 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), soyabean |
| **Ramkrishanpur(Howrah)** | 11 | 2026-11-03 | 2026-11-03 | brinjal, onion, tomato, rice |
| **Ramnagar APMC** | 7 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), tomato, cauliflower, capsicum |
| **Rampachodvaram APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Rampura Phul APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rampuraphul(Bhai Rupan) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rampuraphul(Chowke) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rampuraphul(Dhapali) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rampuraphul(Mehraj) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Rampuraphul(Nabha Mandi) APMC** | 20 | 2026-11-03 | 2026-11-03 | orange, apple, papaya, cucumbar(kheera) |
| **Rampurhat APMC** | 6 | 2026-11-03 | 2026-11-03 | paddy(common), mustard, rice, onion |
| **Ranaghat APMC** | 8 | 2026-11-03 | 2026-11-03 | rice(fine/superfine/grade a), masur dal, onion, brinjal |
| **Rani APMC** | 4 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), green gram(moong)(whole), cotton, guar seed(cluster beans seed) |
| **Ranipettai(Uzhavar Sandhai )** | 48 | 2026-11-03 | 2026-11-03 | garlic, bhindi(ladies finger), banana - green, carrot |
| **Raniwara APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Ranniangadi Market** | 5 | 2026-11-03 | 2026-11-03 | cowpea(veg), tapioca, bhindi(ladies finger), amaranthus |
| **Rannod APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Rapthadu APMC** | 1 | 2026-11-03 | 2026-11-03 | ground nut seed |
| **Rapur APMC** | 1 | 2026-11-03 | 2026-11-03 | wood |
| **Rasipuram(Uzhavar Sandhai )** | 50 | 2026-11-03 | 2026-11-03 | cauliflower, coriander(leaves), ashgourd, bhindi(ladies finger) |
| **Ratia APMC** | 14 | 2026-11-03 | 2026-11-03 | carrot, mousambi(sweet lime), potato, brinjal |
| **Ratlam APMC** | 10 | 2026-11-03 | 2026-11-03 | wheat, garlic, green peas, black gram(urd beans)(whole) |
| **Ravulapalem (Kothapeta APMC)** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Rawatsar APMC** | 3 | 2026-11-03 | 2026-11-03 | tomato, onion, potato |
| **Rawla APMC** | 4 | 2026-11-03 | 2026-11-03 | green gram(moong)(whole), guar, mustard, cotton |
| **Raxaul APMC** | 5 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), brinjal, cauliflower, potato |
| **Rayachoti APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Rayagada APMC** | 7 | 2026-11-03 | 2026-11-03 | brinjal, cabbage, cluster beans, cauliflower |
| **Rayagada(Muniguda) APMC** | 6 | 2026-11-03 | 2026-11-03 | drumstick, pointed gourd(parval), beetroot, bhindi(ladies finger) |
| **Rayya APMC** | 10 | 2026-11-03 | 2026-11-03 | onion, tomato, potato, paddy(basmati) |
| **Rayya(Sathiala) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(basmati) |
| **Razole APMC** | 1 | 2026-11-03 | 2026-11-03 | coconut |
| **Rehati APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), green gram(moong)(whole), maize |
| **Rehli APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, wheat |
| **Rewa APMC** | 6 | 2026-11-03 | 2026-11-03 | mustard, lentil(masur)(whole), wheat, gur(jaggery) |
| **Rewa(F&V) APMC** | 5 | 2026-11-03 | 2026-11-03 | cauliflower, potato, bottle gourd, cabbage |
| **Rewari APMC** | 5 | 2026-11-03 | 2026-11-03 | banana, apple, onion, tomato |
| **Rishikesh APMC** | 19 | 2026-11-03 | 2026-11-03 | onion, bottle gourd, bhindi(ladies finger), potato |
| **Rohtak APMC** | 9 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime), potato, onion, bajra(pearl millet/cumbu) |
| **Rohtak(Kalanaur) APMC** | 2 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), paddy(basmati) |
| **Rompicherla APMC** | 2 | 2026-11-03 | 2026-11-03 | groundnut, paddy(fine/superfine/grade a) |
| **Roorkee APMC** | 10 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cucumbar(kheera), bottle gourd, potato |
| **Ropar APMC** | 19 | 2026-11-03 | 2026-11-03 | apple, ginger(green), cabbage, french beans(frasbean) |
| **Rudrangi APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, cotton, paddy(fine/superfine/grade a) |
| **Rudrapur APMC** | 23 | 2026-11-03 | 2026-11-03 | pomegranate, mousambi(sweet lime), papaya, potato |
| **S.R.Puram APMC** | 1 | 2026-11-03 | 2026-11-03 | gur(jaggery) |
| **SMY Baijnath** | 15 | 2026-11-03 | 2026-11-03 | guava, apple, bhindi(ladies finger), green chilli |
| **SMY Bhuntar** | 30 | 2026-11-03 | 2026-11-03 | brinjal, tomato, bottle gourd, ginger(green) |
| **SMY Chail Chowk** | 3 | 2026-11-03 | 2026-11-03 | cabbage, pea pod/pea cod/हरी मटर, ginger(green) |
| **SMY Chauri Bihal** | 5 | 2026-11-03 | 2026-11-03 | cauliflower, cabbage, capsicum, apple |
| **SMY Dhanotu** | 26 | 2026-11-03 | 2026-11-03 | papaya, cauliflower, bottle gourd, french beans(frasbean) |
| **SMY Dharamshala** | 28 | 2026-11-03 | 2026-11-03 | apple, mousambi(sweet lime), cabbage, cauliflower |
| **SMY Jaisinghpur** | 16 | 2026-11-03 | 2026-11-03 | raddish, bhindi(ladies finger), orange, indian colza(sarson) |
| **SMY Jogindernagar** | 19 | 2026-11-03 | 2026-11-03 | tomato, bottle gourd, cauliflower, cucumbar(kheera) |
| **SMY Jwalaji** | 3 | 2026-11-03 | 2026-11-03 | onion, banana, cauliflower |
| **SMY Nadaun** | 8 | 2026-11-03 | 2026-11-03 | papaya, pineapple, apple, mousambi(sweet lime) |
| **SMY Nagrota Bagwan** | 18 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime), kinnow, orange, cabbage |
| **SMY Nahan** | 20 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), ginger(green), apple, banana |
| **SMY Nalagarh** | 12 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cucumbar(kheera), tomato, bottle gourd |
| **SMY Nerwa** | 4 | 2026-11-03 | 2026-11-03 | capsicum, peas wet, french beans(frasbean), cabbage |
| **SMY Palampur** | 34 | 2026-11-03 | 2026-11-03 | brinjal, pumpkin, raddish, bhindi(ladies finger) |
| **SMY Patli Kulh** | 1 | 2026-11-03 | 2026-11-03 | persimon(japani fal) |
| **SMY Rajgarh** | 1 | 2026-11-03 | 2026-11-03 | french beans(frasbean) |
| **SMY Wakhnaghat** | 5 | 2026-11-03 | 2026-11-03 | french beans(frasbean), pea pod/pea cod/हरी मटर, tomato, cabbage |
| **Sabalgarh APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, bajra(pearl millet/cumbu), sesamum(sesame,gingelly,til), mustard |
| **Sadasivpet APMC** | 2 | 2026-11-03 | 2026-11-03 | maize, onion |
| **Sadhaura APMC** | 12 | 2026-11-03 | 2026-11-03 | raddish, tomato, brinjal, bhindi(ladies finger) |
| **Sadulpur APMC** | 3 | 2026-11-03 | 2026-11-03 | cowpea(lobia/karamani), bajra(pearl millet/cumbu), green gram(moong)(whole) |
| **Sadulshahar APMC** | 5 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), cotton, wheat, guar seed(cluster beans seed) |
| **Safidon APMC** | 3 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime), paddy(basmati), apple |
| **Sagar APMC** | 9 | 2026-11-03 | 2026-11-03 | mustard, soyabean, lak(teora), maize |
| **Sagar(F&V) APMC** | 21 | 2026-11-03 | 2026-11-03 | colacasia, papaya, banana, tomato |
| **Sahaspur APMC** | 2 | 2026-11-03 | 2026-11-03 | pumpkin, raddish |
| **Sahidngar APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Sahnewal APMC** | 9 | 2026-11-03 | 2026-11-03 | onion, paddy(common), potato, tomato |
| **Sai Agro Infratrade Pvt Agri Market, Dist Wardha** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Saidpurhat APMC** | 5 | 2026-11-03 | 2026-11-03 | potato, rice, wheat, onion |
| **Sailana APMC** | 8 | 2026-11-03 | 2026-11-03 | soyabean, mustard, onion, wheat |
| **Sainthia APMC** | 8 | 2026-11-03 | 2026-11-03 | rice, tomato, onion, brinjal |
| **Sakhigopal APMC** | 1 | 2026-11-03 | 2026-11-03 | coconut |
| **Saluru APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Samalkot APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Samana APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Samana(Kakrala) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Sambalpur APMC** | 3 | 2026-11-03 | 2026-11-03 | pumpkin, brinjal, tomato |
| **Sami APMC** | 8 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), ajwan, corriander seed, castor seed |
| **Sampara (Kakinada Rural) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Sampath Nagar(Uzhavar Sandhai )** | 43 | 2026-11-03 | 2026-11-03 | banana, amaranthus, carrot, snakeguard |
| **Samrala APMC** | 9 | 2026-11-03 | 2026-11-03 | ginger(green), cucumbar(kheera), onion, potato |
| **Samsi APMC** | 3 | 2026-11-03 | 2026-11-03 | rice, onion, potato |
| **Sanawad APMC** | 7 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), wheat, green gram(moong)(whole), cotton |
| **Sanawad(F&V) APMC** | 10 | 2026-11-03 | 2026-11-03 | bottle gourd, potato, green chilli, brinjal |
| **Sanchore APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Sangat APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Sangli(Miraj)** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Sangli(Phale, Bhajipala Market)** | 10 | 2026-11-03 | 2026-11-03 | mousambi(sweet lime), ginger(green), onion, apple |
| **Sangriya APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Sankarankoil(Uzhavar Sandhai )** | 30 | 2026-11-03 | 2026-11-03 | papaya, bhindi(ladies finger), amla(nelli kai), onion |
| **Sankarapuram(Uzhavar Sandhai )** | 42 | 2026-11-03 | 2026-11-03 | cluster beans, green chilli, mango(raw-ripe), yam(ratalu) |
| **Sant Namdev Krushi Bazar, Tal Sengaon Dist Hingoli** | 2 | 2026-11-03 | 2026-11-03 | soyabean, turmeric |
| **Santar Bazaar APMC** | 8 | 2026-11-03 | 2026-11-03 | raddish, green chilli, cauliflower, coriander(leaves) |
| **Santir Bazar APMC** | 2 | 2026-11-03 | 2026-11-03 | brinjal, potato |
| **Sanwer APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, soyabean |
| **Sarangapur APMC161** | 1 | 2026-11-03 | 2026-11-03 | jowar(sorghum) |
| **Sarangpur APMC** | 5 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), soyabean, wheat, lentil(masur)(whole) |
| **Sarangpur(F&V) APMC** | 9 | 2026-11-03 | 2026-11-03 | sponge gourd, bhindi(ladies finger), brinjal, cauliflower |
| **Sarankul APMC** | 3 | 2026-11-03 | 2026-11-03 | bitter gourd, cucumbar(kheera), tomato |
| **Saraskana APMC** | 6 | 2026-11-03 | 2026-11-03 | brinjal, bhindi(ladies finger), papaya(raw), cabbage |
| **Sargipali APMC** | 8 | 2026-11-03 | 2026-11-03 | pumpkin, green chilli, bhindi(ladies finger), onion |
| **Sarona APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Saroornagar,RBZ** | 24 | 2026-11-03 | 2026-11-03 | cauliflower, little gourd(kundru), brinjal, carrot |
| **Sarvepalli APMC** | 1 | 2026-11-03 | 2026-11-03 | lime |
| **Sasthamkotta Market** | 17 | 2026-11-03 | 2026-11-03 | colacasia, mushroom, snakeguard, tomato |
| **Sathiyamagalam(Uzhavar Sandhai )** | 40 | 2026-11-03 | 2026-11-03 | cauliflower, cluster beans, banana, bhindi(ladies finger) |
| **Sathur(Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | onion, ashgourd, tomato, amaranthus |
| **Satna APMC** | 12 | 2026-11-03 | 2026-11-03 | green peas, lak(teora), lentil(masur)(whole), bengal gram(gram)(whole) |
| **Satna(F&V) APMC** | 6 | 2026-11-03 | 2026-11-03 | apple, potato, mousambi(sweet lime), pomegranate |
| **Sattenapalli APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), cotton |
| **Sattupalli (Ramalayam),RBZ** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Sattupally APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Saunsar APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Savarkundla APMC** | 7 | 2026-11-03 | 2026-11-03 | wheat, cummin seed(jeera), bajra(pearl millet/cumbu), soyabean |
| **Sayala APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Sealdah Koley Market APMC** | 12 | 2026-11-03 | 2026-11-03 | cabbage, capsicum, pointed gourd(parval), carrot |
| **Segaon APMC** | 4 | 2026-11-03 | 2026-11-03 | cotton, wheat, maize, soyabean |
| **Sehora APMC** | 8 | 2026-11-03 | 2026-11-03 | wheat, maize, bengal gram(gram)(whole), buttery |
| **Sehore APMC** | 9 | 2026-11-03 | 2026-11-03 | soyabean, black gram(urd beans)(whole), bengal gram(gram)(whole), kabuli chana(chickpeas-white) |
| **Sehore(F&V) APMC** | 21 | 2026-11-03 | 2026-11-03 | ginger(green), bottle gourd, cucumbar(kheera), capsicum |
| **Semriharchand APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, paddy(common), soyabean, wheat |
| **Sendhwa APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, maize, cotton, paddy(common) |
| **Sendhwa(F&V) APMC** | 11 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, cabbage, bhindi(ladies finger) |
| **Seoni APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Sevda APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), bajra(pearl millet/cumbu), sesamum(sesame,gingelly,til) |
| **Shadabad APMC** | 3 | 2026-11-03 | 2026-11-03 | bottle gourd, brinjal, pumpkin |
| **Shadnagar APMC** | 9 | 2026-11-03 | 2026-11-03 | green chilli, beetroot, tomato, bitter gourd |
| **Shadora APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Shahabad APMC** | 31 | 2026-11-03 | 2026-11-03 | apple, cluster beans, brinjal, cucumbar(kheera) |
| **Shahagarh APMC** | 2 | 2026-11-03 | 2026-11-03 | mustard, wheat |
| **Shahaswan APMC** | 5 | 2026-11-03 | 2026-11-03 | papaya, brinjal, banana - green, apple |
| **Shahdol APMC** | 1 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole) |
| **Shahpura Bhitoni (F&V) APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, black gram(urd beans)(whole), wheat |
| **Shahpura Niwas APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, kodo millet(varagu), kutki, dhawai flowers |
| **Shahzadpur APMC** | 13 | 2026-11-03 | 2026-11-03 | onion, potato, cucumbar(kheera), capsicum |
| **Shajapur APMC** | 10 | 2026-11-03 | 2026-11-03 | mustard, onion, black gram(urd beans)(whole), coriander(leaves) |
| **Shajapur(F&V) APMC** | 2 | 2026-11-03 | 2026-11-03 | garlic, onion |
| **Shamgarh APMC** | 15 | 2026-11-03 | 2026-11-03 | onion, linseed, soyabean, groundnut |
| **Shamshabad APMC** | 4 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), wheat, soyabean, maize |
| **Shankarapally APMC** | 2 | 2026-11-03 | 2026-11-03 | potato, green chilli |
| **Shekhpura APMC** | 5 | 2026-11-03 | 2026-11-03 | bottle gourd, wheat, cucumbar(kheera), brinjal |
| **Sheopurbadod APMC** | 7 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), maize, wheat, mustard |
| **Sheopurkalan (F&V) APMC** | 9 | 2026-11-03 | 2026-11-03 | cauliflower, cucumbar(kheera), cabbage, raddish |
| **Sheopurkalan APMC** | 8 | 2026-11-03 | 2026-11-03 | maize, paddy(common), jowar(sorghum), wheat |
| **Sherpur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Shevgaon(Bodhegaon)** | 1 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu) |
| **Shillong APMC** | 22 | 2026-11-03 | 2026-11-03 | pumpkin, betal leaves, cucumbar(kheera), squash(chappal kadoo) |
| **Shivpuri APMC** | 8 | 2026-11-03 | 2026-11-03 | mustard, wheat, bengal gram(gram)(whole), groundnut |
| **Shivpuri(F&V) APMC** | 14 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), potato, spinach, green chilli |
| **Shivsiddha Govind Producer Company Ltd Sanchalit Khajgi Krushi Utpann Bajar Samati-Abhona-Kalwan** | 3 | 2026-11-03 | 2026-11-03 | maize, soyabean, onion |
| **Shree Salasar Krushi Bazar, Dist Parbhani** | 3 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), soyabean, bengal gram(gram)(whole) |
| **Shujalpur APMC** | 9 | 2026-11-03 | 2026-11-03 | onion, bengal gram(gram)(whole), kabuli chana(chickpeas-white), soyabean |
| **Shyampur APMC** | 2 | 2026-11-03 | 2026-11-03 | wheat, soyabean |
| **Siddavatam APMC** | 2 | 2026-11-03 | 2026-11-03 | banana, papaya |
| **Siddhpur APMC** | 8 | 2026-11-03 | 2026-11-03 | mustard, groundnut, castor seed, black gram(urd beans)(whole) |
| **Siddipet(Rythu Bazar)** | 15 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), beetroot, cauliflower, potato |
| **Sidhi APMC** | 1 | 2026-11-03 | 2026-11-03 | wheat |
| **Sidhwan Bet (Lodhiwala) APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Sidhwan Bet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Sikri APMC** | 1 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu) |
| **Siliguri APMC** | 11 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal), masur dal, green gram dal(moong dal), green chilli |
| **Silvani APMC** | 5 | 2026-11-03 | 2026-11-03 | wheat, lentil(masur)(whole), lak(teora), maize |
| **Simhadhripuram APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Sindi (Selu)** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Singampunari(Uzhavar Sandhai )** | 35 | 2026-11-03 | 2026-11-03 | knool khol, onion green, tomato, potato |
| **Singanallur(Uzhavar Sandhai )** | 56 | 2026-11-03 | 2026-11-03 | pumpkin, potato, bitter gourd, ashgourd |
| **Singanamala APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Sirali APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, maize, wheat |
| **Sirali(F&V) APMC** | 5 | 2026-11-03 | 2026-11-03 | bottle gourd, brinjal, tomato, cauliflower |
| **Sircilla APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Sirhind APMC** | 28 | 2026-11-03 | 2026-11-03 | capsicum, lemon, onion, guava |
| **Sirkali(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | onion, cluster beans, bottle gourd, cabbage |
| **Sironj APMC** | 9 | 2026-11-03 | 2026-11-03 | lak(teora), wheat, mustard, black gram(urd beans)(whole) |
| **Sirsa APMC** | 2 | 2026-11-03 | 2026-11-03 | potato, tomato |
| **Sitamarhi APMC** | 2 | 2026-11-03 | 2026-11-03 | onion, potato |
| **Sitamau APMC** | 7 | 2026-11-03 | 2026-11-03 | wheat, soyabean, garlic, linseed |
| **Sitarganj APMC** | 9 | 2026-11-03 | 2026-11-03 | brinjal, carrot, raddish, cucumbar(kheera) |
| **Sivagangai (Uzhavar Sandhai )** | 42 | 2026-11-03 | 2026-11-03 | papaya, green chilli, banana - green, cabbage |
| **Sivakasi(Uzhavar Sandhai )** | 35 | 2026-11-03 | 2026-11-03 | potato, brinjal, pumpkin, bottle gourd |
| **Siwan APMC** | 12 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), cucumbar(kheera), capsicum, squash(chappal kadoo) |
| **Siyana APMC** | 13 | 2026-11-03 | 2026-11-03 | bottle gourd, cucumbar(kheera), pumpkin, cauliflower |
| **Sohela APMC** | 2 | 2026-11-03 | 2026-11-03 | brinjal, pumpkin |
| **Sohna APMC** | 10 | 2026-11-03 | 2026-11-03 | raddish, cauliflower, potato, methi(leaves) |
| **Sojat Road APMC** | 1 | 2026-11-03 | 2026-11-03 | guar seed(cluster beans seed) |
| **Sonepat APMC** | 16 | 2026-11-03 | 2026-11-03 | guava, banana, capsicum, onion |
| **Songadh APMC** | 2 | 2026-11-03 | 2026-11-03 | guar, bhindi(ladies finger) |
| **Songadh(Badarpada) APMC** | 2 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), guar |
| **Songadh(Umrada) APMC** | 2 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), guar |
| **Sonkatch APMC** | 3 | 2026-11-03 | 2026-11-03 | wheat, maize, soyabean |
| **Sontoli APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(common), chili red, mustard |
| **Sooramangalam(Uzhavar Sandhai )** | 57 | 2026-11-03 | 2026-11-03 | pumpkin, onion, mousambi(sweet lime), banana - green |
| **Sooranad  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Soyatkalan APMC** | 10 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), bengal gram(gram)(whole), garlic, wheat |
| **Sridungargarh APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Sriganganagar (F&V) APMC** | 37 | 2026-11-03 | 2026-11-03 | sponge gourd, tinda, colacasia, cucumbar(kheera) |
| **Srikakulam APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Srikalahasti APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), groundnut |
| **Srivilliputhur(Uzhavar Sandhai )** | 36 | 2026-11-03 | 2026-11-03 | potato, cluster beans, ginger(green), carrot |
| **Sulargharat APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Sullurpet APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Sultan bathery Market** | 4 | 2026-11-03 | 2026-11-03 | coconut, coffee, ginger(green), banana - green |
| **Sultanpur APMC** | 3 | 2026-11-03 | 2026-11-03 | raddish, brinjal, cauliflower |
| **Sulur(Uzhavar Sandhai )** | 39 | 2026-11-03 | 2026-11-03 | potato, cauliflower, brinjal, cluster beans |
| **Sundarapuram(Uzhavar Sandhai )** | 45 | 2026-11-03 | 2026-11-03 | banana, pumpkin, ashgourd, tapioca |
| **Sunguvarchatram(Uzhavar Sandhai )** | 25 | 2026-11-03 | 2026-11-03 | onion, bhindi(ladies finger), bitter gourd, potato |
| **Surajgarh APMC** | 1 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu) |
| **Surajpur APMC** | 1 | 2026-11-03 | 2026-11-03 | same/savi |
| **Surat APMC** | 38 | 2026-11-03 | 2026-11-03 | beetroot, cabbage, cauliflower, pumpkin |
| **Suratgarh APMC** | 6 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), guar, green gram(moong)(whole), cotton |
| **Surjyagarha APMC** | 5 | 2026-11-03 | 2026-11-03 | brinjal, tomato, potato, onion |
| **Susner APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, soyabean, bengal gram(gram)(whole), black gram(urd beans)(whole) |
| **Suthalia APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Suvasra APMC** | 5 | 2026-11-03 | 2026-11-03 | soyabean, black gram(urd beans)(whole), wheat, groundnut |
| **Taal APMC** | 3 | 2026-11-03 | 2026-11-03 | soyabean, wheat, maize |
| **Tadepalligudem APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Tadipatri APMC** | 2 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), bengal gram(gram)(whole) |
| **Takhatpur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Talalagir APMC** | 5 | 2026-11-03 | 2026-11-03 | green chilli, brinjal, bhindi(ladies finger), tomato |
| **Talcher APMC** | 8 | 2026-11-03 | 2026-11-03 | pumpkin, cauliflower, tomato, bhindi(ladies finger) |
| **Taleja APMC** | 10 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), groundnut, green gram(moong)(whole), black gram(urd beans)(whole) |
| **Taliparamba Market** | 7 | 2026-11-03 | 2026-11-03 | brinjal, potato, cucumbar(kheera), green chilli |
| **Talod(Harsol) APMC** | 4 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), wheat, paddy(common), cotton |
| **Tamarainagar(Uzhavar Sandhai )** | 42 | 2026-11-03 | 2026-11-03 | water melon, sweet potato, snakeguard, lime |
| **Tamluk (Medinipur E) APMC** | 8 | 2026-11-03 | 2026-11-03 | betal leaves, brinjal, bitter gourd, potato |
| **Tanda Urmur APMC** | 26 | 2026-11-03 | 2026-11-03 | apple, bhindi(ladies finger), cauliflower, field pea |
| **Tanduru APMC** | 5 | 2026-11-03 | 2026-11-03 | maize, soyabean, green gram(moong)(whole), black gram(urd beans)(whole) |
| **Tanuku APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Tarana APMC** | 4 | 2026-11-03 | 2026-11-03 | soyabean, kabuli chana(chickpeas-white), wheat, black gram(urd beans)(whole) |
| **Tarantaran APMC** | 5 | 2026-11-03 | 2026-11-03 | brinjal, onion, paddy(basmati), potato |
| **Tarori APMC** | 5 | 2026-11-03 | 2026-11-03 | tomato, banana, onion, potato |
| **Teghra APMC** | 3 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, bhindi(ladies finger) |
| **Tekari APMC** | 3 | 2026-11-03 | 2026-11-03 | cauliflower, bhindi(ladies finger), bottle gourd |
| **Tenakallu APMC** | 1 | 2026-11-03 | 2026-11-03 | tamarind fruit |
| **Tenali APMC** | 1 | 2026-11-03 | 2026-11-03 | lime |
| **Tendukheda APMC** | 5 | 2026-11-03 | 2026-11-03 | lentil(masur)(whole), gur(jaggery), maize, soyabean |
| **Tenkasi(Uzhavar Sandhai )** | 44 | 2026-11-03 | 2026-11-03 | papaya, coconut, sweet potato, snakeguard |
| **Thalappara  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | bottle gourd |
| **Thalasserry Market** | 7 | 2026-11-03 | 2026-11-03 | onion, carrot, potato, snakeguard |
| **Thalavadi(Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | papaya, bitter gourd, green chilli, beans |
| **Thalavaipuram(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | tomato, brinjal, coriander(leaves), bottle gourd |
| **Thalayolaparambu Market** | 28 | 2026-11-03 | 2026-11-03 | banana, cluster beans, drumstick, onion |
| **Thamarakkulam VFPCK Market** | 4 | 2026-11-03 | 2026-11-03 | cowpea(veg), banana, coconut seed, bitter gourd |
| **Thamarassery Market** | 21 | 2026-11-03 | 2026-11-03 | ashgourd, bitter gourd, cowpea(veg), green chilli |
| **Thammampatti (Uzhavar Sandhai )** | 43 | 2026-11-03 | 2026-11-03 | pumpkin, cauliflower, bottle gourd, bhindi(ladies finger) |
| **Thandla APMC** | 4 | 2026-11-03 | 2026-11-03 | wheat, maize, soyabean, cotton |
| **Thanesar APMC** | 33 | 2026-11-03 | 2026-11-03 | water melon, pineapple, onion, mousambi(sweet lime) |
| **Thanjavur(Uzhavar Sandhai )** | 50 | 2026-11-03 | 2026-11-03 | banana, onion, cauliflower, coriander(leaves) |
| **Thara APMC** | 7 | 2026-11-03 | 2026-11-03 | guar seed(cluster beans seed), cummin seed(jeera), groundnut, bajra(pearl millet/cumbu) |
| **Thara(Shihori) APMC** | 3 | 2026-11-03 | 2026-11-03 | bajra(pearl millet/cumbu), groundnut, castor seed |
| **Tharad APMC** | 4 | 2026-11-03 | 2026-11-03 | castor seed, guar seed(cluster beans seed), cummin seed(jeera), mustard |
| **Thathakapatti(Uzhavar Sandhai )** | 60 | 2026-11-03 | 2026-11-03 | coriander(leaves), water melon, groundnut, tapioca |
| **Thattanchavady APMC** | 4 | 2026-11-03 | 2026-11-03 | ragi(finger millet), green gram(moong)(whole), black gram(urd beans)(whole), paddy(common) |
| **The Agricultural Produce Market Committee-Amreli** | 17 | 2026-11-03 | 2026-11-03 | jowar(sorghum), green gram(moong)(whole), castor seed, soyabean |
| **Theni(Uzhavar Sandhai )** | 57 | 2026-11-03 | 2026-11-03 | chili red, papaya, pineapple, beans |
| **Thiruchanur APMC** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Thiruchengodu RM** | 45 | 2026-11-03 | 2026-11-03 | pumpkin, coriander(leaves), mousambi(sweet lime), cluster beans |
| **Thirukalukundram(Uzhavar Sandhai )** | 23 | 2026-11-03 | 2026-11-03 | banana, ashgourd, ginger(green), ridgeguard(tori) |
| **Thirumangalam RM** | 1 | 2026-11-03 | 2026-11-03 | jowar(sorghum) |
| **Thirumangalam(Uzhavar Sandhai )** | 26 | 2026-11-03 | 2026-11-03 | bitter gourd, amaranthus, drumstick, guava |
| **Thirunavalur RM** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Thirupathur RM** | 50 | 2026-11-03 | 2026-11-03 | cauliflower, chikoos(sapota), bhindi(ladies finger), sweet potato |
| **Thiruvali  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Thiruvaniyoor  VFPCK Market** | 2 | 2026-11-03 | 2026-11-03 | ashgourd, banana |
| **Thiruverumbur(Uzhavar Sandhai )** | 37 | 2026-11-03 | 2026-11-03 | banana, bottle gourd, amaranthus, drumstick |
| **Thodupuzha Market** | 8 | 2026-11-03 | 2026-11-03 | banana, grapes, water melon, orange |
| **Thoubal APMC** | 11 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), bengal gram dal(chana dal), potato, onion |
| **Thrippunithura Market** | 30 | 2026-11-03 | 2026-11-03 | cabbage, banana - green, tapioca, bottle gourd |
| **Thrissur Market** | 2 | 2026-11-03 | 2026-11-03 | amaranthus, ashgourd |
| **Thuraiyur RM** | 45 | 2026-11-03 | 2026-11-03 | tomato, potato, cauliflower, papaya |
| **Tikamgarh APMC** | 6 | 2026-11-03 | 2026-11-03 | soyabean, mustard, black gram(urd beans)(whole), wheat |
| **Tikonia APMC** | 6 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), bottle gourd, lemon, pumpkin |
| **Tileibani APMC** | 6 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, bhindi(ladies finger), cabbage |
| **Timarni APMC** | 6 | 2026-11-03 | 2026-11-03 | maize, black gram(urd beans)(whole), soyabean, green gram(moong)(whole) |
| **Tindivanam RM** | 46 | 2026-11-03 | 2026-11-03 | papaya, banana - green, snakeguard, mango(raw-ripe) |
| **Tinsukia Market** | 18 | 2026-11-03 | 2026-11-03 | sponge gourd, green chilli, ginger(green), carrot |
| **Tiphra APMC** | 30 | 2026-11-03 | 2026-11-03 | white muesli, beans, apple, orange |
| **Tirukattupalli(Uzhavar Sandhai )** | 19 | 2026-11-03 | 2026-11-03 | pumpkin, coconut, onion green, brinjal |
| **Tirupatthur(Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | potato, green chilli, green avare(w), drumstick |
| **Tiruppur (North) (Uzhavar Sandhai )** | 38 | 2026-11-03 | 2026-11-03 | brinjal, bhindi(ladies finger), cowpea(veg), bitter gourd |
| **Tiruppur (South) (Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | cauliflower, coriander(leaves), cowpea(veg), beans |
| **Tiruthani(Uzhavar Sandhai )** | 30 | 2026-11-03 | 2026-11-03 | brinjal, bitter gourd, green chilli, ginger(green) |
| **Tiruthuraipoondi(Uzhavar Sandhai )** | 26 | 2026-11-03 | 2026-11-03 | ashgourd, pumpkin, bhindi(ladies finger), amaranthus |
| **Tiruvallur(Uzhavar Sandhai )** | 20 | 2026-11-03 | 2026-11-03 | onion, bhindi(ladies finger), ridgeguard(tori), cluster beans |
| **Tiruvannamalai(Uzhavar Sandhai )** | 60 | 2026-11-03 | 2026-11-03 | banana, cowpea(veg), green avare(w), mango(raw-ripe) |
| **Tiruvarur(Uzhavar Sandhai )** | 22 | 2026-11-03 | 2026-11-03 | pumpkin, tomato, drumstick, lime |
| **Tiruvuru APMC** | 3 | 2026-11-03 | 2026-11-03 | maize, dry chillies, rice(fine/superfine/grade a) |
| **Todaraisingh APMC** | 8 | 2026-11-03 | 2026-11-03 | guar seed(cluster beans seed), sesamum(sesame,gingelly,til), jowar(sorghum), mustard |
| **Toofanganj APMC** | 4 | 2026-11-03 | 2026-11-03 | jute, brinjal, rice, potato |
| **Tsemenyu APMC** | 2 | 2026-11-03 | 2026-11-03 | chow chow, pumpkin |
| **Tuli APMC** | 6 | 2026-11-03 | 2026-11-03 | cucumbar(kheera), ginger(green), papaya(raw), brinjal |
| **Tulsipur APMC** | 5 | 2026-11-03 | 2026-11-03 | brinjal, lentil(masur)(whole), pumpkin, bottle gourd |
| **Tuni APMC** | 1 | 2026-11-03 | 2026-11-03 | cashewnuts |
| **Tuticorin(Uzhavar Sandhai )** | 52 | 2026-11-03 | 2026-11-03 | pumpkin, banana, potato, cauliflower |
| **Uchana APMC** | 4 | 2026-11-03 | 2026-11-03 | cotton, bajra(pearl millet/cumbu), paddy(common), paddy(basmati) |
| **Udaipur (Grain) APMC** | 6 | 2026-11-03 | 2026-11-03 | soyabean, wheat, chili red, gur(jaggery) |
| **Udaipura APMC** | 9 | 2026-11-03 | 2026-11-03 | buttery, bengal gram(gram)(whole), green gram(moong)(whole), wheat |
| **Udala APMC** | 7 | 2026-11-03 | 2026-11-03 | potato, tomato, bitter gourd, pumpkin |
| **Udhagamandalam(Uzhavar Sandhai )** | 53 | 2026-11-03 | 2026-11-03 | banana, grapes, orange, ashgourd |
| **Udumalpettai RM** | 45 | 2026-11-03 | 2026-11-03 | coriander(leaves), tomato, banana - green, coconut |
| **Udumbannoor  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Ujjain APMC** | 13 | 2026-11-03 | 2026-11-03 | green peas, bengal gram(gram)(whole), paddy(common), garlic |
| **Ujjain(F&V) APMC** | 15 | 2026-11-03 | 2026-11-03 | ginger(green), tomato, capsicum, bitter gourd |
| **Ulundurpet RM** | 32 | 2026-11-03 | 2026-11-03 | banana - green, snakeguard, mango(raw-ripe), tender coconut |
| **Umariya APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), soyabean, buttery |
| **Umarked(Danki)** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Umreth APMC** | 2 | 2026-11-03 | 2026-11-03 | paddy(common), bajra(pearl millet/cumbu) |
| **Una APMC** | 2 | 2026-11-03 | 2026-11-03 | soyabean, cotton |
| **Unava APMC** | 2 | 2026-11-03 | 2026-11-03 | cotton, castor seed |
| **Undi APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Ungatur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Unhel APMC** | 3 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), wheat, soyabean |
| **Uniyara APMC** | 6 | 2026-11-03 | 2026-11-03 | wheat, mustard, soyabean, black gram(urd beans)(whole) |
| **Unjha APMC** | 6 | 2026-11-03 | 2026-11-03 | suva(dill seed), ajwan, soanf, cummin seed(jeera) |
| **Uparhali Pmy APMC** | 27 | 2026-11-03 | 2026-11-03 | ginger(green), cabbage, papaya(raw), pumpkin |
| **Upleta APMC** | 10 | 2026-11-03 | 2026-11-03 | soyabean, castor seed, corriander seed, cotton |
| **Urvakonda APMC** | 2 | 2026-11-03 | 2026-11-03 | bengal gram(gram)(whole), groundnut |
| **Usilampatti(Uzhavar Sandhai )** | 23 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), amaranthus, green chilli, green avare(w) |
| **Uthiramerur RM** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **V. Kota Sub-yard of AMC Palamaneru** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **V.Saidapur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Vadakkenchery Market** | 29 | 2026-11-03 | 2026-11-03 | brinjal, cabbage, little gourd(kundru), cowpea(veg) |
| **Vadali APMC** | 6 | 2026-11-03 | 2026-11-03 | red gram/arhar/tur(whole), soyabean, wheat, cotton |
| **Vadalur(Uzhavar Sandhai )** | 35 | 2026-11-03 | 2026-11-03 | bhindi(ladies finger), beans, mango(raw-ripe), yam(ratalu) |
| **Vadaseri RM** | 45 | 2026-11-03 | 2026-11-03 | water melon, bitter gourd, banana, ashgourd |
| **Vadavalli(Uzhavar Sandhai )** | 43 | 2026-11-03 | 2026-11-03 | cauliflower, brinjal, papaya, mousambi(sweet lime) |
| **Vadgam APMC** | 5 | 2026-11-03 | 2026-11-03 | groundnut, maize, wheat, guar seed(cluster beans seed) |
| **Vadhvan APMC** | 28 | 2026-11-03 | 2026-11-03 | garlic, bitter gourd, raddish, drumstick |
| **Vakadu APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Valakom  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Valangaiman RM** | 18 | 2026-11-03 | 2026-11-03 | ashgourd, snakeguard, bottle gourd, coconut |
| **Valmikipuram APMC** | 1 | 2026-11-03 | 2026-11-03 | tomato |
| **Valsad APMC** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Vamanapuram Market** | 15 | 2026-11-03 | 2026-11-03 | tapioca, bitter gourd, brinjal, elephant yam(suran)/amorphophallus |
| **Vanasthalipuram,RBZ** | 26 | 2026-11-03 | 2026-11-03 | cauliflower, field bean(anumulu), bottle gourd, snakeguard |
| **Vandavasi(Uzhavar Sandhai )** | 34 | 2026-11-03 | 2026-11-03 | brinjal, tomato, amaranthus, beetroot |
| **Vaniyampadi(Uzhavar Sandhai )** | 43 | 2026-11-03 | 2026-11-03 | groundnut, bottle gourd, pumpkin, drumstick |
| **Vankaner APMC** | 7 | 2026-11-03 | 2026-11-03 | wheat, soanf, groundnut, cotton |
| **Vantamamidi APMC** | 11 | 2026-11-03 | 2026-11-03 | brinjal, tomato, cucumbar(kheera), field pea |
| **Varud(Rajura Bazar)** | 1 | 2026-11-03 | 2026-11-03 | green chilli |
| **Vayala  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Vazhapadi(Uzhavar Sandhai)** | 37 | 2026-11-03 | 2026-11-03 | papaya, mousambi(sweet lime), bitter gourd, carrot |
| **Vedaranyam(Uzhavar Sandhai)** | 29 | 2026-11-03 | 2026-11-03 | brinjal, bhindi(ladies finger), ginger(green), chow chow |
| **Vedasandur(Uzhavar Sandhai )** | 10 | 2026-11-03 | 2026-11-03 | pumpkin, bhindi(ladies finger), tomato, bottle gourd |
| **Veernapalli APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Velayuthampalayam(Uzhavar Sandhai )** | 22 | 2026-11-03 | 2026-11-03 | cluster beans, snakeguard, onion green, bitter gourd |
| **Vellanad VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Vellore RM** | 56 | 2026-11-03 | 2026-11-03 | garlic, papaya, ashgourd, coconut |
| **Vemulawada APMC** | 3 | 2026-11-03 | 2026-11-03 | cotton, paddy(common), paddy(fine/superfine/grade a) |
| **Vemuru APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Vengamedu(Uzhavar Sandhai )** | 24 | 2026-11-03 | 2026-11-03 | coriander(leaves), bottle gourd, bhindi(ladies finger), drumstick |
| **Vengannore  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | banana |
| **Vengeri(Kozhikode) Market** | 11 | 2026-11-03 | 2026-11-03 | bitter gourd, cucumbar(kheera), bhindi(ladies finger), brinjal |
| **Vengola  VFPCK Market** | 1 | 2026-11-03 | 2026-11-03 | pineapple |
| **Venkatagiri APMC** | 3 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a), black gram(urd beans)(whole), groundnut |
| **Venkateswarnagar APMC** | 13 | 2026-11-03 | 2026-11-03 | bottle gourd, cluster beans, cabbage, carrot |
| **Veraval APMC** | 6 | 2026-11-03 | 2026-11-03 | soyabean, bengal gram(gram)(whole), groundnut, black gram(urd beans)(whole) |
| **Vidisha APMC** | 10 | 2026-11-03 | 2026-11-03 | wheat, paddy(common), maize, lentil(masur)(whole) |
| **Vijapur APMC** | 1 | 2026-11-03 | 2026-11-03 | groundnut |
| **Vijapur(Gojjariya) APMC** | 1 | 2026-11-03 | 2026-11-03 | castor seed |
| **Vijapur(Kukarvada) APMC** | 1 | 2026-11-03 | 2026-11-03 | castor seed |
| **Vijapur(Vegetable) APMC** | 1 | 2026-11-03 | 2026-11-03 | green chilli |
| **Vijayanagaram APMC** | 1 | 2026-11-03 | 2026-11-03 | maize |
| **Vijayawada APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(fine/superfine/grade a) |
| **Vijaypur APMC** | 4 | 2026-11-03 | 2026-11-03 | sesamum(sesame,gingelly,til), bajra(pearl millet/cumbu), mustard, wheat |
| **Vikasnagar APMC** | 13 | 2026-11-03 | 2026-11-03 | tomato, colacasia, green chilli, cucumbar(kheera) |
| **Villupuram(Uzhavar Sandhai )** | 10 | 2026-11-03 | 2026-11-03 | tomato, ashgourd, banana - green, amaranthus |
| **Vinukonda APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Viralimalai(Uzhavar Sandhai )** | 23 | 2026-11-03 | 2026-11-03 | papaya, tomato, amaranthus, green chilli |
| **Viramgam APMC** | 4 | 2026-11-03 | 2026-11-03 | castor seed, cotton, paddy(common), wheat |
| **Virudhunagar(Uzhavar Sandhai )** | 19 | 2026-11-03 | 2026-11-03 | cluster beans, green avare(w), ashgourd, bhindi(ladies finger) |
| **Viruthachalam(Uzhavar Sandhai )** | 33 | 2026-11-03 | 2026-11-03 | papaya, ashgourd, bhindi(ladies finger), coconut |
| **Visakhapatnam APMC** | 1 | 2026-11-03 | 2026-11-03 | rice |
| **Visavadar APMC** | 12 | 2026-11-03 | 2026-11-03 | black gram(urd beans)(whole), kulthi(horse gram), green gram(moong)(whole), groundnut(split) |
| **Vishrampur APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Visnagar APMC** | 4 | 2026-11-03 | 2026-11-03 | cotton, bajra(pearl millet/cumbu), wheat, castor seed |
| **Vuyyur APMC** | 1 | 2026-11-03 | 2026-11-03 | black gram dal(urd dal) |
| **Vyra APMC** | 1 | 2026-11-03 | 2026-11-03 | soyabean |
| **Warangal APMC** | 31 | 2026-11-03 | 2026-11-03 | maize, soyabean, brinjal, french beans(frasbean) |
| **Weekly Market Area,RBZ APMC** | 1 | 2026-11-03 | 2026-11-03 | bitter gourd |
| **Wokha Town APMC** | 3 | 2026-11-03 | 2026-11-03 | green chilli, pumpkin, papaya |
| **Yamuna Nagar APMC** | 1 | 2026-11-03 | 2026-11-03 | potato |
| **Yellamanchili APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **Yellandu APMC** | 2 | 2026-11-03 | 2026-11-03 | cotton, maize |
| **Yemmiganur APMC** | 2 | 2026-11-03 | 2026-11-03 | groundnut, castor seed |
| **Yerragondapalem APMC** | 1 | 2026-11-03 | 2026-11-03 | cotton |
| **Yerraguntla APMC** | 1 | 2026-11-03 | 2026-11-03 | onion |
| **Zaheerabad APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, black gram(urd beans)(whole), soyabean, red gram/arhar/tur(whole) |
| **Zalod(Sanjeli) APMC** | 4 | 2026-11-03 | 2026-11-03 | maize, bajra(pearl millet/cumbu), paddy(common), wheat |
| **Zaloosa-Chararishrief (F&V)** | 1 | 2026-11-03 | 2026-11-03 | apple |
| **Zira APMC** | 15 | 2026-11-03 | 2026-11-03 | carrot, papaya, cucumbar(kheera), capsicum |
| **kum Kalan APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |
| **lakhowal APMC** | 1 | 2026-11-03 | 2026-11-03 | paddy(common) |

---

## 3. Provenance Linkage: Sample Accepted Rows vs Raw Crawled Files

Every accepted row is tagged with `data_provenance='real'`, `is_synthetic=False`, and linked to its SHA-256 byte payload:

| Crop | Mandi | Date | Modal Price (₹/qtl) | Source | Raw Crawled SHA-256 Hash |
|---|---|---|---|---|---|
| Cabbage | Mukkom Market | 2026-11-03 | ₹2,600.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Tomato | Mukkom Market | 2026-11-03 | ₹4,000.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Tapioca | Mananthavady Market | 2026-11-03 | ₹3,000.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Banana | Perambra Market | 2026-11-03 | ₹3,000.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Potato | Perambra Market | 2026-11-03 | ₹2,500.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Snakeguard | Perambra Market | 2026-11-03 | ₹4,000.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Paddy(Common) | Kagaznagar APMC | 2026-11-03 | ₹2,400.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Wheat | Krishi Upaj Mandi Samiti Bichhiya | 2026-11-03 | ₹2,725.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Ladies Finger | RYTHU BAZAR FALAKNUMA | 2026-11-03 | ₹4,500.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |
| Cauliflower | RYTHU BAZAR FALAKNUMA | 2026-11-03 | ₹1,800.00 | `data_gov_in` | `921b3fb75f85523dcf9c...` |

---

## 4. Quarantined Records Diagnostic Summary

Quarantined records are isolated byte-for-byte in `data/quarantine/`. No quarantined row is ever allowed to enter `data/processed/panel.parquet` or training pipelines.

- **Plausibility Violations**: Rows where $P_{\min} > P_{\text{modal}}$ or $P_{\text{modal}} > P_{\max}$ are routed to quarantine.
- **Out of Bounds**: Extreme values outside biological and historical price boundaries are blocked.
- **Unknown Units**: Any non-standard unit that cannot be converted to Rs/quintal is quarantined without silent estimation.
