from src.file_utils import *
from src.responds import *

PROJECT_DIR = Path(__file__).parent.parent.resolve()
CV_STYLE = PROJECT_DIR / "pages/cv_style.css"


def get_cv_style(self, _method) -> None:
    msg = get_file_contents(CV_STYLE)
    respond_200(self, msg, "text/css")