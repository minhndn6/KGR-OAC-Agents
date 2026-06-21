import json, shutil
from pathlib import Path

it = Path(r"C:\Project\Dataflow-builder\.claude\skills\oac-dataflow-builder-workspace\iteration-1")
for eval_dir in sorted(it.glob("eval-*")):
    for config in ["with_skill", "without_skill"]:
        cdir = eval_dir / config
        if not cdir.exists():
            continue
        run_dir = cdir / "run-1"
        run_dir.mkdir(exist_ok=True)
        # move grading.json, timing.json, outputs into run-1
        for name in ["grading.json", "timing.json", "outputs"]:
            src = cdir / name
            if src.exists():
                dst = run_dir / name
                if dst.exists():
                    continue
                shutil.move(str(src), str(dst))
        # patch grading.json with summary
        gf = run_dir / "grading.json"
        if gf.exists():
            g = json.loads(gf.read_text(encoding="utf-8"))
            exps = g.get("expectations", [])
            passed = sum(1 for e in exps if e.get("passed"))
            total = len(exps)
            g["summary"] = {
                "passed": passed,
                "failed": total - passed,
                "total": total,
                "pass_rate": round(passed / total, 4) if total else 0.0,
            }
            gf.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{eval_dir.name}/{config}: {passed}/{total}")
print("done")
