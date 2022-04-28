import click
import datetime
import hashlib
import typing as t
import time

import httpx

from ..api.client import IOServiceClient
from ..api.models import SubscriptionsFeed


def hash_fiscal_code(code: str) -> str:
    uppercased_code = code.upper()
    encoded_code = bytes(uppercased_code, encoding="utf8")
    hashed_code = hashlib.sha256(encoded_code)
    hexed_hash = hashed_code.hexdigest()
    lowercased_hash = hexed_hash.lower()
    return lowercased_hash


@click.group()
@click.version_option(package_name="io-beep-boop")
@click.option(
    "-t",
    "--token",
    type=str,
    help="One of the two IO App API tokens of the service you want to use.",
    prompt=True,
)
@click.option(
    "--base-url",
    default="https://api.io.italia.it/api/v1",
    type=str,
    help="The base URL of the IO App API to use.",
)
@click.pass_context
def main(ctx: click.Context, token: str, base_url: str):
    ctx.ensure_object(dict)
    ctx.obj["CLIENT"] = IOServiceClient(token=token, base_url=base_url)


@main.command("registered-fast")
@click.option(
    "--input",
    "input_file",
    type=click.File("r"),
    help="The path to the file to use as input.",
    prompt=True,
    default="./input.txt",
)
@click.option(
    "--registered",
    "registered_file",
    type=click.File("w"),
    help="The path to the file to output registered users to.",
    prompt=True,
    default="./registered.txt",
)
@click.option(
    "--unregistered",
    "unregistered_file",
    type=click.File("w"),
    help="The path to the file to output unregistered users to.",
    prompt=True,
    default="./unregistered.txt",
)
@click.option(
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="The date to start retrieving fiscal codes from.",
    default=datetime.date.today().isoformat(),
    prompt=True,
)
@click.option(
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="The date to stop retrieving fiscal codes at.",
    default=datetime.date.today().isoformat(),
    prompt=True,
)
@click.option(
    "--sleep",
    type=float,
    help="Time to sleep between two subscription feed requests.",
    default=1.0,
)
@click.pass_context
def registered_fast(ctx: click.Context, input_file: t.TextIO, registered_file: t.TextIO, unregistered_file: t.TextIO, start_date: datetime.date, end_date: datetime.date, sleep: float):
    # Clean up input file
    click.echo("Cleaning up input file...")
    input_codes: set[str] = set(filter(lambda line: bool(line), map(lambda line: line.strip().upper(), input_file)))

    # Convert codes into a map of hash → code
    click.echo("Hashing fiscal codes...")
    input_map: dict[str, str] = {hash_fiscal_code(code): code for code in input_codes}

    # Retrieve objects from the API
    client: IOServiceClient = ctx.obj["CLIENT"]

    api_codes: set[str] = set()
    total_days: int = (end_date - start_date).days + 1

    with click.progressbar(range(0, total_days), length=total_days, label="Retrieving data from the API...") as days:
        for day in days:
            while True:
                try:
                    feed: SubscriptionsFeed = client.get_subscriptions_on_day(date=start_date + datetime.timedelta(days=day))
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:
                        continue
                    else:
                        raise
                else:
                    api_codes += set(feed.subscriptions)
                    api_codes -= set(feed.unsubscriptions)
                finally:
                    time.sleep(sleep)

    # Convert objects back to fiscal codes
    click.echo("Calculating registered fiscal codes...")
    registered_codes: set[str] = {input_map.get(code) for code in api_codes}
    unregistered_codes: set[str] = input_codes.difference(registered_codes)

    click.echo("Writing registered codes file...")
    for code in registered_codes:
        registered_file.write(f"{code}\n")

    click.echo("Writing unregistered codes file...")
    for code in unregistered_codes:
        unregistered_file.write(f"{code}\n")


@main.command("registered-slow")
@click.option(
    "--input",
    "input_file",
    type=click.File("r"),
    help="The path to the file to use as input.",
    prompt=True,
    default="./input.txt",
)
@click.option(
    "--registered",
    "registered_file",
    type=click.File("w"),
    help="The path to the file to output registered users to.",
    prompt=True,
    default="./registered.txt",
)
@click.option(
    "--unregistered",
    "unregistered_file",
    type=click.File("w"),
    help="The path to the file to output unregistered users to.",
    prompt=True,
    default="./unregistered.txt",
)
@click.option(
    "--sleep",
    type=float,
    help="Time to sleep between two profile requests.",
    default=1.0,
)
@click.pass_context
def registered_slow(ctx: click.Context, input_file: t.TextIO, registered_file: t.TextIO, unregistered_file: t.TextIO, sleep: float):
    # Clean up input file
    click.echo("Cleaning up input file...")
    input_codes: set[str] = set(filter(lambda line: bool(line), map(lambda line: line.strip().upper(), input_file)))

    # Retrieve objects from the API
    client: IOServiceClient = ctx.obj["CLIENT"]

    with click.progressbar(input_codes, label="Performing checks...") as codes:
        for code in codes:
            while True:
                try:
                    profile = client.get_profile(fiscal_code=code)
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:
                        continue
                    elif e.response.status_code == 404:
                        unregistered_file.write(f"{code}\n")
                        break
                    else:
                        raise
                else:
                    if not profile.sender_allowed:
                        unregistered_file.write(f"{code}\n")
                        break
                    else:
                        registered_file.write(f"{code}\n")
                        break
                finally:
                    time.sleep(sleep)


if __name__ == "__main__":
    main()
