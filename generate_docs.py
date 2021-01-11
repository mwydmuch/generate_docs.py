#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_docs.py
Copyright (c) 2021 Marek Wydmuch
"""

import os
import click
import csv
from odf.opendocument import load
from odf import text, teletype


def replace_in_node(node, to_replace):
    node_text = teletype.extractText(node)

    new_text = False
    for k, v in to_replace.items():
        r = '{' + k + '}'
        if r in node_text:
            node_text = node_text.replace(r, v)
            new_text = True

    if new_text:
        if node.tagName == 'text:span':
            new_node = text.Span()
        elif node.tagName == 'text:p':
            new_node = text.P()
        else:
            raise TypeError("Unknown node type!")

        new_node.attributes = node.attributes
        new_node.addText(node_text)
        node.parentNode.insertBefore(new_node, node)
        node.parentNode.removeChild(node)


def replace_in_doc(in_path, out_path, to_replace):
    doc = load(in_path)

    # First replace in spans elements
    spans = doc.getElementsByType(text.Span)
    for s in spans:
        replace_in_node(s, to_replace)

    # Then replace in paragraphs
    ps = doc.getElementsByType(text.P)
    for p in ps:
        replace_in_node(p, to_replace)

    doc.save(out_path)


@click.command()
@click.option("-t", "--template_path", type=str, required=True, help="Path to ODT file with {} fields.")
@click.option("-c", "--content_path", type=str, required=True, help="Path to TSV or CSV file with data for the template.")
@click.option("-d", "--delimiter", type=str, default="\t", help="Delimiter for address book file.\t[default: '\\t']")
@click.option("-o", "--output_template", type=str, required=True, help="Output file path template. It should have odt, pdf, png, or jpg extension.")
@click.option("-k", "--keep_odt", type=bool, is_flag=True, help="Keep odt instead of removing them after conversion to the final file format.")
def generate_docs(template_path: str, content_path: str, delimiter: str, output_template: str, keep_odt: bool):
    # Check if conversion via lowriter to pdf/png/jpg is supported
    r_value = os.system("lowriter --version")
    lowriter = True
    if r_value != 0:
        lowriter = False
        print("Warning: LibreOffice is not installed, conversion to pdf, png and jpg format is unavailable!")

    # Generate documents
    with open(content_path, "r", encoding="utf-8") as content_file:
        content_reader = csv.DictReader(content_file, delimiter=delimiter)
        for to_replace in content_reader:
            odt_output_path = output_template.format(**to_replace)
            output_path = odt_output_path
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            if lowriter and output_path[-3:] != "odt":
                odt_output_path = odt_output_path[:-3] + "odt"

            replace_in_doc(template_path, odt_output_path, to_replace)

            if lowriter and output_path[-3:] != "odt":
                output_ext = output_path[-3:]
                os.system("lowriter --convert-to {} {}".format(output_ext, odt_output_path))
                os.rename(os.path.basename(output_path), output_path)
                if not keep_odt:
                    os.remove(odt_output_path)

            print("Successfully save file to:", output_path)


if __name__ == "__main__":
    generate_docs()
