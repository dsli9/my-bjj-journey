import argparse
import logging

import docker

from bjj_journey.utils import set_up_logging


LOGGER = logging.getLogger(__name__)

GCLOUD_REGION = "us-east1"
GCLOUD_PROJECT_ID = "bjj-dashboard-383320"
GCLOUD_REPO_ID = "bjj-docker-repo"
DOCKER_REGISTRY = f"{GCLOUD_REGION}-docker.pkg.dev/{GCLOUD_PROJECT_ID}/{GCLOUD_REPO_ID}"


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Tag image with prod")

    parser.add_argument("image", help="Name of image to tag.")
    parser.add_argument(
        "-v",
        "--verbose",
        help=(
            "Increase level of feedback output. Use -vv for even more detail. "
            "Log level defaults to 'WARNING'"
        ),
        action="count",
        default=0,
        dest="verbosity",
    )
    parser.add_argument(
        "-i",
        "--image-version",
        default="latest",
        help=(
            "Version of the image to tag with prod (e.g. 1.0.1). "
            "This must correspond with an image tag in Google Artifact Registry"
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Tag an existing image with prod."""
    args = parse_args()
    set_up_logging(args.verbosity)

    image_url = f"{DOCKER_REGISTRY}/{args.image}"
    version_tag = f"{image_url}:{args.image_version}"

    # Create a client for interacting with Docker repository
    docker_client = docker.from_env()
    prod_tag = f"{image_url}:prod"

    # Pull, Tag, and Push the Docker Image
    LOGGER.info(f"Pulling the image with tag {version_tag}")
    image = docker_client.images.pull(version_tag)
    LOGGER.info(
        f"Digest of image with version {args.image_version}:"
        f" {image.attrs.get('RepoDigests')[0]}"
    )

    LOGGER.info(f"Tagging image {version_tag} with prod tag")
    image.tag(prod_tag)

    LOGGER.info(f"Pushing image {prod_tag}")
    docker_client.images.push(prod_tag)


if __name__ == "__main__":
    main()
