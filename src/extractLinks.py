from bs4 import BeautifulSoup, ResultSet, Tag
from typing import List
from pathlib import Path
from progress.bar import Bar
import click
from pyfs import isFile, resolvePath
from io import TextIOWrapper

def extractURLs(soup: BeautifulSoup) -> dict[str, str]:
    data: dict[str, str] = {}

    urls: ResultSet = soup.find_all(name="a")
    urlCount: int = len(urls)

    with Bar("Extracting URLs from Awesome List...", max=urlCount) as bar:
        url: Tag
        for url in urls:
            data[url.text.replace("\n", " ").strip()] = url.get(key="href")
            bar.next()

    return data

@click.command()
@click.option(
    "-i",
    "--input",
    "inputPath",
    type=Path,
    required=True,
    help="Path to Awesome List in HTML file",
    )
def main(inputPath: Path)  ->  None:
    absInputPath: Path = resolvePath(path=inputPath)

    assert isFile(path=absInputPath)

    htmlFile: TextIOWrapper = open(file=absInputPath, mode="r")
    
    soup: BeautifulSoup = BeautifulSoup(markup=htmlFile, features="lxml")

    data: dict[str, str] = extractURLs(soup=soup)


if __name__ == "__main__":
    main()
