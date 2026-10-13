# Kiak Kai Extradosed Bridge — 4D BIM Method Statement Simulation

Web app (static, single page) แสดงแบบจำลอง 3 มิติแบบ BIM + แผนงาน 4D ของงาน Balanced Cantilever สะพานข้ามแม่น้ำเจ้าพระยา บริเวณแยกเกียกกาย ช่วง P1–P4 (120 + 165 + 71.766 m)

| ฟังก์ชัน | รายละเอียด |
|---|---|
| 4D Timeline | เล่น/เลื่อนวันที่ ดูลำดับงาน Gantt, S-curve, Method Statement 17+ ขั้นตอน |
| BIM | คลิกชิ้นส่วน ดู Element ID, แบบอ้างอิง, ปริมาตร, สถานะ 4D, ที่มาของวันที่ · Export GLB |
| ธีม | Day · Sunset · Night · BIM 4D · Blueprint |
| Drone | Drone Tour อัตโนมัติ 14 จุด + โหมดบินเอง (W/A/S/D, R/F, ลากเมาส์) |
| เสียง | เสียงบรรยากาศ (แม่น้ำ ลม นก เครื่องจักร ปั๊มคอนกรีต ใบพัดโดรน) + ดนตรี — สังเคราะห์ด้วย Web Audio ไม่ต้องมีไฟล์เสียง |
| แผงข้อมูล | ปุ่ม ◧ / ◨ (หรือกด `[` `]`) เปิด/ปิดแผงซ้าย/ขวา · `H` ซ่อน UI ทั้งหมด |
| อัปเดตแผน | ปุ่ม **📂 อัปเดตแผน** อัปโหลด PDF (พิมพ์จาก MS Project) / MS Project XML / CSV / JSON แล้วแบบจำลองจะคำนวณวันที่ใหม่ทั้งหมด (บันทึกในเบราว์เซอร์นั้น ๆ) |
| PWA | ติดตั้งเป็นแอป (Install app) และเปิดใช้แบบออฟไลน์ได้หลังเปิดครั้งแรก |

## โครงสร้างไฟล์

```
index.html                 แอปทั้งหมด (three.js r160 จาก CDN)
manifest.webmanifest, sw.js, icons/   PWA
sample/schedule_R2.json    แผนงาน Programme R.2 (12/12/2024) ที่แปลงแล้ว – ใช้ทดสอบปุ่มอัปเดตแผน
sample/schedule_template.csv  ตัวอย่างรูปแบบ CSV
tools/mpp2json.py          แปลง .mpp → JSON (ต้องมี Java + `pip install mpxj`)
.github/workflows/deploy-pages.yml   Deploy อัตโนมัติไป GitHub Pages
```

## การอัปเดตแผนงาน

| ไฟล์ | วิธี |
|---|---|
| **PDF** | MS Project ▸ มุมมอง Gantt (คอลัมน์ ID, Task Name, Duration, Start, Finish) ▸ Print ▸ Microsoft Print to PDF ▸ อัปโหลด |
| **XML** | MS Project ▸ File ▸ Save As ▸ XML Format (*.xml) ▸ อัปโหลด |
| **.mpp** | เบราว์เซอร์อ่านไม่ได้โดยตรง → ใช้ XML/PDF ข้างบน หรือ `python tools/mpp2json.py file.mpp` แล้วอัปโหลด `.json` |
| **CSV** | คอลัมน์ `ID, Task Name, Start, Finish` (ดู `sample/schedule_template.csv`) |

การจับคู่กับ BIM ใช้ชื่องานตาม Programme R.2: `Segment A'` … `Segment T(Mid span closure)`, `Segment M1'(End span closure-Final)`, `Pylon P2A` + `Kicker`/`1st Portion`…`8th Portion`, `Pier Table … completed`, `Installation of Tower Crane`, `Assembly and Installation of Form Traveler`, `End span construction`, `Temporary support installation` (แยก P2/P3 ตามหัวข้อ `Pier No. P2/P3`).
วันที่ที่ได้มาจากการคำนวณจะถูกคำนวณใหม่อัตโนมัติ เช่น การรื้อ FT3 หลัง Segment L1 ก่อนหล่อ Closure T, Stay cable, Ballast, งานสถาปัตย์/ประติมากรรมหลังโครงสร้างแล้วเสร็จ

## Deploy ขึ้น GitHub Pages

```bash
cd kiakkai-4d-bim
git remote add origin https://github.com/<org-or-user>/kiakkai-4d-bim.git
git push -u origin main
```

จากนั้นใน GitHub: **Settings ▸ Pages ▸ Source = GitHub Actions** — workflow `deploy-pages.yml` จะ deploy ทุกครั้งที่ push ไป `main`
URL: `https://<org-or-user>.github.io/kiakkai-4d-bim/`

> **ข้อควรระวังด้านข้อมูลโครงการ:** GitHub Pages ของ repo แบบ **public** เปิดให้ทุกคนเข้าถึงได้ (รวมถึงตำแหน่ง/ขนาดโครงสร้างและแผนงาน) หากเป็นข้อมูลภายใน ให้ใช้ repo แบบ **private** กับ GitHub Pages แบบจำกัดสิทธิ์ (GitHub Enterprise Cloud) หรือ Deploy บน Azure Static Web Apps / Netlify / เซิร์ฟเวอร์ภายในที่มีการยืนยันตัวตน — repo นี้ **ไม่มี** ไฟล์แบบ PDF/MPP ต้นฉบับ

## รันในเครื่อง

```bash
python -m http.server 8080
```
เปิด `http://localhost:8080` (ต้องต่ออินเทอร์เน็ตครั้งแรกเพื่อโหลด three.js / pdf.js / ฟอนต์)

## แหล่งข้อมูลที่ใช้สร้างแบบจำลอง

Substructure 2022-08-15 · Superstructure 2023-08-25 (M-0xx–M-6xx) · Form Traveller 22-ITD-KK-FT (GA/EC) · Construction Stage & Camber Rev.2 (M-901–M-914, M-1011–M-1043) · Programme R.2 (12/12/2024) · AR Main Bridge (24 sheets) · Presentation KK-C2 R9 · Federated model "20260723_Kiek Kai Bridge 1_2&3" (Autodesk Viewer)

ข้อจำกัด: แบบจำลองเป็น Parametric จากมิติในแบบ (LOD ~200) · วันที่งานฐานราก/ตอม่อ/สถาปัตย์/งานระบบเป็นสมมติฐาน · รัฐสภาแสดงเป็น Height map 4 m · ปริมาตรคอนกรีตไม่ใช่ BOQ
