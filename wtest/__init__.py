
from .pre import write_pre
from .end import write_end
from .middle import write_middle


def write_test(root,ojson):
    write_pre(root, ojson)
    write_middle(root, ojson)
    write_end(root, ojson)
    pass

