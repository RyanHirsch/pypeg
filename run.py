import os
import sys
import ffmpeg


filepath = os.path.abspath(sys.argv[1])
output_filepath = "{0}.gif".format(os.path.splitext(filepath)[0])

print(f"Converting to gif:")
print(f"  {filepath}")
print(f"  => {output_filepath}")


# https://trac.ffmpeg.org/wiki/FFprobeTips
probed = ffmpeg.probe(
    filepath, select_streams="v:0", show_entries="stream=width,height"
)

width = probed["streams"][0]["width"]
height = probed["streams"][0]["height"]

# https://engineering.giphy.com/how-to-make-gifs-with-ffmpeg/
#   -filter_complex "[0:v] fps=12,scale=360:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse
input = ffmpeg.input(filepath)
split = (
    input.video.filter_("fps", 12)
    .filter_("scale", w=width, h=-1)
    .filter_multi_output("split")
)
palette = ffmpeg.filter(split.stream(0), "palettegen")
(ffmpeg.filter([split.stream(1), palette], "paletteuse")).output(output_filepath).run(
    overwrite_output=True
)
