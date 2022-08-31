import click

from os import scandir
from os.path import isdir
from pathlib import Path
from PIL import Image

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--order", default="LR")
@click.option("-o", "--output", default="")
@click.option("--pindex", default="1")
@click.option("--zalign", default="3")
def main(files, order, output, pindex, zalign):
    page_count = int(pindex)
    zalign = int(zalign)

    if len(files) < 2:
        if isdir(files[0]):
            dir_files = scandir(files[0])

            files = []
            for file in dir_files:
                files.append(file.path)

            files.sort()
    
    for image_file in files:
        with Image.open(image_file) as img:
            print(f"cracking `{image_file}`")
            new_img = img.crop((150, 0, img.width - 150, img.height))

            r_img = new_img.crop((new_img.width // 2, 0, new_img.width, new_img.height))
            l_img = new_img.crop((0, 0, new_img.width // 2, new_img.height))

            extension = Path(image_file).suffix

            for char in order:
                if char == "L":
                    l_name = output + str(page_count).zfill(zalign) + extension
                    page_count += 1
                    l_img.save(l_name)
                    print(f"created `{l_name}` from left half")

                elif char == "R":
                    r_name = output + str(page_count).zfill(zalign) + extension
                    r_img.save(r_name)
                    print(f"created `{r_name}` from right half")
                    page_count += 1

        print()
    

if __name__ == "__main__":
    main()
    
