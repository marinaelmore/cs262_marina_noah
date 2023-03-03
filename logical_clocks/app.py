from virtual_machine import main
import argparse
import asyncio



if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser()
    # add argument
    parser.add_argument("--machine_id", help="Pass Machine ID",
                        type=str, choices=["machine_1", "machine_2", "machine_3"], required=True)

    args = parser.parse_args()

    if args.machine_id:
        #asyncio.run(main(args.machine_id))
        main(args.machine_id)