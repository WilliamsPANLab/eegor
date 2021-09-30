from pathlib import Path
import eegor.report.data as template_folder
from eegor.utils.figure import embed_html


template_folder = Path(template_folder.__file__).parent


def open_template():
    with open(template_folder / "template.html", "r") as f:
        return "".join(f.readlines())


def individual_report(subject, num_dropped_epochs, num_poor_channels,
                      freq_open_fig, freq_closed_fig):
    freq_open_png = embed_html(freq_open_fig)
    freq_closed_png = embed_html(freq_closed_fig)

    template = open_template()
    report = template.format(subject=subject,
                             num_dropped_epochs=num_dropped_epochs,
                             num_poor_channels=num_poor_channels,
                             freq_open_png=freq_open_png,
                             freq_closed_png=freq_closed_png)
    return report
