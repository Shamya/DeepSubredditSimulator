from __future__ import division #makes / always do float division, and // do integer division
import os, subprocess, sys, re,  time
#import matplotlib.pyplot as plt

START = chr(2)
END = chr(3)

#Program arguments: python main.py mode [data_file] [max_epochs]
#Examples:
# python main.py train title
# python main.py resume post_explainlikeimfive
max_epochs = int(sys.argv.pop()) if len(sys.argv) > 3 else 50
data_file = sys.argv.pop() if len(sys.argv) > 2 else "title"
mode = sys.argv.pop() if len(sys.argv) > 1 else ""

#We had multiple data formats and I didn't feel up to writing nice switching logic so this
# needs to be manually updated to match the input format
data_format = "csv" #Options: txt, csv, oanc
#Whether to use the pretrain to initialize (for "train" mode only)
use_pretrain = False

def getLatestCheckpoint(dir):
  checkpoints = os.listdir(dir)
  if len(checkpoints) > 0:
    max_checkpoint_index = 0
    max_checkpoint_fname = checkpoints[-1]
    for checkpoint in checkpoints:
      if checkpoint[-3:] == ".t7":
        m = re.search("_(\\d+)\.", checkpoint)
        if m and int(m.group(1)) > max_checkpoint_index:
          max_checkpoint_index = int(m.group(1))
          max_checkpoint_fname = checkpoint
    return max_checkpoint_fname

if mode == "train" or mode == "resume":
  os.chdir(os.path.dirname(os.path.abspath(__file__))) #force commands to be run from this file's folder
  train_cmd = (("th train.lua -input_h5 data/%s_charified.h5 -input_json data/%s_charified.json " +
                "-print_every -1 -max_epochs %d -rnn_size 256 -num_layers 3 -gpu 0 -lr_decay_every 1 " +
                "-lr_decay_factor 0.99 -reset_iterations 0 -dropout 0.5") % (data_file, data_file, max_epochs)).split()
  if mode == "train": #we don't have a checkpoint to resume from
    preprocess_cmd = "python scripts/preprocess.py --input_txt data/%s_charified.txt --output_h5 data/%s_charified.h5 --output_json data/%s_charified.json" % (data_file, data_file, data_file)
    charified_titles = ""
    if use_pretrain:
      #Initialize from the pretrained network
      train_cmd.append("-init_from")
      train_cmd.append("cv_pretrain_6epoch/%s"%getLatestCheckpoint("cv_pretrain_6epoch"))
      preprocess_cmd += " --input_json data/oanc_charified.json"
      #Insert the extra characters used in the pretraining data set so the mapping is the same
      # oanc_extra_chars = {"1": "\u0002", "2": " ", "3": "V", "4": "a", "5": "l", "6": "e", "7": "y", "8": "N", "9": "d", "10": "i", "11": "n", "12": "g", "13": "L", "14": "S", "15": "r", "16": "v", "17": "c", "18": "s", "19": "M", "20": "A", "21": "E", "22": "(", "23": "P", "24": ")", "25": "-", "26": "T", "27": "h", "28": "o", "29": "t", "30": "f", "31": "p", "32": "m", "33": ",", "34": "b", "35": "u", "36": "w", "37": "'", "38": "x", "39": ".", "40": "D", "41": "H", "42": "R", "43": "W", "44": "G", "45": "q", "46": "\"", "47": "3", "48": "0", "49": "C", "50": "z", "51": "J", "52": "K", "53": "B", "54": "k", "55": "1", "56": "O", "57": "$", "58": "2", "59": "9", "60": "5", "61": "7", "62": "U", "63": "I", "64": "\u0003", "65": "8", "66": "4", "67": "6", "68": "j", "69": "Y", "70": "F", "71": ":", "72": "[", "73": "]", "74": "Q", "75": "?", "76": "&", "77": "!", "78": ";", "79": "%", "80": "/", "81": "X", "82": "`", "83": "\u00e8", "84": "Z", "85": "\u2026", "86": "@", "87": "+", "88": "\u2022", "89": "*", "90": "~", "91": "\u00e9", "92": "=", "93": "{", "94": "}", "95": "\u00eb", "96": "\u00fc", "97": "\u00f6", "98": "\u00f3", "99": "\u00f8", "100": "\u00a7", "101": "\u2776", "102": "\u2777", "103": "\u2778", "104": "\u27a8", "105": "\u00dc", "106": "\u00d6", "107": "\u00a2", "108": "\u00be", "109": "\ufffd", "110": "\u00b6", "111": "\u00bd", "112": "\u03b2", "113": "\u00e7", "114": "\u00ae", "115": "\u2122", "116": "\u00b0", "117": ">", "118": "#", "119": "\u00b5", "120": "\u00b1", "121": "\u2030", "122": "<", "123": "^", "124": "\u00c5", "125": "\u00e2", "126": "\u00e5", "127": "\u00ef", "128": "\u00e4", "129": "\u00c9", "130": "\u00c7", "131": "\u00e3", "132": "\u00ed", "133": "\u00f1", "134": "\u00ec", "135": "\u00e1", "136": "\u00ee", "137": "\u00ea", "138": "\u00d1", "139": "\u00c4", "140": "_", "141": "\u25a0", "142": "\u00ba", "143": "\u00e0", "144": "\u00d2", "145": "\u00f2", "146": "\u00d3", "147": "|", "148": "\u00db", "149": "\u00af", "150": "\u00bc", "151": "\u2021", "152": "\u00a9", "153": "\u00a4", "154": "\u25c6", "155": "\u0153", "156": "\u2666", "157": "\u25cf", "158": "\u00ab", "159": "\u221a", "160": "\u0192", "161": "\u2248", "162": "\u00ac", "163": "\u0394", "164": "\u2212", "165": "\u2013", "166": "\u201c", "167": "\u201d", "168": "\u2018", "169": "\u2019", "170": "\u2014", "171": "\u03b1", "172": "\u03b3", "173": "\u03bc", "174": "\u00d7", "175": "\u03b4", "176": "\u2032", "177": "\u223c", "178": "\u03b9", "179": "\u03b7", "180": "\u03c3", "181": "\u03a6", "182": "\u2329", "183": "\u232a", "184": "\u03ba", "185": "\u2192", "186": "\u2265", "187": "\u2264", "188": "\u03c7", "189": "\u00df", "190": "\u2033", "191": "\u20ac", "192": "\u00c3", "193": "\u03a3", "194": "\u03b5", "195": "\u00e6", "196": "\u00a3", "197": "\u03a9", "198": "\u00ce", "199": "\u00c2", "200": "\u2020", "201": "\u02c6", "202": "\u03a7", "203": "\u00b7", "204": "\u2003", "205": "\u2260", "206": "\u221e", "207": "\u2208", "208": "\u2286", "209": "\u03c9", "210": "\u2245", "211": "\u03c0", "212": "\u03c6", "213": "\u0393", "214": "\u00b4", "215": "\u03b8", "216": "\u03bb", "217": "\u0397", "218": "\u2190", "219": "\u03c4", "220": "\u2200", "221": "\u221d", "222": "\u03c1", "223": "\u22a5", "224": "\\", "225": "\u00bb", "226": "\u03a8", "227": "\u2191", "228": "\u2193", "229": "\u2229", "230": "\u2211", "231": "\u03bd", "232": "\u03c8", "233": "\u03a0", "234": "\u0398", "235": "\u2194", "236": "\u0142", "237": "\u25b2", "238": "\u2207", "239": "\u2202", "240": "\u03b6", "241": "\u2261", "242": "\u226b", "243": "\u25a1", "244": "\u03be", "245": "\u0160", "246": "\u25b6", "247": "\u25b7", "248": "\u03c5", "249": "\u00d8", "250": "\u00f4", "251": "\u00fa", "252": "\u25cb", "253": "\ufb01", "254": "\ufb02", "255": "\u2002", "256": "\u00a0", "257": "\uf0f7", "258": "\uf020", "259": "\u00f7", "260": "\u2044", "261": "\u201a", "262": "\u2741", "263": "\u00ad", "264": "\u2008", "265": "\u00f9", "266": "\u00c1", "267": "\u272a", "268": "\u0131", "269": "\u00bf", "270": "\u00c0", "271": "\u00f5", "272": "\u02d8", "273": "\u00a5", "274": "\u00a1", "275": "\u00cc", "276": "\u00fb", "277": "\u00cd", "278": "\u8ca5", "279": "\u98ec", "280": "\u9038", "281": "\u0373", "282": "\t", "283": "\u9973", "284": "\u080e", "285": "\ufeff", "286": "\u0101", "287": "\u01fd", "288": "\u00ff", "289": "\u016d", "290": "\u017c", "291": "\u00c6", "292": "\u014d", "293": "\u0113", "294": "\u016b", "295": "\u03c2", "296": "\u03bf", "297": "\u015b", "298": "\u0129", "299": "\u012b", "300": "\u00a6", "301": "\u0159", "302": "\u010d", "303": "\u222b", "304": "\u00b2", "305": "\u00b3", "306": "\u011b", "307": "\u0107", "308": "\u02dc", "309": "\u0161", "310": "\u00b9", "311": "\u00fd", "312": "\u2234", "313": "\u0103", "314": "\u012a", "315": "\u00da", "316": "\u00f0", "317": "\u00fe", "318": "\u0108", "319": "\u010c", "320": "\u017a", "321": "\u0155", "322": "\u01f5", "323": "\u0144", "324": "\u0399", "325": "\u0392"}
      # for idx,char in oanc_extra_chars.items():
      #   print(idx)
      #   charified_titles += unichr(int(char[2:], 16)).encode('utf8') if char[:2] == "\u" else char
    #clear out the previous training run
    for file in os.listdir("cv"):
      file_path = os.path.join("cv", file)
      try:
        if os.path.isfile(file_path):
          os.unlink(file_path)
      except Exception as e:
        print e
    if data_format == "txt":
      titles = None
      with open("data/%s.txt"%data_file) as f:
        titles = list(f)[0]
      titles = titles.replace("**end**", "\n").replace("**start**", "")
      for title in titles.split("\n"):
        title = title.strip()
        if len(title) > 0:
          charified_titles += START + title.strip() + END
    elif data_format == "csv":
      csvs = None
      with open("data/%s.csv"%data_file) as f:
        csvs = list(f)[1:] #first line is a header
      for csv in csvs:
        post_title = csv.strip().split(",")[2]
        if re.match('^".*"$', post_title) is not None:
          post_title = re.match('^"(.*)"$', post_title).group(1)
          post_title = re.sub('""', '"', post_title)
        post_title = re.sub('comma_symbol', ',', post_title)
        post_title = re.sub(chr(0x7f), '', post_title) #remove DEL character
        charified_titles += START + post_title + END
    elif data_format == "oanc":
      with open("data/%s.txt"%data_file) as f:
        charified_titles = f.read()
    with open("data/%s_charified.txt"%data_file, "w") as f:
      f.write(charified_titles)
    subprocess.call(preprocess_cmd.split())
  else: #mode == "resume":
    train_cmd.append("-init_from")
    train_cmd.append("cv/%s"%getLatestCheckpoint("cv"))
  subprocess.call(train_cmd)


start_time = time.time()
#Overall process:
# We general 20k characters; some of these characters are the START and END tokens we inserted before
# We then slice up the 20k characters into individual post titles by extracting "START <title text> END"
# Then we take the first 100 of those as output
length = 2000
samples = 10
if mode == "sample":
  length = 200*max_epochs
  samples = max_epochs
generated = subprocess.check_output(("th sample.lua -checkpoint cv/%s -length %d -start_text %s" % (getLatestCheckpoint("cv"), length, START) ).split())
generated = generated.split(END + START)
generated[0] = generated[0][1:] #remove START from first one
generated[-1] = generated[-1][:-1] #remove END from last one
for i in xrange(samples):
  generated[i] = generated[i].replace(START, "").replace(END, "")
  print generated[i]

end_time = time.time()

print end_time - start_time