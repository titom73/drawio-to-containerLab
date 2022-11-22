#!/usr/bin/python
# coding: utf-8 -*-

import sys
import os
import logging
import jinja2


__author__ = "titom73"
__version__ = 0.1


def templater(lab_name, lab_image, nodes_yaml, links_yaml, template_file="CLAB_TEMPLATE.j2"):
    # templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
    template_path = '%s/templates/'% os.path.dirname(__file__)
    templateLoader = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path),
                                        autoescape=jinja2.select_autoescape(),
                                        trim_blocks=True,
                                        lstrip_blocks=True)
    try:
        template = templateLoader.get_template(template_file)
    except jinja2.TemplateNotFound as error:
        logging.error("Template not found in %s", str(template_path))
    else:
        return template.render(
            lab_name=lab_name,
            lab_image=lab_image,
            nodes_yaml=nodes_yaml,
            links_yaml=links_yaml
        )
    return None