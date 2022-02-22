import argparse
import csv
import os.path
import sys
import wikipedia


def crawl(titles, maxdepth=1):
	queue = [(title, 1) for title in titles]
	visited = set()
	while queue:
		title, depth = queue.pop(0)
		if title in visited:
			continue
		visited.add(title)
		try:
			page = wikipedia.page(title, auto_suggest=False)
			yield(page.title, page.content)
			if depth < maxdepth:
				queue.extend((t, depth+1) for t in page.links)
		except Exception as e:
			print(e, file=sys.stderr)


def write_output(crawler, output_dir):
	for title, text in crawler:
		filename = title.replace(' ', '_') + '.txt'
		try:
			with open(os.path.join(output_dir, filename), 'w+') as fp:
				fp.write(text)
		except Exception as e:
			print(e, file=sys.stderr)

def parse_arguments():
    parser = argparse.ArgumentParser(
    	description='Simple crawler for English Wikipedia.')
    parser.add_argument(
		'title', nargs='+', help='The titles of the starting pages.')
    parser.add_argument('-d', '--maxdepth', type=int, default=1)
    parser.add_argument('-o', '--output-dir', default='')
    return parser.parse_args()


if __name__ == '__main__':
	args = parse_arguments()
	titles = args.title
	if '-' in titles:
		titles.remove('-')
		for line in sys.stdin:
			titles.append(line.rstrip())
	crawler = crawl(titles, args.maxdepth)
	write_output(crawler, args.output_dir)

