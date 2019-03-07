import adoptapi
import click
import json
import platform


def _replacement(value, substitutes):
    return substitutes.get(value, value)


class RequestOptions:
    def __init__(self, **kwargs):
        self.openjdk_impl = kwargs.get("openjdk_impl", None)
        self.os = kwargs.get("os", _replacement(platform.system().lower(), {"darwin": "mac"}))
        self.arch = kwargs.get(
            "arch",
            _replacement(
                platform.machine().lower(),
                {
                    "amd64": "x64",
                    "x86_64": "x64",
                    "aarch64_be": "aarch64",
                    "armv8b": "aarch64",
                    "armv8l": "aarch64",
                    "i386": "x32",
                    "i686": "x32",
                    "s390": "s390x",
                },
            ),
        )
        self.release = kwargs.get("release", None)
        self.type = kwargs.get("type", None)
        self.heap_size = kwargs.get("heap_size", "normal")

    def serialize(self):
        return self.__dict__


@click.group()
@click.option("-v", "--version", is_flag=True, help="Display the version number and exit.")
def cli(version):
    pass


@cli.command()
@click.argument("version", type=str, default="openjdk8", required=True)
@click.argument("out_file", type=click.File(mode="w"), default="-")
@click.option("-n", "--nightly", is_flag=True, default=False)
@click.option("-i", "--indent", type=int, default=None)
@click.option("--openjdk-impl", type=click.Choice(["hotspot", "openj9"]))
@click.option("--os", type=click.Choice(["windows", "linux", "mac"]))
@click.option("--arch", type=click.Choice(["x64", "x32", "ppc64", "s390x", "ppc64le", "aarch64"]))
@click.option("--release", type=str)
@click.option("--type", type=click.Choice(["jdk", "jre"]))
@click.option("--heap-size", type=click.Choice(["normal", "large"]))
def info(version, out_file, nightly, indent, **kwargs):
    if kwargs.get("release") == "latest":
        dump_data = next(adoptapi.info(version, nightly=nightly, **kwargs)).serialize()
    else:
        dump_data = list(
            map(adoptapi.Release.serialize, adoptapi.info(version, nightly=nightly, **kwargs))
        )

    json.dump(
        dump_data,
        out_file,
        indent=indent,
        separators=(",", ":") if indent is None else (", ", ": "),
    )


@cli.command()
def binary():
    pass


@cli.command()
def latest_assets(version, nightly, **kwargs):
    pass


if __name__ == "__main__":
    cli()
