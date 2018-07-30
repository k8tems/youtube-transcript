"""Download transcript and convert to human-readable format"""
import argparse
import html
import requests
import xml.etree.ElementTree as ET


def format_start(start):
    return '%02d:%02d' % (start // 60, start % 60)


def parse(xml_transcript):
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
        # Add additional newline for writing space
        result += '\n'
    return result


def download(video_id, lang):
    resp = requests.get(
        'https://video.google.com/timedtext?lang=%s&v=%s' % (lang, video_id))
    return resp.text


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', type=str)
    parser.add_argument('dest', type=str)
    parser.add_argument('--lang', type=str, default='en')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    transcript = parse(download(args.video_id, args.lang))
    with open(args.dest, 'w') as f:
        f.write(transcript)
