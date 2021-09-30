import base64
from io import BytesIO


def embed_html(fig, dst):
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
    return f"<img src='data:image/png;base64,{encoded}'>"
