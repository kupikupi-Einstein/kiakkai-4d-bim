"""
mpp2json.py – convert an MS Project .mpp file into schedule JSON that the 4D BIM web app can import.

The browser cannot read .mpp (binary MS Project database), so use this offline converter
(or in MS Project: File > Save As > XML, then upload the .xml directly).

Requirements:
    Java 11+ (JRE)            https://adoptium.net
    pip install mpxj           (includes JPype; MPXJ reads .mpp / .mpx / .xml / Primavera .xer)

Usage:
    python tools/mpp2json.py "Program of Extradose at Kiak Kai Bridge R.3.mpp"  [out.json]

Then open the web app > 📂 อัปเดตแผน > drop the generated .json file.
"""
import json
import os
import sys


def to_iso(v):
    if v is None:
        return None
    s = str(v)          # LocalDateTime -> '2025-03-28T08:00'
    return s[:10]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".schedule.json"

    import jpype
    import mpxj  # noqa: F401  (adds the MPXJ jars to the class path)
    jpype.startJVM()
    from net.sf.mpxj.reader import UniversalProjectReader

    project = UniversalProjectReader().read(src)
    tasks = []
    for t in project.getTasks():
        name = t.getName()
        if name is None:
            continue
        tasks.append({
            "id": int(t.getID() or 0),
            "name": str(name),
            "start": to_iso(t.getStart()),
            "finish": to_iso(t.getFinish()),
            "level": int(t.getOutlineLevel() or 0),
        })
    jpype.shutdownJVM()

    with open(out, "w", encoding="utf-8") as f:
        json.dump({"source": os.path.basename(src), "tasks": tasks}, f, ensure_ascii=False, indent=1)
    print(f"{len(tasks)} tasks -> {out}")


if __name__ == "__main__":
    main()
