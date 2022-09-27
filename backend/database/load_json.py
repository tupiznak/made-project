import json
import re
import string

FILE_PATH = '../../../../mp_data/dblpv13.json'
import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger('json_parser')


def custom_replaces(line: str):
    line = re.sub(r'NumberInt\((.+)\)', r'\1', line)
    line = line.replace(f'\\\\', f' ')
    for c in string.ascii_lowercase:
        if c in ('n', 't'):
            continue
        line = line.replace(f'\{c}', f'\\\{c}')
    if line.startswith('},'):
        line = '}'
    return line


def parse_json(file_path: str = FILE_PATH, previous_parsed_documents: int = 0):
    with open(file_path) as f:
        f.readline()  # first array open line "["
        documents_count = 0
        run = True
        while True:
            document_lines = ''
            while True:
                line = f.readline()
                line = custom_replaces(line)
                document_lines += line
                if documents_count >= previous_parsed_documents - 1:
                    logger.debug(f'{line.encode()}')
                if line == '}':
                    break
                if line == ']':
                    run = False
                    break
            if not run:
                break
            documents_count += 1
            if documents_count < previous_parsed_documents:
                continue
            document_lines = re.sub(r'NumberInt\((.+)\)', r'(\1)', document_lines)
            logger.debug(document_lines.encode())
            logger.warning(document_lines[1220:1240])
            logger.warning(documents_count)
            logger.info(json.loads(document_lines))


if __name__ == '__main__':
    logger.setLevel(level=logging.DEBUG)
    parse_json()
