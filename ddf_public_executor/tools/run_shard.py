#!/usr/bin/env python3
import argparse, hashlib, json, pathlib, re, subprocess, time

p=argparse.ArgumentParser()
p.add_argument("--worker",type=int,required=True)
p.add_argument("--workers",type=int,default=256)
p.add_argument("--count",type=int,default=4096)
a=p.parse_args()

root=pathlib.Path(__file__).resolve().parents[1]
out=root/"out"/f"worker_{a.worker:03d}"
out.mkdir(parents=True,exist_ok=True)

widths=[64,128,256,512]
stages=[4,6,8,10]
banks=[2,4,8,16]
gates=[1,2,4,8]
modes=[0,1,2,3]
strategies=["balanced","area","speed","retime"]

def cfg(cid):
    x=cid
    return {
      "candidate_id":cid,
      "data_w":widths[x%4],
      "stages":stages[(x//4)%4],
      "state_banks":banks[(x//16)%4],
      "invariant_gates":gates[(x//64)%4],
      "mode":modes[(x//256)%4],
      "strategy":strategies[(x//1024)%4]
    }

def run(cmd):
    t=time.time()
    cp=subprocess.run(cmd,shell=True,cwd=root,text=True,capture_output=True)
    return cp.returncode,time.time()-t,cp.stdout[-12000:],cp.stderr[-12000:]

passes={
 "balanced":"proc; opt; memory; opt; techmap; opt; abc; stat",
 "area":"proc; flatten; opt -full; memory; opt -full; techmap; abc -g simple; stat",
 "speed":"proc; opt; memory; opt; techmap; abc -fast; opt; stat",
 "retime":"proc; opt; memory; opt; techmap; abc -dff; opt; stat",
}

results=[]
for cid in range(a.worker,a.count,a.workers):
    c=cfg(cid)
    ys=out/f"c{cid:04d}.ys"
    ys.write_text(
      "read_verilog -sv rtl/ddf_node.sv rtl/invariant_gate.sv rtl/ddf_pipeline.sv\n"
      "hierarchy -top ddf_pipeline\n"
      f"chparam -set DATA_W {c['data_w']} ddf_pipeline\n"
      f"chparam -set STAGES {c['stages']} ddf_pipeline\n"
      f"chparam -set STATE_BANKS {c['state_banks']} ddf_pipeline\n"
      f"chparam -set INVARIANT_GATES {c['invariant_gates']} ddf_pipeline\n"
      f"chparam -set MODE {c['mode']} ddf_pipeline\n"
      +passes[c["strategy"]]+"\n"
    )
    rc,sec,stdout,stderr=run(f"yosys -q -s {ys}")
    raw=json.dumps(c,sort_keys=True,separators=(",",":")).encode()
    rec={
      "config":c,
      "identity_sha256":hashlib.sha256(raw).hexdigest(),
      "pass":rc==0,
      "seconds":round(sec,4),
      "stdout_tail":stdout[-4000:],
      "stderr_tail":stderr[-4000:]
    }
    results.append(rec)

summary={
 "worker":a.worker,
 "candidate_count":len(results),
 "passed":sum(r["pass"] for r in results),
 "failed":sum(not r["pass"] for r in results),
 "seconds":round(sum(r["seconds"] for r in results),4),
 "core_access":"DENY",
 "certification_host_access":"DENY"
}
(out/"results.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
(out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
print(json.dumps(summary,sort_keys=True))
