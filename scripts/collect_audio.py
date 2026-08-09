#!/usr/bin/env python3
"""
把來源音檔挑出來、改成 app 需要的檔名。

用法：
    python3 scripts/collect_audio.py --src ~/Downloads/moe_audio
    python3 scripts/collect_audio.py --src ~/Downloads/moe_audio --ext wav --copy

比對方式是「來源檔名裡有沒有出現這個漢字」。教育部那包的命名規則我不確定，
所以如果比對不到，腳本會列出缺哪些字，你再手動放進去就好——
目標檔名一律小寫，這點很重要，GitHub Pages 區分大小寫。
"""
import argparse, csv, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="解壓後的音檔資料夾")
    ap.add_argument("--ext", default="mp3", help="來源副檔名，預設 mp3")
    ap.add_argument("--copy", action="store_true", help="真的複製，預設只試跑")
    args = ap.parse_args()

    src = pathlib.Path(args.src).expanduser()
    if not src.is_dir():
        sys.exit(f"找不到資料夾：{src}")

    pool = list(src.rglob(f"*.{args.ext}"))
    print(f"來源共 {len(pool)} 個 .{args.ext}")

    rows = list(csv.DictReader((ROOT / "audio" / "mapping.csv").open(encoding="utf-8")))
    hit, miss = 0, []

    for row in rows:
        han, target = row["han"], ROOT / row["target"]
        found = next((p for p in pool if han in p.stem), None)
        if not found:
            miss.append(han)
            continue
        hit += 1
        if args.copy:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(found, target)
        else:
            print(f"  {found.name}  ->  {row['target']}")

    print(f"\n對到 {hit} / {len(rows)}")
    if miss:
        print("缺這些字，請自己補：" + " ".join(miss))
    if not args.copy:
        print("\n這是試跑。確認沒問題後加 --copy 再跑一次。")


if __name__ == "__main__":
    main()
