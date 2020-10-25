### System ###
import sys
import logging

### Logging ###
import logzero
from logzero import logger


### Diffing ###
from diff_match_patch import diff_match_patch

### CLI Parsing ###
import click


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: {}".format(", ".join(sorted(matches))))


@click.group(cls=AliasedGroup)
@click.pass_context
@click.option("-d", "--debug", is_flag=True, help="Print debug information if given")
def cli(ctx, debug):
    """A pure-python diffing utility using Google's diff-match-patch.

    \b
    This tool serves exactly two functions:
    1. Create diffs between two versions of the same file
    2. Apply diffs to a file

    Commands can be abbreviated by the shortest unique string.

    \b
    For example:
        diff -> d
        apply -> a

    \b
    Examples of full commands:
        diffusor diff <source_file> <modified_file> -n <target_file>
        diffusor apply <patch_file> -t <target_file>
    """
    ctx.ensure_object(dict)

    logzero.loglevel(logging.DEBUG if debug else logging.INFO)

    ctx.obj["debug"] = debug


@cli.command()
@click.pass_context
@click.argument("original", type=click.File("r"))
@click.argument("modified", type=click.File("r"))
@click.option(
    "-n", "--name", help="The filename to save with the patch", default=None, type=str
)
@click.option(
    "-o",
    "--output-file",
    help="The file to output to",
    default=None,
    type=click.File("w"),
)
def diff(ctx, original, modified, name, output_file):
    dmp = diff_match_patch()

    original = original.read()
    modified = modified.read()

    patches = dmp.patch_make(original, modified)

    diff = dmp.patch_toText(patches)

    if name:
        diff = "file: {}\n".format(name) + diff

    if output_file:
        output_file.write(diff)
    else:
        click.echo(diff)


@cli.command()
@click.pass_context
@click.argument("patch", type=click.File("r"))
@click.option(
    "-t",
    "--target-file",
    help="The file to apply the patches to",
    default=None,
    type=click.File("r"),
)
@click.option(
    "-o",
    "--output-file",
    help="The file to output to",
    default=None,
    type=click.File("w"),
)
def apply(ctx, patch, target_file, output_file):
    dmp = diff_match_patch()

    diff = patch.read()

    inferred_target_file = None
    diff_split = diff.split("\n")
    if diff_split[0].startswith("file:"):
        inferred_target_file = diff_split[0].lstrip("file: ").strip()
        diff = "\n".join(diff_split[1:])
        logger.debug("Inferred target file: {}".format(inferred_target_file))

    patches = dmp.patch_fromText(diff)

    if target_file:
        target = target_file.read()
    elif inferred_target_file:
        with click.open_file(inferred_target_file, "r") as f:
            target = f.read()
    else:
        logger.error("Could not infer target file. Please specify using -t option")
        sys.exit(1)

    patched_text, _ = dmp.patch_apply(patches, target)

    if output_file:
        output_file.write(patched_text)
    else:
        click.echo(patched_text)


if __name__ == "__main__":
    cli()
