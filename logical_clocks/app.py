from virtual_machine import run_virtual_machine
import argparse
import json

#python3 app.py --machine_id machine_2

def main():
    # Parse configurations to get machine ids
    json_data = open('config.json').read()
    config = json.loads(json_data)
    machine_ids = config.keys()

    # create parser
    parser = argparse.ArgumentParser()

    # add argument
    parser.add_argument("--machine_id", help="Pass Machine ID",
                        type=str, choices=machine_ids, required=True)

    args = parser.parse_args()

    if args.machine_id and args.machine_id in machine_ids:
        run_virtual_machine(args.machine_id)

if __name__ == '__main__':
    main()    