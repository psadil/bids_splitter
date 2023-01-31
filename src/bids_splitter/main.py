import pathlib
import os
import click


@click.command()
@click.option(
    "--src",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    required=True,
    help="Path to the BIDS dataset to split",
)
@click.option(
    "--dest",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    required=True,
    help="root directory underneath which to create the new datasets",
)
def main(src: pathlib.Path, dest: pathlib.Path) -> None:
    for sub in src.glob("sub-*"):
        sub_out_root = dest / sub.name
        sub_out = sub_out_root / sub.name
        sub_out.mkdir(exist_ok=True, parents=True)
        for dirpath, _, filenames in os.walk(sub):
            d = sub_out / pathlib.Path(dirpath).relative_to(sub)
            d.mkdir(exist_ok=True)
            for filename in filenames:
                pathlib.Path(d / filename).symlink_to(src / d / filename)
        for toplevel in ["README", "dataset_description.json"]:
            (sub_out / toplevel).symlink_to(src / toplevel)
