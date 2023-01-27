import click

from pathlib import Path
from os import scandir
from os.path import exists, isdir
from PIL import Image, UnidentifiedImageError
from PIL.Image import Image as Pilimage


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option(
    '-c',
    '--crop',
    default='0, 0, 0, 0',
    type=str,
    help="Crop image before spliting. Usage: ['int, int, int, int']",
)
@click.option(
    '-d',
    '--direction',
    default='v',
    type=str,
    help='Split direction, `v` for vertical, `h` for horizontal',
)
@click.option(
    '-i', '--index', default=1, type=int, help='File name suffix start index'
)
@click.option(
    '-f',
    '--force',
    default=False,
    is_flag=True,
    help='Force overwriting existing files',
)
@click.option('-o', '--output', default='', type=str, help='File name prefix')
@click.option(
    '--order',
    default='L-R',
    type=str,
    help="Page orientation order. eg: 'L-R' means `Left first, right second`",
)
@click.option(
    '-r',
    '--rotate',
    default=0,
    type=float,
    help='Apply rotation of `n` degrees clockwise before spliting',
)
@click.option(
    '-z',
    '--zalign',
    default=None,
    type=int,
    help='Zero prefix align on the page index',
)
def main(crop, direction, force, order, output, paths, index, rotate, zalign):
    """
    Description: `lignin` is a program that takes pages as image files,
    split them in half (verticaly or horizontaly) and generate two new files
    with the two halfs from the input file.
    """
    files = get_files(list(paths))

    if not zalign:
        zalign = len(str(len(files) * 2))

    try:
        crop = get_crop(crop)
    except ValueError:
        click.echo(
            f'ERROR: `{crop}` is not a valid value to crop',
            err=True,
            color=True,
        )
        exit(1)

    try:
        direction = get_direction(direction)
    except ValueError:
        click.echo(
            f'ERROR: `{direction}` is not a valid direction',
            err=True,
            color=True,
        )
        exit(1)

    try:
        order = get_order(order, direction)
    except ValueError:
        click.echo(
            f'ERROR: `{order}` is not a valid order to `{direction}` split',
            err=True,
            color=True,
        )
        exit(1)

    page_count: int = index

    pages: list[dict] = []
    for image_path in files:
        click.echo(f'spliting `{image_path}`')
        extension: str = Path(image_path).suffix

        try:
            img = Image.open(image_path)
        except UnidentifiedImageError:
            click.echo(f'`{image_path}` is not a supported file format')
            continue

        try:
            img = img.crop(
                (
                    0 + crop[0],
                    0 + crop[1],
                    img.width - crop[2],
                    img.height - crop[3],
                )
            )
        except ValueError:
            click.echo(
                f'ERROR: crop of `{crop}` does not fit in image of size `{img.size}`',
                err=True,
                color=True,
            )
            exit(1)

        img = img.rotate(rotate * -1, expand=True)

        if direction == 'v':
            splited_pages: dict = vsplit_image(img)
        else:
            splited_pages: dict = hsplit_image(img)

        for i in range(len(splited_pages)):
            page_name: str = output + str(page_count).zfill(zalign) + extension
            page: dict = {
                'File': splited_pages[order[i]],
                'Name': page_name,
                'Origin': f'`{image_path}` from `{order[i]}`',
            }
            pages.append(page)
            page_count += 1
    print()

    save_page_list(pages, force)


def save_page_list(pages: list[dict], force):
    for page in pages:
        if exists(page['Name']) and not force:
            confirmation = click.confirm(f"overwrite file `{page['Name']}`?")
            if not confirmation:
                continue

        click.echo(f"saving {page['Name']}, from {page['Origin']}")
        page['File'].save(page['Name'])


def get_crop(symbol: str) -> list[int]:
    try:
        crop = list(map(int, symbol.split(', ')))
    except TypeError:
        raise ValueError('Invalid crop box')

    if len(crop) != 4:
        raise ValueError('Invalid crop box')

    for item in crop:
        if item < 0:
            raise ValueError('Invalid crop box')

    return crop


def get_direction(symbol: str) -> str:
    if not symbol in map(str.lower, ['v', 'h']):
        raise ValueError(f'{symbol} is not a valid direction')

    return symbol.lower()


def get_files(files: list[str]) -> list[str]:
    if not type(files) == list:
        raise ValueError(f'Invalid type: {type(files)}')

    if len(files) == 1 and isdir(files[0]):

        dir_files = scandir(files[0])

        files = []
        for file in dir_files:
            files.append(file.path)

    files = sorted(files, key=str.lower)

    return files


def get_order(symbol: str, direction: str) -> list[str]:
    symbol = symbol.upper()

    if direction == 'h':
        if not symbol in ['T-B', 'B-T']:
            raise ValueError('Invalid symbol assignment to order')

        symbol = symbol.replace('T', 'Top')
        symbol = symbol.replace('B', 'Bottom')
    elif direction == 'v':
        if not symbol in ['L-R', 'R-L']:
            raise ValueError('Invalid symbol assignment to order')

        symbol = symbol.replace('L', 'Left')
        symbol = symbol.replace('R', 'Right')
    else:
        raise ValueError('Invalid symbol assignment to order')

    order: list[str] = symbol.split('-')

    return order


def hsplit_image(img: Pilimage) -> dict[str, Pilimage]:
    pages: dict[str, Pilimage] = {
        'Top': img.crop((0, 0, img.width, img.height // 2)),
        'Bottom': img.crop((0, img.height // 2, img.width, img.height)),
    }

    return pages


def vsplit_image(img: Pilimage) -> dict[str, Pilimage]:
    pages: dict[str, Pilimage] = {
        'Left': img.crop((0, 0, img.width // 2, img.height)),
        'Right': img.crop((img.width // 2, 0, img.width, img.height)),
    }

    return pages


if __name__ == '__main__':
    main()
