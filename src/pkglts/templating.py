"""
Set of functions to extend jinja2.
"""
from os.path import exists
import re

OPENING_MARKER = "{" + "#"
CLOSING_MARKER = "#" + "}"

BLOCK_RE = re.compile(
    r"\{#[ ]pkglts,[ ](?P<key>[a-zA-Z0-9.]*)(?P<aft_head>.*?)\n(?P<cnt>.*?)#\}(?P<aft_foot>.*?(?=\n))",
    re.DOTALL | re.MULTILINE)


class TplBlock(object):
    """Simple container for templated blocks."""

    def __init__(self):
        self.before_header = ""
        self.bid = None
        self.after_header = ""
        self.content = ""
        self.before_footer = ""
        self.after_footer = ""

    def __str__(self):
        return "Block(\n|%s|%s|%s|\n|%s|\n|%s|%s|\n)" % (self.before_header,
                                                         self.bid,
                                                         self.after_header,
                                                         repr(self.content),
                                                         self.before_footer,
                                                         self.after_footer)

    def user_defined(self, cnt):
        """Make this block a user defined one.

        Args:
            cnt (str): content

        Returns:
            None
        """
        self.bid = None
        self.content = cnt


def parse_source(txt):
    """Parse text to find preserved blocks

    Args:
        txt (str): full text to parse

    Returns:
        (list of [str, str, str, str]): ordered list of blocks:
                    - block_id (or None if content is not preserved
                    - line start before start for preserved content
                    - content
                    - line start before end for preserved content
    """
    blocks = []
    last_end = 0

    for res in BLOCK_RE.finditer(txt):
        i = res.start()
        while i > last_end and txt[i] != "\n":
            i -= 1

        if i >= last_end:
            block = TplBlock()
            block.user_defined(txt[last_end: (i + 1)])
            blocks.append(block)

        bef = txt[(i + 1): res.start()]

        bid = res.group('key')
        aft_head = res.group('aft_head')
        cnt = res.group('cnt')
        aft_foot = res.group('aft_foot')

        i = len(cnt) - 1
        while i > 0 and cnt[i] != "\n":
            i -= 1
        aft = cnt[(i + 1): len(cnt)]
        cnt = cnt[:i]
        last_end = res.end() + 1

        block = TplBlock()
        block.bid = bid
        block.before_header = bef
        block.after_header = aft_head
        block.content = cnt
        block.before_footer = aft
        block.after_footer = aft_foot
        blocks.append(block)

    if last_end < len(txt):
        block = TplBlock()
        block.user_defined(txt[last_end: len(txt)])
        blocks.append(block)

    return blocks


def render(cfg, src_pth, tgt_pth):
    """Render src_pth templated file into tgt_pth

    Notes: keeps 'preserved' block structure

    Args:
        cfg (Config):  current package configuration
        src_pth (str): path to reference file
        tgt_pth (str): path to potentially non existent yet target file

    Returns:
        (list of [str, str]): key, cnt for preserved blocks
    """
    # parse src file to find 'preserved' blocks
    with open(src_pth, 'r') as fhr:
        src_blocks = parse_source(fhr.read())

    blocks = []
    if exists(tgt_pth):  # retrieves preserved blocks from source
        # parse tgt file to find 'preserved' blocks
        with open(tgt_pth, 'r') as fhr:
            tgt_blocks = parse_source(fhr.read())

        src_blocks = dict((b.bid, b) for b in src_blocks if b.bid is not None)
        for tgt_block in tgt_blocks:
            # check stored content hash
            if tgt_block.bid is not None:
                tgt_block.content = src_blocks[tgt_block.bid].content

            blocks.append(tgt_block)
    else:  # format non preserved blocks for the first and only time
        for block in src_blocks:
            if block.bid is None:
                block.content = cfg.render(block.content)

            blocks.append(block)

    # regenerate preserved block content
    preserved = []
    tgt = ""
    for block in blocks:
        if block.bid is None:
            tgt += block.content
        else:
            # format cnt
            cnt = cfg.render(block.content)
            preserved.append((block.bid, cnt))
            # rewrite preserved tag if necessary
            tgt += block.before_header + "{" + "# pkglts, %s" % block.bid + "%s\n" % block.after_header
            tgt += cnt
            tgt += "\n" + block.before_footer + "#" + "}%s\n" % block.after_footer

    with open(tgt_pth, 'w') as fhw:
        fhw.write(tgt)

    return preserved
