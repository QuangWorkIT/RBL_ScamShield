import os
import zipfile
import shutil
import tempfile
import xml.etree.ElementTree as ET

DOCX_PATH = r"C:\Users\USER\RBL_ScamShield\ScamShield_VN_Evidence_Grounded_Two_Tier_Architecture_for_Vi_Action_Tracker.docx"
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

def update_tracker(completed_ids=None, appendix_a_done=None, appendix_b2_done=None, appendix_b3_done=None):
    """
    Updates the status of tasks in the Action Tracker docx in-place.
    """
    if not os.path.exists(DOCX_PATH):
        raise FileNotFoundError(f"File not found: {DOCX_PATH}")

    # Read original zip
    with zipfile.ZipFile(DOCX_PATH, 'r') as zin:
        xml_content = zin.read('word/document.xml')
        all_files = {name: zin.read(name) for name in zin.namelist() if name != 'word/document.xml'}

    root = ET.fromstring(xml_content)
    tables = root.findall('.//w:tbl', NS)

    def set_cell_text(cell, new_text):
        # find or clear text elements
        t_elems = cell.findall('.//w:t', NS)
        if t_elems:
            t_elems[0].text = new_text
            for t in t_elems[1:]:
                t.text = ""
        else:
            p = cell.find('.//w:p', NS)
            if p is None:
                p = ET.SubElement(cell, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
            r = ET.SubElement(p, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
            t = ET.SubElement(r, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
            t.text = new_text

    # 1. Update Table 2 (Tasks: B1, H1-H18, M1-M10)
    if completed_ids:
        t2 = tables[1]
        for row in t2.findall('.//w:tr', NS)[1:]:
            cells = row.findall('.//w:tc', NS)
            if not cells: continue
            task_id = ''.join([t.text for t in cells[0].findall('.//w:t', NS) if t.text]).strip()
            if task_id in completed_ids:
                status_cell = cells[-1]
                set_cell_text(status_cell, "Xong")
                print(f"  [Table 2] Set {task_id} -> Xong")

    # 2. Update Table 5 (Appendix A)
    if appendix_a_done:
        t5 = tables[4]
        for row in t5.findall('.//w:tr', NS)[1:]:
            cells = row.findall('.//w:tc', NS)
            if not cells: continue
            item_num = ''.join([t.text for t in cells[0].findall('.//w:t', NS) if t.text]).strip()
            if item_num in [str(x) for x in appendix_a_done]:
                status_cell = cells[-1]
                set_cell_text(status_cell, "Xong")
                print(f"  [Table 5] Set Appendix A #{item_num} -> Xong")

    # 3. Update Table 8 (Appendix B2)
    if appendix_b2_done:
        t8 = tables[7]
        for row in t8.findall('.//w:tr', NS)[1:]:
            cells = row.findall('.//w:tc', NS)
            if not cells: continue
            item_num = ''.join([t.text for t in cells[0].findall('.//w:t', NS) if t.text]).strip()
            if item_num in [str(x) for x in appendix_b2_done]:
                status_cell = cells[-1]
                set_cell_text(status_cell, "Xong")
                print(f"  [Table 8] Set Appendix B2 #{item_num} -> Xong")

    # 4. Update Table 9 (Appendix B3)
    if appendix_b3_done:
        t9 = tables[8]
        for row in t9.findall('.//w:tr', NS)[1:]:
            cells = row.findall('.//w:tc', NS)
            if not cells: continue
            item_num = ''.join([t.text for t in cells[0].findall('.//w:t', NS) if t.text]).strip()
            if item_num in [str(x) for x in appendix_b3_done]:
                status_cell = cells[-1]
                set_cell_text(status_cell, "Xong")
                print(f"  [Table 9] Set Appendix B3 #{item_num} -> Xong")

    new_xml = ET.tostring(root, encoding='utf-8')

    # Atomic write to docx
    tmp_path = DOCX_PATH + ".tmp"
    with zipfile.ZipFile(tmp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        zout.writestr('word/document.xml', new_xml)
        for name, data in all_files.items():
            zout.writestr(name, data)

    shutil.move(tmp_path, DOCX_PATH)
    print(f"Successfully updated {DOCX_PATH} in-place.")

if __name__ == '__main__':
    # Test setting B1 and Appendix items as done (since B1 was already completed!)
    update_tracker(
        completed_ids=["B1"],
        appendix_a_done=list(range(1, 11)),
        appendix_b2_done=list(range(1, 11)),
        appendix_b3_done=list(range(1, 4))
    )
