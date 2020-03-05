from defusedxml import ElementTree

from modules.xml import get_unique_xml_element, parse_remote_xml
from modules.download import podcast_download
import time
def download_rss():

    remote_rss = True
    delay = 1
    rename = True
	
    rss_source = ''
    while not rss_source:
        rss_source = input(f'RSS {"URL" if remote_rss else "path"}: ')
        try:
            rss = parse_remote_xml(rss_source)
        except Exception as e:
            print(str(e))
            rss_source = ''

    output_dir = input('The output directory (download): ')
    if not output_dir:
        output_dir = 'download'
		
	
    start = input('The starting position (0): ')
    end = input('The end position (0): ')
    if not start or  not end:
        start = 0
        end = 0
	
    total_files = len(rss.findall('channel/item'))
    print(f'{str(total_files)} file{"s" if total_files != 1 else ""} in total.\n')
    pub_date = rss.find('channel/pubDate')
    print(pub_date.text)
    
    last_pub = time.strptime(pub_date.text, "%a, %d %b %Y %H:%M:%S %z")
    print(last_pub)

    download = podcast_download(rss, rss_source, last_pub, delay, output_dir, rename, start, end, print_progress=print)
    print('Download complete\n')
    print(f'{str(download["total_downloads"])} files downloaded.')
    print(f'{str(download["total_errors"])} errors.')


if __name__ == '__main__':
    try:
        download_rss()
    except KeyboardInterrupt:
        print("\nDownloading cancelled.")
		
    input('\nPress ENTER to exit')