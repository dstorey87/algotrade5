"""
Jinja2 rendering utils, used to generate new strategy and configurations.
"""


def render_template(templatefile: str, arguments: dict) -> str:
    from jinja2 import Environment, PackageLoader, select_autoescape

    env = Environment(
        loader=PackageLoader("freqtrade", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(templatefile)
    return template.render(**arguments)


# REMOVED_UNUSED_CODE: def render_template_with_fallback(
# REMOVED_UNUSED_CODE:     templatefile: str, templatefallbackfile: str, arguments: dict | None = None
# REMOVED_UNUSED_CODE: ) -> str:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Use templatefile if possible, otherwise fall back to templatefallbackfile
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     from jinja2.exceptions import TemplateNotFound
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     if arguments is None:
# REMOVED_UNUSED_CODE:         arguments = {}
# REMOVED_UNUSED_CODE:     try:
# REMOVED_UNUSED_CODE:         return render_template(templatefile, arguments)
# REMOVED_UNUSED_CODE:     except TemplateNotFound:
# REMOVED_UNUSED_CODE:         return render_template(templatefallbackfile, arguments)
