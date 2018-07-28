import html
import xml.etree.ElementTree as ET


def format_start(start):
    return '%02d:%02d' % (start // 60, start % 60)


def parse_transcript(xml_transcript):
    result = ''
    root = ET.fromstring(xml_transcript)
    for child in root:
        # Make sure to convert `None` to ''
        text = child.text or ''
        # Explicit newlines hinder search; using space instead
        text = text.replace('\n', ' ')
        text = html.unescape(text)
        start = format_start(int(float(child.attrib['start'])))
        result += '%s%s\n' % (start.ljust(7), text)
    return result


def download_transcript(video_id):
    lang = 'en'
    resp = requests.get(
        'https://video.google.com/timedtext?lang=%s&v=%s' % (lang, video_id))
    return resp.text


if __name__ == '__main__':
    transcript = parse_transcript(download_transcript(sys.argv[1]))
    with open(sys.argv[2], 'w') as f:
        f.write(transcript)
