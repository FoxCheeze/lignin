import click

from pathlib import Path
from os import scandir
from os.path import isdir
from PIL import Image
from PIL.Image import Image as Pilimage


@click.group()
def main():
    pass


@main.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--order', default='L-R')
@click.option('-o', '--output', default='')
@click.option('--pindex', default='1')
@click.option('--zalign', default='3')
def vsplit(files, order, output, pindex, zalign, write_files=True):
    if len(files) == 1 and isdir(files[0]):
        files = convert_files(files)

    page_count: int = int(pindex)

    order = get_order(order)
    zalign = int(zalign)

    pages: list[dict] = []
    for image_path in files:
        print(f'spliting `{image_path}`')
        extension: str = Path(image_path).suffix

        with Image.open(image_path) as img:
            img = img.crop((150, 0, img.width - 150, img.height))
            splited_pages: dict = vsplit_image(img)

        for i in range(len(splited_pages)):
            page_name: str = output + str(page_count).zfill(zalign) + extension
            page: dict = {
                'File': splited_pages[order[i]],
                'Name': page_name,
                'Origin': f'{image_path} -- {order[i]}',
            }
            pages.append(page)
            page_count += 1

    if write_files:
        save_page_list(pages)

    return pages


def save_page_list(pages: list[dict]):
    for page in pages:
        print(f"saving {page['Name']}, from {page['Origin']}")
        page['File'].save(page['Name'])


def vsplit_image(img: Pilimage) -> dict[str, Pilimage]:
    pages: dict = {}

    pages['Left'] = img.crop((0, 0, img.width // 2, img.height))
    pages['Right'] = img.crop((img.width // 2, 0, img.width, img.height))

    return pages


def get_order(symbol: str) -> list[str]:
    symbol = symbol.replace('L', 'Left')
    symbol = symbol.replace('R', 'Right')

    order: list = symbol.split('-')

    return order


def convert_files(files: list) -> list:
    dir_files = scandir(files[0])

    files = []
    for file in dir_files:
        files.append(file.path)

    files.sort()

    return files


if __name__ == '__main__':
    main()
