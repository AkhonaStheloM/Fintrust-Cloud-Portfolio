from ..utils.sessions import get_client

VALID_STRATEGIES = {
    "rehost",
    "replatform",
    "refactor",
    "retire",
    "retain",
    "repurchase"
}


def _get_tag(tags, key):

    for tag in (tags or []):

        if tag["Key"] == key:
            return tag["Value"]

    return None


def classify_instances(
        tag_prefix="migration"
):

    ec2 = get_client("ec2")

    paginator = ec2.get_paginator(
        "describe_instances"
    )

    portfolio = {
        s: []
        for s in VALID_STRATEGIES
    }

    untagged = []

    for page in paginator.paginate():

        for reservation in page[
            "Reservations"
        ]:

            for inst in reservation[
                "Instances"
            ]:

                tags = inst.get(
                    "Tags",
                    []
                )

                strategy = _get_tag(
                    tags,
                    f"{tag_prefix}:strategy"
                )

                wave = _get_tag(
                    tags,
                    f"{tag_prefix}:wave"
                )

                entry = {
                    "id":
                        inst["InstanceId"],
                    "wave":
                        wave,
                    "strategy":
                        strategy
                }

                if (
                    strategy
                    in
                    VALID_STRATEGIES
                ):
                    portfolio[
                        strategy
                    ].append(entry)

                else:
                    untagged.append(
                        entry
                    )

    return portfolio, untagged


def get_migration_wave(
        wave_number
):

    portfolio, _ = classify_instances()

    return [
        instance
        for instances
        in portfolio.values()
        for instance
        in instances
        if instance["wave"]
        == str(wave_number)
    ]