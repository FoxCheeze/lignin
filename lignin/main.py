import click

from os import scandir
from os.path import isdir
from pathlib import Path
from PIL import Image
from PIL.Image import Image as Pilimage

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--order", default="L-R")
@click.option("-o", "--output", default="")
@click.option("--pindex", default="1")
@click.option("--zalign", default="3")
def split(files, order, output, pindex, zalign):
    page_count: int = int(pindex)

    order = get_order(order)
    zalign = int(zalign)

    if len(files) == 1 and isdir(files[0]):
        dir_files = scandir(files[0])

        files = []
        for file in dir_files:
            files.append(file.path)

        files.sort()
    
    for image_path in files:
        print(f"spliting `{image_path}`")
        extension: str = Path(image_path).suffix

        with Image.open(image_path) as img:
            img = img.crop((150, 0, img.width - 150, img.height))
            pages: dict = split_image(img)

        page_name: str = output + str(page_count).zfill(zalign) + extension
        page_count += 1
        pages[order[0]].save(page_name)
        print(f"created `{page_name}` from {order[0]} half")

        page_name: str = output + str(page_count).zfill(zalign) + extension
        pages[order[1]].save(page_name)
        print(f"created `{page_name}` from {order[1]} half")
        page_count += 1

        print()


def split_image(img: Pilimage) -> dict[str, Pilimage]:
    pages: dict = {}

    pages["Left"] = img.crop((0, 0, img.width // 2, img.height))
    pages["Right"] = img.crop((img.width // 2, 0, img.width, img.height))

    return pages
    

def get_order(symbol: str) -> list[str]:
    symbol = symbol.replace("L", "Left")
    symbol = symbol.replace("R", "Right")

    order: list = symbol.split("-")

    return order


if __name__ == "__main__":
    split()
    
