class CSVExporter:
    @staticmethod
    def export_transactions(history: list, filepath: str) -> bool:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("trx_id,type,amount,category,timestamp\n")
                for trx in history:
                    f.write(trx.to_csv_row() + "\n")
            return True
        except Exception as e:
            print(f"Export Error: {e}")
            return False