import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="kiranl-p-1.3 AI reporting")
    parser.add_argument("-r", "--run", help="Run specific action.", choices=["training", "nlsql"])

    args = parser.parse_args()
    match args.run.lower():
        case "training":
            from engines.training import Training
            t = Training()
            t.run()
        case "nlsql":
            from engines.nlsql import Nlsql
            n = Nlsql()

            example_prompt: str = "tampilkan total tagihan dan tgl pembayaran untuk lporan tgihan air tahun 2022 dalam bentuk bar chart"
            response = n.run(example_prompt)
            print(response)
        case _:
            print("command not found!")