from re import findall
from re import search

from json import dump

OPT_REGEX = r'( [a-z]+)(\.add_option\()(.*?)(\))'
OPTION_NAMES_REGEX = r"('-{1,2})(.*?)(')"
DEST_REGEX = r"(dest=')(.*?)(')"
OTHER_REGEX = r"([a-z]+=')(.*?)(')"


with open("src/ytb/yt-dlp-options.py", "r", encoding="utf-8") as _:
    content = _.read().replace("\n", "")

opt_dict = {}

for ind, match in enumerate(findall(OPT_REGEX, content)):
    option_names = []
    if search(OPTION_NAMES_REGEX, match[2]):
        option_names = [i[1] for i in findall(OPTION_NAMES_REGEX, match[2])]

    other_values = {}
    if search(OTHER_REGEX, match[2]):
        other_values = {i[0][:-2]: i[1] for i in findall(OTHER_REGEX, match[2])}

    opt_dict[ind] = {
        "category": match[0].strip(),
        "dest": "" if not search(DEST_REGEX, match[2]) else search(DEST_REGEX, match[2]).group(2),
        "option_names": option_names,
        "other_values": other_values
    }

with open("src/ytb/yt-dlp-options.json", "w", encoding="utf-8") as _:
    dump(opt_dict, _, indent=4)
