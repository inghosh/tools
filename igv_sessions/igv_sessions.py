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


def add_panels_to_igv_session(doc: minidom.Document, bam_list: List[Path]):
    session = doc.getElementsByTagName('Session')[0]
    for idx, bam in enumerate(bam_list):
        panel = doc.createElement("Panel")
        panel.setAttribute("height", "887")
        panel.setAttribute("name", f"Panel{1711560405577 + idx}")
        panel.setAttribute("width", "1663")
        session.appendChild(panel)

        track1 = doc.createElement("Track")
        track1.setAttribute("attributeKey", f"{bam.name} Coverage")
        track1.setAttribute("autoScale", "true")
        track1.setAttribute("clazz", "org.broad.igv.sam.CoverageTrack")
        track1.setAttribute("fontSize", "10")
        track1.setAttribute("id", f"{str(bam)}_coverage")
        track1.setAttribute("name", f"{bam.name} Coverage")
        track1.setAttribute("snpThreshold", "0.2")
        track1.setAttribute("visible", "true")
        panel.appendChild(track1)

        data_range = doc.createElement("DataRange")
        track1.appendChild(data_range)

        track2 = doc.createElement("Track")
        track2.setAttribute("attributeKey", f"{bam.name}")
        track2.setAttribute("clazz", "org.broad.igv.sam.AlignmentTrack")
        track2.setAttribute("color", "185,185,185")
        track2.setAttribute("experimentType", "THIRD_GEN")
        track2.setAttribute("fontSize", "10")
        track2.setAttribute("id", f"{str(bam)}")
        track2.setAttribute("name", f"{bam.name}")
        track2.setAttribute("visible", "true")
        panel.appendChild(track2)

        render_options = doc.createElement("RenderOptions")
        track2.appendChild(render_options)

    panel_attributes = doc.createElement("PanelLayout")
    div_fracs = ", ".join([str(x/len(bam_list)) for x in range(1 + len(bam_list))])
    panel_attributes.setAttribute("dividerFractions", div_fracs)
    session.appendChild(panel_attributes)


def doc_to_str(doc: minidom.Document) -> str:
    xml_str = doc.toprettyxml(indent="\t")
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
    with open("igv_session.xml", "w") as f:
        f.write(xml_str)
