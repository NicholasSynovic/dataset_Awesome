from bs4 import BeautifulSoup, ResultSet, Tag
from typing import List
from pathlib import Path
from progress.bar import Bar
import click
from pyfs import isFile, resolvePath
from io import TextIOWrapper
from pandas import DataFrame

def extractURLs(soup: BeautifulSoup) -> dict[str, List[str]]:
    data: dict[str, List[str]] = {"name": [], "url": []}

    urls: ResultSet = soup.find_all(name="a")
    urlCount: int = len(urls)

    with Bar("Extracting URLs from Awesome List...", max=urlCount) as bar:
        url: Tag
        for url in urls:
            data["name"].append(url.text.replace("\n", " ").strip())
            data["url"].append(url.get(key="href"))
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
@click.option(
        "-o",
        "--output",
        "outputPath",
        type=Path,
        required=True,
        help="Path to save pickled pandas.DataFrame of relevant URLs",
        )
def main(inputPath: Path, outputPath: Path)  ->  None:
    absInputPath: Path = resolvePath(path=inputPath)
    absOutputPath: Path = resolvePath(path=outputPath)

    assert isFile(path=absInputPath)

    htmlFile: TextIOWrapper = open(file=absInputPath, mode="r")
    
    soup: BeautifulSoup = BeautifulSoup(markup=htmlFile, features="lxml")

    data: dict[str, List[str]] = extractURLs(soup=soup)

    df: DataFrame = DataFrame(data=data)
    df.to_pickle(path=absOutputPath)


if __name__ == "__main__":
    main()
