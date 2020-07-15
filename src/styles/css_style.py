import src.common.paths as paths
import src.common.responds as responds
import src.utils.file_utils as fu


def get_cv_style(self, _method) -> None:
    msg = fu.get_file_contents(paths.CV_STYLE)
    responds.respond_200(self, msg, "text/css")
