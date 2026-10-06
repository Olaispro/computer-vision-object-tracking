"""Greedy IoU tracker for normalized or pixel xyxy detections."""
import argparse,csv,json

def iou(a,b):
    x1=max(a[0],b[0]);y1=max(a[1],b[1]);x2=min(a[2],b[2]);y2=min(a[3],b[3]); inter=max(0,x2-x1)*max(0,y2-y1)
    area=lambda q:max(0,q[2]-q[0])*max(0,q[3]-q[1])
    u=area(a)+area(b)-inter;return inter/u if u else 0.0

def track(rows, threshold=.25, max_gap=1):
    active={}; next_id=1; output=[]
    for frame in sorted({int(r['frame']) for r in rows}):
        dets=[r for r in rows if int(r['frame'])==frame]; candidates=[]
        for tid,t in active.items():
            if frame-t['frame']<=max_gap+1:
                for j,d in enumerate(dets):
                    if t['label']==d['label']:
                        box=[float(d[k]) for k in ('x1','y1','x2','y2')]; candidates.append((iou(t['box'],box),tid,j,box))
        used_t=set();used_d=set()
        for score,tid,j,box in sorted(candidates,reverse=True):
            if score>=threshold and tid not in used_t and j not in used_d:
                d=dets[j];active[tid]={'box':box,'frame':frame,'label':d['label']};output.append({**d,'track_id':tid,'iou':round(score,3)});used_t.add(tid);used_d.add(j)
        for j,d in enumerate(dets):
            if j not in used_d:
                box=[float(d[k]) for k in ('x1','y1','x2','y2')];active[next_id]={'box':box,'frame':frame,'label':d['label']};output.append({**d,'track_id':next_id,'iou':None});next_id+=1
    return output

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--out',default='tracks.json');a=p.parse_args()
    with open(a.input,encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    result=track(rows);open(a.out,'w',encoding='utf-8').write(json.dumps(result,indent=2));print(f'{len(result)} detections -> {a.out}')
if __name__=='__main__':main()
