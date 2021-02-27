from getyt import get_video_info
from getyt import _getyt_init
import common


confidentials = common.read_json("doc/confidentials.json")
config = common.read_json("doc/config.json")
video_id = "wfhOmvXL0i0"
file_name = "D:/123\\youtube-dl fKp66a5MCco 248 乃木坂46掛橋沙耶香、衣装脱ぎ捨てボクサーに！岡山出身の4期生がCM単独初出演　鋭いパンチ連発！.mkv"


#wfhOmvXL0i0
_getyt_init(confidentials)
video_info_list = []
video_info_list = get_video_info(video_id)

_ = video_info_list[2]
#t = "2020-07-07T02:00:02Z"


#duration = dateutil.parser.parse('2020-07-07T02:00:02Z')

common.d2s("PT3M54S")


print(common.d2s("PT3M54S"))