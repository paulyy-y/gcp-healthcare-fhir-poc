import argparse

def parse_command_line_args():
    """Parses command line arguments."""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--credentials",
        default=None,
        help="Path to your service account credentials",
    )

    parser.add_argument(
        "--project_id",
        default=None,
        help="Google cloud project id (not fully qualified)",
    )

    parser.add_argument(
        "--resource_id",
        default=None,
        help="Google cloud project id (not fully qualified)",
    )

    parser.add_argument(
        "--region",
        default="us-west2",
        help="Cloud region to use",
    )

    parser.add_argument(
        "--fhir_dataset",
        default="us-west2",
        help="FHIR dataset to target",
    )

    parser.add_argument(
        "--fhir_datastore",
        default="us-west2",
        help="FHIR datastore to target",
    )

    parser.add_argument(
        "--resource_type",
        default=None,
        help="The type of resource. First letter must be capitalized",
    )

    parser.add_argument(
        "--resource_path",
        default=None,
        help="The path to JSON that has resource definition, examples in resources",
    )

    parser.add_argument(
        "--action",
        default=None,
        help="Action performed by script, either Get or Create [a resource]",
    )

    return parser.parse_args()