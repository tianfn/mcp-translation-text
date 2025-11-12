"""Translation MCP Provider implementation.

提供基于小牛翻译（Niutrans）API 的文本翻译服务，支持 450+ 种语言互译。
"""
import os
from typing import Any, Dict, List, Tuple, Annotated

import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import Field

__all__ = ["mcp", "main"]

# Create an MCP server
mcp = FastMCP("Niutrans Translation")

DEFAULT_NIUTRANS_API_URL = "https://api.niutrans.com/NiuTransServer/translation"


LANGUAGE_ENTRIES: List[Tuple[str, str, str]] = [
    ("自动检测", "Auto Detect", "auto"),
    ("阿尔巴尼亚语", "Albanian", "sq"),
    ("阿拉伯语", "Arabic", "ar"),
    ("阿姆哈拉语", "Amharic", "am"),
    ("阿丘雅语", "Achuar", "acu"),
    ("阿瓜鲁纳语", "Aguaruna", "agr"),
    ("阿卡瓦伊语", "Akawaio", "ake"),
    ("阿穆斯戈语", "Amuzgo", "amu"),
    ("阿塞拜疆语", "Azerbaijani", "az"),
    ("爱尔兰语", "Irish", "ga"),
    ("爱沙尼亚语", "Estonian", "et"),
    ("埃维语", "Ewe", "ee"),
    ("奥吉布瓦语", "Ojibwa", "ojb"),
    ("奥罗莫语", "Oromoo", "om"),
    ("奥利亚语", "Oriya", "or"),
    ("奥赛梯语", "Ossetic", "os"),
    ("阿雅安伊富高语", "Ayangan Ifugao", "ifb"),
    ("艾马拉语", "Aymara", "aym"),
    ("阿卡特克语", "Acateco", "knj"),
    ("安蒂波洛伊富高语", "Antipolo Ifugao", "ify"),
    ("阿奇语", "Achi", "acr"),
    ("安拜语", "Ambai", "amk"),
    ("奥罗科语", "Oroko", "bdu"),
    ("阿多拉语", "Adhola", "adh"),
    ("阿格尼桑维语", "Agni Sanvi", "any"),
    ("阿舍宁卡语", "Asheninka", "cpb"),
    ("埃菲克语", "Efik", "efi"),
    ("阿乔利语", "Acholi", "ach"),
    ("埃桑语", "Esan", "ish"),
    ("埃多语", "Edo", "bin"),
    ("阿卢尔语", "Alur", "alz"),
    ("阿亚库乔克丘亚语", "Ayacucho Quechua", "quy"),
    ("奥克语", "Occitan", "oc"),
    ("阿斯图里亚斯语", "Asturian", "ast"),
    ("阿拉贡语", "Aragonese", "an"),
    ("阿法尔语", "Afar", "aa"),
    ("阿尔及利亚阿拉伯语", "Algerian Arabic", "arq"),
    ("阿布哈兹语", "Abkhaz", "ab"),
    ("巴布亚皮钦语", "Tok Pisin", "tpi"),
    ("巴拉萨纳语", "Barasana", "bsn"),
    ("巴什基尔语", "Bashkir", "ba"),
    ("巴斯克语", "Basque", "eu"),
    ("白俄罗斯语", "Belarusian", "be"),
    ("白苗文", "Hmong", "mww"),
    ("柏柏尔语", "Berber", "ber"),
    ("保加利亚语", "Bulgarian", "bg"),
    ("冰岛语", "Icelandic", "is"),
    ("比斯拉马语", "Bislama", "bi"),
    ("别姆巴语", "Bemba", "bem"),
    ("波兰语", "Polish", "pl"),
    ("波斯尼亚语", "Bosnian", "bs"),
    ("波斯语", "Persian", "fa"),
    ("波塔瓦托米语", "Potawatomi", "pot"),
    ("布列塔尼语", "Breton", "br"),
    ("波孔奇语", "Poqomchi'", "poh"),
    ("班巴拉语", "Bambara", "bam"),
    ("北部马姆语", "Northern Mam", "map"),
    ("巴里巴语", "Bariba", "bba"),
    ("博科巴鲁语", "Bokobaru", "bus"),
    ("布萨语", "Busa", "bqp"),
    ("波拉语", "Bola", "bnp"),
    ("巴里亚语", "Bariai", "bch"),
    ("班通安隆语", "Bantoanon", "bno"),
    ("班迪亚勒语", "Bandial", "bqj"),
    ("巴卡语", "Baka", "bdh"),
    ("邦邦语", "Bambam", "ptu"),
    ("巴里语", "Bari", "bfa"),
    ("布阿尔考钦语", "Bualkhaw Chin", "cbl"),
    ("北部格雷博语", "Northern Grebo", "gbo"),
    ("巴萨语", "Basaa", "bas"),
    ("布卢语", "Bulu", "bum"),
    ("邦阿西楠语", "Pangasinan", "pag"),
    ("鲍勒语", "Baoule", "bci"),
    ("比亚克语", "Biak", "bhw"),
    ("巴塔克卡罗语", "Batak Karo", "btx"),
    ("波纳佩语", "Pohnpeian", "pon"),
    ("伯利兹克里奥尔语", "Belizean Creole", "bzj"),
    ("巴拉圭瓜拉尼语", "Paraguayan Guarani", "gug"),
    ("北部普埃布拉纳瓦特语", "Northern Puebla Nahuatl", "ncj"),
    ("巴西葡萄牙语", "Brazilian Portuguese", "pt-BR"),
    ("邦板牙语", "Pampanga", "pam"),
    ("北索托语", "Northern Sotho", "nso"),
    ("北萨米语", "Northern Sami", "se"),
    ("查莫罗语", "Chamorro", "cha"),
    ("楚瓦什语", "Chuvash", "cv"),
    ("茨瓦纳语", "Tswana", "tn"),
    ("聪加语", "Xitsonga", "ts"),
    ("车臣语", "Chechen", "che"),
    ("查克玛语", "Chakma", "ccp"),
    ("茨鲁语", "Chiru", "cdf"),
    ("茨瓦语", "Tswa", "tsc"),
    ("楚瓦博语", "Chuwabu", "chw"),
    ("鞑靼语", "Tatar", "tt"),
    ("丹麦语", "Danish", "da"),
    ("德语", "German", "de"),
    ("德顿语", "Tetun", "tet"),
    ("迪维希语", "Divehi", "dv"),
    ("丁卡语", "Dinka", "dik"),
    ("迪尤拉语", "Dyula", "dyu"),
    ("迪塔马利语", "Ditammari", "tbz"),
    ("达迪比语", "Dadibi", "mps"),
    ("蒂穆贡-穆鲁特语", "Timugon Murut", "tih"),
    ("东部卡加延-阿格塔语", "Eastern Cagayan Agta", "duo"),
    ("丹美语", "Dangme", "ada"),
    ("杜阿拉语", "Duala", "dua"),
    ("帝力德顿语", "Tetun Dili", "tdt"),
    ("德鲁语", "Drehu", "dhv"),
    ("蒂夫语", "Tiv", "tiv"),
    ("多巴巴塔克语", "Toba Batak", "bbc"),
    ("地峡萨波特克语", "Isthmus Zapotec", "zai"),
    ("低地德语", "Low German", "nds"),
    ("道本语", "Toki Pona", "toki"),
    ("俄语", "Russian", "ru"),
    ("恩都卡语", "Ndyuka", "djk"),
    ("恩舍特语", "Enxet", "enx"),
    ("恩泽马语", "Nzema", "nzi"),
    ("恩加朱语", "Ngaju", "nij"),
    ("恩科里语", "Nkore", "nyn"),
    ("恩道语", "Ndau", "ndc"),
    ("恩敦加语", "Ndonga", "ndo"),
    ("法语", "French", "fr"),
    ("法罗语", "Faroese", "fo"),
    ("菲律宾语", "Filipino", "fil"),
    ("斐济语", "Fijian", "fj"),
    ("芬兰语", "Finnish", "fi"),
    ("法兰钦语", "Falam Chin", "cfm"),
    ("法拉法拉语", "Frafra", "gur"),
    ("佛得角克里奥尔语", "Cape Verdean Creole", "kea"),
    ("丰语", "Fon", "fon"),
    ("弗留利语", "Friulian", "fur"),
    ("法兰克-普罗旺斯语", "Franco-Provençal", "frp"),
    ("梵语", "Sanskrit", "sa"),
    ("高棉语", "Khmer", "km"),
    ("盖丘亚语", "Quichua", "quw"),
    ("刚果语", "Kikongo", "kg"),
    ("弗里西语", "Frisian", "fy"),
    ("格鲁吉亚语", "Georgian", "jy"),
    ("古吉拉特语", "Gujarati", "gu"),
    ("瓜哈哈拉语", "Guajajara", "gub"),
    ("果发语", "Goffa", "gof"),
    ("格森语", "Kasem", "xsm"),
    ("格巴亚语", "Gbaya", "krs"),
    ("龚语", "Gun", "guw"),
    ("刚果斯瓦希里语", "Congo Swahili", "swc"),
    ("圭米语", "Guaymi", "gym"),
    ("瓜拉尼语", "Guarani", "gn"),
    ("格陵兰语", "Kalaallisut", "kl"),
    ("高原马达加斯加语", "Plateau Malagasy", "plt"),
    ("古英语", "Old English", "ang"),
    ("哈萨克语", "Kazakh", "ka"),
    ("哈萨克语(西里尔)", "Kazakh (Cyrillic)", "kk"),
    ("海地克里奥尔语", "Haitian Creole", "ht"),
    ("韩语", "Korean", "ko"),
    ("豪萨语", "Hausa", "ha"),
    ("荷兰语", "Dutch", "nl"),
    ("黑山语", "Montenegrin", "me"),
    ("哈卡钦语", "Hakha Chin", "cnh"),
    ("胡里语", "Huli", "hui"),
    ("亥比语", "Halbi", "hlb"),
    ("赫雷罗语", "Herero", "her"),
    ("胡帕语", "Hupa", "hup"),
    ("吉尔吉斯语", "Kyrgyz", "ky"),
    ("基切语", "Kiche", "quc"),
    ("加莱拉语", "Galela", "gbi"),
    ("加利西亚语", "Galician", "gl"),
    ("加泰罗尼亚语", "Catalan", "ca"),
    ("捷克语", "Czech", "cs"),
    ("基里巴斯语", "Kiribati", "gil"),
    ("景颇语", "Jingpho", "kac"),
    ("加语", "Ga", "gaa"),
    ("基库尤语", "Kikuyu", "kik"),
    ("金邦杜语", "Kimbundu", "kmb"),
    ("加利富纳语", "Garifuna", "cab"),
    ("加拿大法语", "Canadian French", "fr-CA"),
    ("卡拜尔语", "Kabyle", "kab"),
    ("卡韦卡尔语", "Cabecar", "cjp"),
    ("卡克奇克尔语", "Cakchiquel", "cak"),
    ("卡纳达语", "Kannada", "kn"),
    ("凯克其语", "Qeqchi", "kek"),
    ("坎帕语", "Campa", "cni"),
    ("科普特语", "Coptic", "cop"),
    ("科奇语", "Camsa", "kbh"),
    ("科西嘉语", "Corsican", "co"),
    ("克雷塔罗奥托米语", "Queretaro Otomi", "otq"),
    ("克罗地亚语", "Croatian", "hr"),
    ("库尔德语(库尔曼奇语)", "Kurdish (Kurmanji)", "ku"),
    ("库尔德语(索拉尼语)", "Kurdish (Sorani)", "ckb"),
    ("库阿努阿语", "Kuanua", "ksd"),
    ("库斯科克丘亚语", "Cusco Quechua", "quz"),
    ("卡平阿马朗伊语", "Kapingamarangi", "kpg"),
    ("克里米亚鞑靼语", "Crimean Tatar", "crh"),
    ("卡尔梅克卫拉特语", "Kalmyk-Oirat", "xal"),
    ("克利科语", "Keliko", "kbo"),
    ("卡库瓦语", "Kakwa", "keo"),
    ("喀克其奎语", "Kaqchikel", "cki"),
    ("卡乌龙语", "Kaulong", "pss"),
    ("库隆语", "Kulung", "kle"),
    ("卡纳尔高地-基丘亚语", "Canar Highland Quichua", "qxr"),
    ("库克群岛毛利语", "Cook Islands Maori", "rar"),
    ("卡比耶语", "Kabiye", "kbp"),
    ("卡姆巴语", "Kamba", "kam"),
    ("卡昂多语", "Kaonde", "kqn"),
    ("喀麦隆皮钦语", "Cameroonian Pidgin", "wes"),
    ("宽亚玛语", "Kwanyama", "kua"),
    ("克林贡语", "Klingon", "tlh"),
    ("卡努里语", "Kanuri", "kr"),
    ("康沃尔语", "Cornish", "kw"),
    ("卡舒比语", "Kashubian", "csb"),
    ("卢旺达语", "Kinyarwanda", "rw"),
    ("拉丁语", "Latin", "la"),
    ("拉脱维亚语", "Latvian", "lv"),
    ("老挝语", "Lao", "lo"),
    ("隆迪语", "Kirundi", "rn"),
    ("立陶宛语", "Lithuanian", "lt"),
    ("林加拉语", "Lingala", "ln"),
    ("卢干达语", "Luganda", "lg"),
    ("卢克帕语", "Lukpa", "dop"),
    ("卢森堡语", "Luxembourgish", "lb"),
    ("罗马尼亚语", "Romanian", "ro"),
    ("罗姆语", "Romani", "rmn"),
    ("隆韦语", "Lomwe", "ngl"),
    ("罗维那语", "Roviana", "rug"),
    ("勒期语", "Lacid", "lsi"),
    ("临高语", "Lingao", "ond"),
    ("罗子语", "Lozi", "loz"),
    ("卢巴开赛语", "Luba-Kasai", "lua"),
    ("卢巴-加丹加语", "Luba-Katanga", "lub"),
    ("隆打语", "Lunda", "lun"),
    ("卢乌德语", "Ruund", "rnd"),
    ("卢瓦来语", "Luvale", "lue"),
    ("林堡语", "Limburgs", "li"),
    ("逻辑语", "Lojban", "jbo"),
    ("马尔加什语", "Malagasy", "mg"),
    ("马耳他语", "Maltese", "mt"),
    ("马恩岛语", "Manx", "gv"),
    ("马拉地语", "Marathi", "mr"),
    ("马拉雅拉姆语", "Malayalam", "ml"),
    ("马来语", "Malay", "ms"),
    ("马里语", "Mari", "mhr"),
    ("马姆语", "Mam", "mam"),
    ("马其顿语", "Macedonian", "mk"),
    ("毛利语", "Maori", "mi"),
    ("蒙古语", "Mongolian", "mo"),
    ("蒙古语(西里尔)", "Mongolian (Cyrillic)", "mn"),
    ("缅甸语", "Burmese", "my"),
    ("孟加拉语", "Bengali", "bn"),
    ("曼尼普尔语", "Manipuri", "mni"),
    ("摩图语", "Motu", "meu"),
    ("马绍尔语", "Marshallese", "mah"),
    ("马拉瑙语", "Maranao", "mrw"),
    ("马勒语", "Maale", "mdy"),
    ("马都拉语", "Madurese", "mad"),
    ("莫西语", "Mossi", "mos"),
    ("穆图凡语", "Muthuvan", "muv"),
    ("米佐语", "Mizo", "lus"),
    ("毛里求斯克里奥尔语", "Mauritian Creole", "mfe"),
    ("姆班杜语", "Umbundu", "umb"),
    ("马普切语", "Mapuche", "arn"),
    ("米斯特克语", "Metlatonoc Mixtec", "mxv"),
    ("马库阿语", "Makhuwa", "vmw"),
    ("曼代灵西马隆贡语", "Batak Simalungun", "bts"),
    ("曼布韦-龙古语", "Mambwe-Lungu", "mgr"),
    ("门诺低地德语", "Plautdietsch", "pdt"),
    ("米兰达语", "Mirandese", "mwl"),
    ("迈蒂利语", "Maithili", "mai"),
    ("马来语克里奥尔语", "Malay trade and creole", "crp"),
    ("纳瓦特尔语", "Nahuatl", "nhg"),
    ("南非荷兰语", "Afrikaans", "af"),
    ("南非科萨语", "Xhosa", "xh"),
    ("南非祖鲁语", "Zulu", "zu"),
    ("尼泊尔语", "Nepali", "ne"),
    ("挪威语", "Norwegian", "no"),
    ("南阿塞拜疆语", "South Azerbaijani", "azb"),
    ("南玻利维亚克丘亚语", "South Bolivian Quechua", "quh"),
    ("弄巴湾语", "Lun Bawang", "lnd"),
    ("尼日利亚富拉语", "Nigerian Fulfulde", "fuv"),
    ("努曼干语", "Numanggang", "nop"),
    ("纳特尼语", "Nateni", "ntm"),
    ("尼亚库萨语", "Nyakyusa", "nyy"),
    ("纽埃语", "Niuean", "niu"),
    ("尼亚斯语", "Nias", "nia"),
    ("涅姆巴语", "Nyemba", "nba"),
    ("尼荣圭语", "Nyungwe", "nyu"),
    ("纳瓦霍语", "Navajo", "nav"),
    ("尼亚内卡语", "Nyaneka", "nyk"),
    ("尼日利亚皮钦语", "Nigerian Pidgin", "pcm"),
    ("南恩德贝莱语", "Southern Ndebele", "nr"),
    ("帕皮阿门托语", "Papiamento", "pap"),
    ("派特语", "Paite", "pck"),
    ("旁遮普语", "Punjabi", "pa"),
    ("葡萄牙语", "Portuguese", "pt"),
    ("普什图语", "Pashto", "ps"),
    ("佩勒-阿塔语", "Pele-Ata", "ata"),
    ("皮京语", "Pijin", "pis"),
    ("帕潘特拉托托纳克语", "Papantla Totonac", "top"),
    ("齐切瓦语", "Chewa", "ny"),
    ("契维语", "Twi", "tw"),
    ("切诺基语", "Cherokee", "chr"),
    ("奇南特克语", "Chinantec", "chq"),
    ("齐马内语", "Tsimane", "cas"),
    ("乔奎语", "Chokwe", "cjk"),
    ("乔皮语", "Chopi", "cce"),
    ("丘克语", "Chuukese", "chk"),
    ("钦博拉索高地克丘亚语", "Chimborazo Highland Quichua", "qug"),
    ("恰蒂斯加尔语", "Chhattisgarhi", "hne"),
    ("日语", "Japanese", "ja"),
    ("瑞典语", "Swedish", "sv"),
    ("萨摩亚语", "Samoan", "sm"),
    ("塞尔维亚语", "Serbian", "sr"),
    ("塞舌尔克里奥尔语", "Seychelles Creole", "crs"),
    ("塞索托语", "Sesotho", "st"),
    ("桑戈语", "Sango", "sg"),
    ("僧伽罗语", "Sinhalese", "si"),
    ("山地马里语", "Hill Mari", "mrj"),
    ("世界语", "Esperanto", "eo"),
    ("舒阿尔语", "Shuar", "jiv"),
    ("斯洛伐克语", "Slovak", "sk"),
    ("斯洛文尼亚语", "Slovenian", "sl"),
    ("斯瓦希里语", "Swahili", "sw"),
    ("苏格兰盖尔语", "Scottish Gaelic", "gd"),
    ("索马里语", "Somali", "so"),
    ("苏奥语", "Suau", "swp"),
    ("桑贝里吉语", "Samberigi", "ssx"),
    ("萨鲍特语", "Sabaot", "spy"),
    ("圣马特奥德马尔-瓦维语", "San Mateo del Mar Huave", "huv"),
    ("斯哈语", "Kisiha", "jmc"),
    ("萨拉马坎语", "Saramaccan", "srm"),
    ("桑格语", "Sangir", "sxn"),
    ("塞纳语", "Sena", "seh"),
    ("圣萨尔瓦多刚果语", "San Salvador Kongo", "kwy"),
    ("松格语", "Songe", "sop"),
    ("索西语", "Tzotzil", "tzo"),
    ("斯高克伦语", "S'gaw Karen", "ksw"),
    ("苏格兰语(低地苏格兰语)", "Scots", "sco"),
    ("书面挪威语", "Bokmal", "nb"),
    ("撒丁语", "Sardinian", "sc"),
    ("掸语", "Shan", "shn"),
    ("塞尔维亚-克罗地亚语", "Serbo-Croatian", "sh"),
    ("斯威士语", "Swazi", "ss"),
    ("上索布语", "Upper Sorbian", "hsb"),
    ("塔吉克语", "Tajik", "tg"),
    ("塔希提语", "Tahitian", "ty"),
    ("泰卢固语", "Telugu", "te"),
    ("泰米尔语", "Tamil", "ta"),
    ("泰语", "Thai", "th"),
    ("汤加语", "Tongan", "to"),
    ("提格雷语", "Tigre", "tig"),
    ("图阿雷格语", "Tamajaq", "tmh"),
    ("土耳其语", "Turkish", "tr"),
    ("土库曼语", "Turkmen", "tk"),
    ("坦普尔马语", "Tampulma", "tpm"),
    ("特丁钦语", "Tedim Chin", "ctd"),
    ("图瓦语", "Tuvan", "tyv"),
    ("图马伊鲁穆语", "Tuma-Irumu", "iou"),
    ("腾内特语", "Tennet", "tex"),
    ("通加格语", "Tungag", "lcm"),
    ("特索语", "Teso", "teo"),
    ("图瓦卢语", "Tuvaluan", "tvl"),
    ("特特拉语", "Tetela", "tll"),
    ("他加禄语", "Tagalog", "tgl"),
    ("通布卡语", "Tumbuka", "tum"),
    ("托霍拉瓦尔语", "Tojolabal", "toj"),
    ("土柔语", "Tooro", "ttj"),
    ("瓦拉莫语", "Wolaytta", "wal"),
    ("瓦瑞语", "Waray", "war"),
    ("文达语", "Venda", "ve"),
    ("沃洛夫语", "Wolof", "wol"),
    ("乌德穆尔特语", "Udmurt", "udm"),
    ("乌尔都语", "Urdu", "ur"),
    ("乌克兰语", "Ukrainian", "uk"),
    ("乌兹别克语", "Uzbek", "uz"),
    ("乌玛语", "Uma", "ppk"),
    ("乌斯潘坦语", "Uspanteco", "usp"),
    ("瓦利语", "Wali", "wlx"),
    ("佤语", "Wa", "prk"),
    ("瓦吉语", "Waskia", "wsk"),
    ("瓦里斯语", "Waris", "wrs"),
    ("文约语", "Vunjo", "vun"),
    ("威尔士语", "Welsh", "cy"),
    ("瓦利斯语", "Wallisian", "wls"),
    ("乌尔霍博语", "Urhobo", "urh"),
    ("瓦乌特拉马萨特克语", "Huautla Mazatec", "mau"),
    ("瓦尤语", "Wayuu", "guc"),
    ("瓦隆语", "Walon", "wa"),
    ("西班牙语", "Spanish", "es"),
    ("希伯来语", "Hebrew", "he"),
    ("希尔哈语", "Tachelhit", "shi"),
    ("希腊语", "Greek", "el"),
    ("夏威夷语", "Hawaiian", "haw"),
    ("信德语", "Sindhi", "sd"),
    ("匈牙利语", "Hungarian", "hu"),
    ("修纳语", "Shona", "sn"),
    ("宿务语", "Cebuano", "ceb"),
    ("叙利亚语", "Syriac", "syc"),
    ("夏威夷克里奥尔英语", "Hawaiian Creole English", "hwc"),
    ("希里莫图语", "Hiri Motu", "hmo"),
    ("西部拉威语", "Western Lawa", "lcp"),
    ("锡达莫语", "Sidamo", "sid"),
    ("西布基农马诺布语", "Western Bukidnon Manobo", "mbb"),
    ("西皮沃语", "Shipibo", "shp"),
    ("西罗伊语", "Siroi", "ssd"),
    ("西部玻利维亚瓜拉尼语", "Western Bolivian Guarani", "gnw"),
    ("西部克耶语", "Western Kayah", "kyu"),
    ("希利盖农语", "Hiligaynon", "hil"),
    ("新挪威语", "Nynorsk", "nn"),
    ("下索布语", "Lower Sorbian", "dsb"),
    ("新通用语", "Lingua Franca Nova", "lfn"),
    ("西方国际语", "Interlingue", "ie"),
    ("亚美尼亚语", "Armenian", "hy"),
    ("雅加达语", "Jakalteko", "jac"),
    ("亚齐语", "Aceh", "ace"),
    ("伊博语", "Igbo", "ig"),
    ("意大利语", "Italian", "it"),
    ("意第绪语", "Yiddish", "yi"),
    ("印地语", "Hindi", "hi"),
    ("印尼巽他语", "Sundanese", "su"),
    ("印尼语", "Indonesian", "id"),
    ("印尼爪哇语", "Javanese", "jv"),
    ("英语", "English", "en"),
    ("尤卡坦玛雅语", "Yucatec Maya", "yua"),
    ("约鲁巴语", "Yoruba", "yo"),
    ("越南语", "Vietnamese", "vi"),
    ("粤语", "Cantonese", "yue"),
    ("伊卡语", "Ika", "ikk"),
    ("伊兹语", "Izi", "izz"),
    ("约姆语", "Yom", "pil"),
    ("雅比姆语", "Yabem", "jae"),
    ("永贡语", "Yongkom", "yon"),
    ("邕北壮语", "Yongbei Zhuang", "zyb"),
    ("伊普马语", "Yipma", "byr"),
    ("伊索科语", "Isoko", "iso"),
    ("伊班语", "Iban", "iba"),
    ("伊洛卡诺语", "Ilocano", "ilo"),
    ("伊巴纳格语", "Ibanag", "ibg"),
    ("雅浦语", "Yapese", "yap"),
    ("因巴布拉高地克丘亚语", "Imbabura Highland Quichua", "qvi"),
    ("伊多语", "Ido", "io"),
    ("因特语", "Interlingua", "ia"),
    ("哲尔马语", "Zarma", "dje"),
    ("中文", "Chinese (Simplified)", "zh"),
    ("中文(繁体)", "Chinese (Traditional)", "cht"),
    ("宗喀语", "Dzongkha", "dz"),
    ("中部伊富高语", "Central Ifugao", "ifa"),
    ("佐通钦语", "Zotung Chin", "czt"),
    ("中部杜顺语", "Central Dusun", "dtp"),
    ("中比科尔语", "Central Bikol", "bcl"),
    ("泽塔尔语", "Tzeltal", "tzh"),
    ("赞德语", "Zande", "zne"),
    ("中部普埃布拉纳瓦特语", "Central Puebla Nahuatl", "ncx"),
    ("中部瓦斯特克纳瓦特语", "Central Huasteca Nahuatl", "nch"),
    ("中古法语", "Middle French", "frm"),
]


def _normalize_alias(value: str) -> str:
    normalized = value.strip().lower()
    normalized = normalized.replace("’", "'").replace("‘", "'")
    normalized = normalized.replace("(", " ").replace(")", " ")
    normalized = normalized.replace("/", " ").replace("-", " ")
    normalized = " ".join(normalized.split())
    return normalized


def _build_language_indexes() -> Tuple[Dict[str, Dict[str, str]], Dict[str, str]]:
    codes: Dict[str, Dict[str, str]] = {}
    synonyms: Dict[str, str] = {}

    for zh_name, en_name, code in LANGUAGE_ENTRIES:
        entry = codes.setdefault(code, {"zh": zh_name, "en": en_name})
        entry.setdefault("zh", zh_name)
        entry.setdefault("en", en_name)

        for name in {zh_name, en_name, code}:
            if not name:
                continue
            key = _normalize_alias(name)
            if key:
                synonyms.setdefault(key, code)
                compact = key.replace(" ", "")
                synonyms.setdefault(compact, code)

    return codes, synonyms


LANGUAGE_CODES, LANGUAGE_SYNONYMS = _build_language_indexes()


def _call_niutrans(payload: Dict[str, Any]) -> Dict[str, Any]:
    api_url = os.getenv("NIUTRANS_API_URL", DEFAULT_NIUTRANS_API_URL)
    try:
        response = requests.post(api_url, data=payload, timeout=10)
    except requests.RequestException as exc:
        raise RuntimeError(f"调用小牛翻译接口失败: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(
            f"小牛翻译接口返回非 200 状态码 {response.status_code}: {response.text}"
        )

    try:
        data: Dict[str, Any] = response.json()
    except ValueError as exc:
        raise RuntimeError("小牛翻译接口返回非 JSON 内容") from exc

    error_code = data.get("error_code") or data.get("errorCode")
    if error_code not in (None, "0", 0):
        message = data.get("error_msg") or data.get("errorMessage") or "Unknown error"
        raise RuntimeError(f"小牛翻译接口报错 {error_code}: {message}")

    return data


def _ensure_language_code(label: str, value: str) -> str:
    if not value:
        raise RuntimeError(f"缺少 {label} 语言代码")

    raw = value.strip()
    if raw in LANGUAGE_CODES:
        return raw

    normalized = _normalize_alias(raw)

    if normalized in LANGUAGE_CODES:
        return normalized

    alias_code = LANGUAGE_SYNONYMS.get(normalized) or LANGUAGE_SYNONYMS.get(
        normalized.replace(" ", "")
    )
    if alias_code:
        return alias_code

    normalized_lower = raw.lower()
    for code in LANGUAGE_CODES:
        if code.lower() == normalized_lower:
            return code

    raise RuntimeError(
        f"不支持的 {label} 语言代码: {value}。请参考 language-catalog 资源提供的列表后重新选择。"
    )


@mcp.tool()
def translate_text(
    text: Annotated[str, Field(description="待翻译的原文文本，可以是任意长度的字符串。")],
    source: Annotated[str, Field(description='源语言代码或常见别名（例如 "zh"、"中文"、"chinese"）。')],
    target: Annotated[str, Field(description='目标语言代码或常见别名（例如 "en"、"英文"、"english"）。')],
) -> Dict[str, Any]:
    """使用小牛翻译 API 将文本从 source 语种翻译到 target 语种。

    支持 450+ 种语言代码，并可自动处理常见别名。返回结构包含译文和 API 原始响应。

    Args:
        text (str): 待翻译的原文文本，可以是任意长度的字符串。
        source (str): 源语言代码或常见别名（例如 "zh"、"中文"、"chinese"）。
        target (str): 目标语言代码或常见别名（例如 "en"、"英文"、"english"）。

    Returns:
        Dict[str, Any]: 包含以下字段的字典：
            - source: 标准化后的源语言代码
            - target: 标准化后的目标语言代码
            - original_text: 原文
            - translated_text: 译文
            - raw: 小牛翻译 API 的原始响应数据
    """
    api_key = os.getenv("NIUTRANS_API_KEY")
    if not api_key:
        raise RuntimeError("缺少环境变量 NIUTRANS_API_KEY")

    source_code = _ensure_language_code("source", source)
    target_code = _ensure_language_code("target", target)

    payload: Dict[str, Any] = {
        "apikey": api_key,
        "from": source_code,
        "to": target_code,
        "src_text": text,
    }

    data = _call_niutrans(payload)

    translated = data.get("tgt_text") or data.get("target_text")
    if translated is None:
        raise RuntimeError(f"小牛翻译接口未返回译文: {data}")

    return {
        "source": source_code,
        "target": target_code,
        "original_text": text,
        "translated_text": translated,
        "raw": data,
    }


@mcp.resource("language://catalog")
def language_catalog() -> Dict[str, Any]:
    """提供小牛翻译支持的语种及别名列表。

    返回内容包括所有语种的代码与中英文名称，以及可用的别名映射，可用于模型在翻译前完成语种推断。
    """

    languages = [
        {"code": code, "zh": zh_name, "en": en_name}
        for zh_name, en_name, code in LANGUAGE_ENTRIES
    ]

    return {
        "total": len(languages),
        "languages": languages,
        "aliases": LANGUAGE_SYNONYMS,
    }


def main():
    """Main entry point for the translation server."""
    mcp.run()


# Run the server
if __name__ == "__main__":
    main()