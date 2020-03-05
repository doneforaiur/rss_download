import os

from defusedxml import ElementTree
from xml.etree.ElementTree import Element
from urllib import request

from .podcast import Episode
from .string import str_to_filename
from .xml import get_unique_xml_element
from .misc import null
import sys
import time
import datetime


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration + 0.001)) #Adding 0.001 because of division by zero
    percent = int(count * block_size * 100 / (total_size + 0.001))
    sys.stdout.write("\r......%d%%,     %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def podcast_download(rss: Element,rss_source, last_pub, delay: int=0, output_dir: str='',
                     rename: bool=False, start=0, end=0, print_progress=null) -> dict:

    files_downloaded = 0
    file_errors = 0
    download_progress = []

    f = open("subs.txt", "w")
    now = time.localtime()

    print (now > last_pub)
    f.write(rss_source + " " +str(time.strftime("%a, %d %b %Y %H:%M:%S %z", now)))
    f.close()

    if output_dir:
        output_dir = os.path.join(os.getcwd(), output_dir)

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
    else:
        output_dir = os.getcwd()
    

    items = rss.findall('channel/item')
    items.reverse()
	

    if not (start == 0 and end == 0):
        items = items[int(start): int(end)]
	
    total_files = len(items)

	
    file_number = 0
    
    for item in items:
	
        file_number += 1

        episode = Episode(item)
        episode.file_extension = "mp3"
		
        print("\n")
        print_progress(f'Downloading {str(file_number)} of {str(total_files)}: "{episode.title}"')
             
        filename = f'{str_to_filename(episode.title)}.{str_to_filename(episode.file_extension)}'

        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            continue

        try:
            request.urlretrieve(episode.url, filepath, reporthook)

            files_downloaded += 1
            download_progress.append({
                'file': filename,
                'downloaded': True,
            })
        except Exception as e:
            print_progress(f'  ERROR -> {str(e)}')

            file_errors += 1
            download_progress.append({
                'file': filename,
                'downloaded': False,
                'error': str(e),
            })

    return {
        'total_items': len(items),
        'total_downloads': files_downloaded,
        'total_errors': file_errors,
        'downloads': download_progress,
    }
