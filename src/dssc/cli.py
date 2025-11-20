"""
Command-line interface for DSSC processing.
"""

import argparse
from pathlib import Path


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Solar photophysics transient absorption analysis"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Chirp fitting command
    chirp_parser = subparsers.add_parser(
        "chirp-fit",
        help="Fit chirp parameters from blank sample"
    )
    chirp_parser.add_argument(
        "data_dir",
        type=Path,
        help="Directory containing wavelength.dat, delay.dat, signal.dat"
    )
    chirp_parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("chirp_params.dat"),
        help="Output file for chirp parameters"
    )
    chirp_parser.add_argument(
        "--wvln-min",
        type=float,
        default=460,
        help="Minimum wavelength for fitting (nm)"
    )
    chirp_parser.add_argument(
        "--wvln-max",
        type=float,
        default=700,
        help="Maximum wavelength for fitting (nm)"
    )

    # Process command
    process_parser = subparsers.add_parser(
        "process",
        help="Process TA data with chirp correction"
    )
    process_parser.add_argument(
        "data_dir",
        type=Path,
        help="Directory containing TA data files"
    )
    process_parser.add_argument(
        "chirp_file",
        type=Path,
        help="Chirp parameters file"
    )
    process_parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("processed"),
        help="Output directory"
    )

    args = parser.parse_args()

    if args.command == "chirp-fit":
        run_chirp_fit(args)
    elif args.command == "process":
        run_process(args)
    else:
        parser.print_help()


def run_chirp_fit(args):
    """Run chirp fitting."""
    from .io import load_ta_data, save_chirp_params
    from .chirp import fit_chirp

    # Load data
    data = load_ta_data(
        args.data_dir / "wavelength.dat",
        args.data_dir / "delay.dat",
        args.data_dir / "signal.dat",
    )

    # Fit chirp
    params = fit_chirp(
        data,
        wavelength_bounds=(args.wvln_min, args.wvln_max)
    )

    # Save parameters
    save_chirp_params(args.output, params)
    print(f"Chirp parameters saved to: {args.output}")
    print(f"Parameters: {params}")


def run_process(args):
    """Run TA processing."""
    from .io import load_ta_data, load_chirp_params
    from .chirp import apply_chirp_correction
    from .processing import adjust_sign_convention, subtract_baseline, convert_to_mOD

    # Load data
    data = load_ta_data(
        args.data_dir / "wavelength.dat",
        args.data_dir / "delay.dat",
        args.data_dir / "signal.dat",
    )

    # Load chirp parameters
    chirp_params = load_chirp_params(args.chirp_file)

    # Process
    data = apply_chirp_correction(data, chirp_params)
    data = adjust_sign_convention(data)
    data = subtract_baseline(data)
    data = convert_to_mOD(data)

    # Save (TODO: implement proper saving)
    args.output.mkdir(exist_ok=True)
    print(f"Processed data would be saved to: {args.output}")
    print(f"Final shape: {data.shape}")


if __name__ == "__main__":
    main()
