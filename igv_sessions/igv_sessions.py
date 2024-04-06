from typing import List
from pathlib import Path
from xml.dom import minidom


def initialize_igv_session(genome: Path) -> minidom.Document:
    doc = minidom.Document()
    session = doc.createElement("Session")
    session.setAttribute("genome", f"{str(genome)}")
    session.setAttribute("locus", "All")
    session.setAttribute("version", "8")
    doc.appendChild(session)
    return doc


def add_resources_to_igv_session(doc: minidom.Document, resource_list: List[Path]):
    session = doc.getElementsByTagName('Session')[0]
    resources = doc.createElement("Resources")
    session.appendChild(resources)
    for resource in resource_list:
        rsc_element = doc.createElement("Resource")
        rsc_element.setAttribute("path", f"{str(resource)}")
        rsc_element.setAttribute("type", "bam")
        resources.appendChild(rsc_element)


def divider_frac_str(n: int) -> str:
    output_str = ", ".join([str(x/n) for x in range(1 + n)])
    return output_str


def add_data_range(track: minidom.Element, doc: minidom.Document):
    data_range = doc.createElement("DataRange")
    track.appendChild(data_range)


def add_coverage_track(bam_path: Path, panel: minidom.Element, doc: minidom.Document):
    track = doc.createElement("Track")
    track.setAttribute("attributeKey", f"{bam_path.name} Coverage")
    track.setAttribute("autoScale", "true")
    track.setAttribute("clazz", "org.broad.igv.sam.CoverageTrack")
    track.setAttribute("fontSize", "10")
    track.setAttribute("id", f"{str(bam_path)}_coverage")
    track.setAttribute("name", f"{bam_path.name} Coverage")
    track.setAttribute("snpThreshold", "0.2")
    track.setAttribute("visible", "true")
    panel.appendChild(track)
    add_data_range(track, doc)


def add_render_options(track: minidom.Element, doc: minidom.Document):
    render_options = doc.createElement("RenderOptions")
    track.appendChild(render_options)


def add_alignment_track(bam_path: Path, panel: minidom.Element, doc: minidom.Document):
    track = doc.createElement("Track")
    track.setAttribute("attributeKey", f"{bam_path.name}")
    track.setAttribute("clazz", "org.broad.igv.sam.AlignmentTrack")
    track.setAttribute("color", "185,185,185")
    track.setAttribute("experimentType", "THIRD_GEN")
    track.setAttribute("fontSize", "10")
    track.setAttribute("id", f"{str(bam_path)}")
    track.setAttribute("name", f"{bam_path.name}")
    track.setAttribute("visible", "true")
    panel.appendChild(track)
    add_render_options(track, doc)


def add_panels_to_igv_session(doc: minidom.Document, bam_list: List[Path]):
    session = doc.getElementsByTagName('Session')[0]
    for idx, bam in enumerate(bam_list):
        panel = doc.createElement("Panel")
        panel.setAttribute("height", "887")
        panel.setAttribute("name", f"Panel{1711560405577 + idx}")
        panel.setAttribute("width", "1663")
        session.appendChild(panel)

        add_coverage_track(bam, panel, doc)
        add_alignment_track(bam, panel, doc)

    panel_attributes = doc.createElement("PanelLayout")
    panel_attributes.setAttribute("dividerFractions", divider_frac_str(len(bam_list)))
    session.appendChild(panel_attributes)


def doc_to_str(doc: minidom.Document) -> str:
    xml_str = doc.toprettyxml(indent="\t", encoding="utf-8")
    return xml_str


def create_igv_session(genome_path: Path, bam_path_list: List[Path]) -> str:
    xml_obj = initialize_igv_session(genome=genome_path)
    add_resources_to_igv_session(doc=xml_obj, resource_list=bam_path_list)
    add_panels_to_igv_session(doc=xml_obj, bam_list=bam_path_list)
    xml_string = doc_to_str(doc=xml_obj)
    return xml_string


if __name__ == "__main__":
    fasta_file = Path("pPRO-167-V2-0001.fasta")
    bam_file_list = [Path("pPRO-167-V2-0001_barcode09.bam"), Path("pPRO-167-V2-0001_barcode10.bam")]
    xml_str = create_igv_session(fasta_file, bam_file_list)
    with open("igv_session.xml", "wb") as f:
        f.write(xml_str)
