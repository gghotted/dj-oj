from django.utils.html import format_html, format_html_join


def html_help_text(*help_texts):
    help_items = format_html_join(
        "", "<li>{}</li>", ((help_text,) for help_text in help_texts)
    )
    return format_html("<ul>{}</ul>", help_items) if help_items else ""
