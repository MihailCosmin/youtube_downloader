from re import findall
from re import search

from json import dump
from json import load

OPT_REGEX = r'( [a-z]+)(\.add_option\()(.*?)(\))'
OPTION_NAMES_REGEX = r"('-{1,2})(.*?)(')"
DEST_REGEX = r"(dest=')(.*?)(')"
OTHER_REGEX = r"([a-z]+=)(.*?)(,)"


with open("src/ytb/yt-dlp-options.py", "r", encoding="utf-8") as _:
    content = _.read().replace("\n", "")

opt_dict = {}

arguments = []
for ind, match in enumerate(findall(OPT_REGEX, content)):
    # print(match)
    print([entry for entry in match[2].split(",")])


# for ind, match in enumerate(findall(OPT_REGEX, content)):
#     option_names = []
#     if search(OPTION_NAMES_REGEX, match[2]):
#         option_names = [i[1] for i in findall(OPTION_NAMES_REGEX, match[2])]

#     other_values = {"default": None}
#     if search(OTHER_REGEX, match[2]):
#         other_values |= {i[0][:-1].replace("'", ""): i[1] for i in findall(OTHER_REGEX, match[2])}

#     opt_dict[ind] = {
#         "category": match[0].strip(),
#         "dest": "" if not search(DEST_REGEX, match[2]) else search(DEST_REGEX, match[2]).group(2),
#         "option_names": option_names,
#         "other_values": other_values
#     }

# with open("src/ytb/yt-dlp-options_2.json", "w", encoding="utf-8") as _:
#     dump(opt_dict, _, indent=4)

# with open("src/ytb/yt-dlp-options_2.json", "r", encoding="utf-8") as _:
#     opt = load(_)

# new_dict = {}
# for value in opt.values():
#     new_dict[value["dest"]] = {
#         "category": value["category"],
#         "type": value["other_values"]["type"] if "type" in value["other_values"] else "bool" if value["other_values"]["default"] in ("True", "False") else "str",
#         "default": value["other_values"]["default"] if "default" in value["other_values"] else "",
#         "description": value["other_values"]["help"] if "help" in value["other_values"] else "",
#     }

# with open("src/ytb/yt-dlp-options5.json", "w", encoding="utf-8") as _:
#     dump(new_dict, _, indent=4)
