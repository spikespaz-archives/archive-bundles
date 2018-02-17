#! /usr/bin/env python3
from argparse import ArgumentParser
from os import system, remove, path, getuid
from cfgparser import read as cfgread, dump as cfgwrite, RawString


parser = ArgumentParser(description="Python script to wrap the pi-gen build scripts.")

# Arguments from config: IMG_NAME, APT_PROXY, BASE_DIR, WORK_DIR, DEPLOY_DIR, USE_QEMU
parser.add_argument("-n", "--img-name", dest="img_name",
                    help="The name of the image to build with the current stage directories."
                         " Setting IMG_NAME=\"Raspbian\" is logical for an unmodified RPi-Distro/pi-gen build,"
                         " but you should use something else for a customized version."
                         " Export files in stages may add suffixes to IMG_NAME.")
parser.add_argument("-p", "--apt-proxy", dest="apt_proxy",
                    help="If you require the use of an apt proxy, set it here."
                         " This proxy setting will not be included in the image,"
                         " making it safe to use an apt-cacher or similar package for development.")
parser.add_argument("-w", "--work-dir", dest="work_dir",
                    help="Directory in which pi-gen builds the target system."
                         " This value can be changed if you have a suitably large,"
                         " fast storage location for stages to be built and cached."
                         " Note, WORK_DIR stores a complete copy of the target system for each build stage,"
                         " amounting to tens of gigabytes in the case of Raspbian.")
parser.add_argument("-d", "--deploy-dir", dest="deploy_dir",
                    help="Output directory for target system images and NOOBS bundles.")
parser.add_argument("-q", "--use-qemu", dest="use_qemu", action="store_true",
                    help="This enable the Qemu mode and set filesystem and image suffix if set to 1.")
# This is at the end because it probably shouldn't be changed
parser.add_argument("--base-dir", dest="base_dir", default=".",
                    help="Top-level directory for pi-gen. Contains stage directories, build scripts,"
                         " and by default both work and deployment directories.")

# Arguments added by this build script
parser.add_argument("-m", "--mode", choices=("build", "build-clean", "docker", "docker-continue", "config"), default="build",
                    help="build/rebuild all, clean and rebuild just the last stage,"
                          " build using Docker, continue from a failed build with Docker, or just generate config")
parser.add_argument("-s", "--save-config", dest="save_config", action="store_true",
                    help="save the config file generated by this build script")
parser.add_argument("--fix-lines", dest="fix_lines", action="store_true",
                    help="fix the line endings of all files")
parser.add_argument("--skip-stages", dest="skip_stages", nargs="+", default=[], type=int,
                    help="list of stages to skip, by names of directory or stage number")
parser.add_argument("-r", "--reset", dest="reset", action="store_true",
                    help="run reset.sh first to remove work and deploy directories as well as stage SKIP files")


# If this script is called directly from shell
if __name__ == "__main__":
    args = parser.parse_args()

    if not args.mode == "config" and getuid() != 0:
        print("Script must be run as root to build images.")
        exit()

    if args.skip_stages and args.mode == "config":
        parser.print_usage()
        print(parser.prog + ": error: config mode and skip files cannot be used together")
        exit()

    if args.reset:
        print("Resetting before build...")
        system("./reset.sh")

    try:
        print("Reading config file...")
        defaults = cfgread("config")
        save_config = True
    except FileNotFoundError:
        print("Config not found.")
        defaults = {}
        save_config = args.save_config

    config = {
        "IMG_NAME": args.img_name or "Raspbian",
        "APT_PROXY": args.apt_proxy,
        "BASE_DIR": RawString(args.base_dir),
        "WORK_DIR": args.work_dir or "$BASE_DIR/work",
        "DEPLOY_DIR": args.deploy_dir or "$BASE_DIR/deploy",
        "USE_QEMU": int(args.use_qemu) or 0
    }

    cfgwrite(config, "config")

    # Start code, make files based on variables
    if args.fix_lines:
        print("Fixing all line endings...")
        system("./fix-lines.sh")

    if args.skip_stages:
        print("Adding stage SKIP files...")

        skip_files = " ".join([path.join(config["BASE_DIR"], "stage" + str(stage), "SKIP")
                               for stage in args.skip_stages])

        system("touch " + skip_files)
    else:
        skip_files = None

    # Build code, run build.sh based on arguments
    if args.mode == "build":
        print("Running normal build...")
        system("./build.sh")
    elif args.mode == "build-clean":
        print("Running clean build...")
        system("CLEAN=1 ./build.sh")
    elif args.mode == "docker":
        print("Running docker build...")
        system("./build-docker.sh")
    elif args.mode == "docker-continue":
        print("Running docker continued build...")
        system("CONTINUE=1 ./build-docker.sh")
    elif args.mode == "config":
        print("Not running any build...")
        save_config = True

    # End code, revert to what the directory was
    if skip_files and args.skip_stages:
        print("Removing stage SKIP files...")
        system("rm " + skip_files)

    if save_config:
        print("Keeping config file...")
    else:
        print("Removing config file...")
        remove("config")
