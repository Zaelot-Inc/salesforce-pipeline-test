import os, json
from xml.etree import ElementTree as ET

NS = {"m":"http://soap.sforce.com/2006/04/metadata"}

def read_api_ver():
    try:
        with open("sfdx-project.json","r") as f:
            data = json.load(f)
            v = data.get("sourceApiVersion")
            return str(v) if v else "60.0"
    except Exception:
        return "60.0"

def collect(path):
    items = {}
    if not os.path.isfile(path): return items
    try:
        root = ET.parse(path).getroot()
        for t in root.findall("m:types", NS):
            name = (t.find("m:name", NS).text or "").strip()
            if not name: continue
            items.setdefault(name, set())
            for mem in t.findall("m:members", NS):
                m = (mem.text or "").strip()
                if m: items[name].add(m)
    except Exception as e:
        print(f"Warning: Could not parse {path}: {e}")
    return items

# --- Main script ---
merged = {}
for p in [
    "changed-sources/destructiveChanges/destructiveChanges.xml",
    "changed-sources/destructiveChangesPost/destructiveChanges.xml"
]:
    sub = collect(p)
    for k,v in sub.items():
        merged.setdefault(k, set()).update(v)

api_ver = read_api_ver()
pkg = ET.Element("Package", xmlns=NS["m"])
for tname in sorted(merged.keys()):
    t = ET.SubElement(pkg, "types")
    for m in sorted(merged[tname]):
        ET.SubElement(t, "members").text = m
    ET.SubElement(t, "name").text = tname
ET.SubElement(pkg, "version").text = api_ver

xml_string = ET.tostring(pkg, encoding="utf-8")
try:
    from xml.dom import minidom
    xml_string = minidom.parseString(xml_string).toprettyxml(indent="  ", encoding="utf-8")
except Exception:
    pass # Use the non-prettified version if minidom fails

# Get the destination path from the environment variable
dest = os.environ.get("DEST_PATH")
if not dest:
    print("Error: DEST_PATH environment variable not set.")
    exit(1)

os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "wb") as f:
    f.write(xml_string if isinstance(xml_string, bytes) else xml_string.encode("utf-8"))

print(f"Successfully created destructive manifest at: {dest}")