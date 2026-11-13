import time
import urllib.request
import json

def test_live():
    print("Testing live endpoints against http://127.0.0.1:8000 ...", flush=True)

    # Wait for server to become responsive
    healthy = False
    for i in range(25):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=3) as r:
                d = json.loads(r.read())
                if d.get("status") == "healthy":
                    healthy = True
                    print(f"[PASS] Health Check: {d.get('status')} (Ready after {i+1}s)", flush=True)
                    break
        except Exception:
            time.sleep(1)

    if not healthy:
        raise SystemExit("Server failed to respond within 25 seconds.")
        
    # 2. Variables
    with urllib.request.urlopen("http://127.0.0.1:8000/api/variables", timeout=5) as r:
        d = json.loads(r.read())
        print(f"[PASS] Variables count: {d.get('count')}", flush=True)

    # 3. Global Trends
    with urllib.request.urlopen("http://127.0.0.1:8000/api/global-trends", timeout=5) as r:
        d = json.loads(r.read())
        print(f"[PASS] Global trends count: {d.get('count')}, Sample Coords: {d['data'][0]['coords']}", flush=True)

    # 4. Demonstrations
    with urllib.request.urlopen("http://127.0.0.1:8000/api/demonstrations", timeout=5) as r:
        d = json.loads(r.read())
        print(f"[PASS] Demonstrations count: {d.get('count')}", flush=True)

    # 5. Analyze (Lucknow Ground-Truth)
    req_data = json.dumps({
        "regionId": "lucknow",
        "variableId": "air_temp",
        "startYear": 2000,
        "endYear": 2023
    }).encode("utf-8")
    req = urllib.request.Request("http://127.0.0.1:8000/api/analyze", data=req_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read())
        print(f"[PASS] Analyze Lucknow: {d['statistics']['decadalRate']} C/dec | Source: {d['source']} | Anomalies: {len(d.get('anomalies', []))}", flush=True)

    # 6. Seasonal Decomposition (Full-Stack Feature 2)
    dec_data = json.dumps({"regionId": "lucknow", "variableId": "air_temp"}).encode("utf-8")
    req2 = urllib.request.Request("http://127.0.0.1:8000/api/decomposition", data=dec_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req2, timeout=10) as r:
        d = json.loads(r.read())
        print(f"[PASS] Seasonal Decomposition 12m: {d['climatology12m'][:4]}...", flush=True)

    # 7. Custom Point (Full-Stack Feature 3)
    pt_data = json.dumps({"latitude": 34.05, "longitude": -118.25, "variableId": "air_temp"}).encode("utf-8")
    req3 = urllib.request.Request("http://127.0.0.1:8000/api/custom-point", data=pt_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req3, timeout=10) as r:
        d = json.loads(r.read())
        print(f"[PASS] Custom Point (LA): {d['metadata']['regionName']} | Rate: {d['statistics']['decadalRate']}", flush=True)

    # 8. Extreme Anomalies (Full-Stack Feature 4)
    anom_data = json.dumps({"regionId": "lucknow", "thresholdSigma": 1.5}).encode("utf-8")
    req4 = urllib.request.Request("http://127.0.0.1:8000/api/anomalies", data=anom_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req4, timeout=10) as r:
        d = json.loads(r.read())
        print(f"[PASS] Extreme Anomalies: {d['totalAnomaliesDetected']} events detected at > 1.5 sigma", flush=True)

    # 9. Audit Report (Full-Stack Feature 5)
    audit_data = json.dumps({"regionId": "lucknow", "variableId": "air_temp"}).encode("utf-8")
    req5 = urllib.request.Request("http://127.0.0.1:8000/api/export/audit-report", data=audit_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req5, timeout=10) as r:
        d = json.loads(r.read())
        print(f"[PASS] Audit Report Generated: ID: {d['analysisId']}", flush=True)

    # 10. Frontend Static HTML Pages
    for page in ["/", "/index.html", "/dashboard.html", "/detective.html", "/results.html", "/global-map.html", "/compare.html", "/variables.html", "/demonstrations.html", "/about.html"]:
        with urllib.request.urlopen(f"http://127.0.0.1:8000{page}", timeout=5) as r:
            assert r.status == 200
    print("[PASS] All 10 Frontend HTML Pages served with HTTP 200 OK!", flush=True)

    print("\n>>> ALL TEST CHECKS PASSED LIVE OVER HTTP! FULL-STACK 100% HEALTHY <<<", flush=True)

if __name__ == "__main__":
    test_live()
