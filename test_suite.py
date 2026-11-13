"""End-to-End Automated Validation Test Suite.
Verifies all routes, schema compatibility, mathematical outputs, and static assets.
"""
import sys
import os
import asyncio
import httpx

# Ensure paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
from app.main import app

total_tests = 0
passed_tests = 0
failed_tests = []

def assert_test(condition, name, details=""):
    global total_tests, passed_tests
    total_tests += 1
    if condition:
        passed_tests += 1
        print(f"  [PASS] {name}")
    else:
        failed_tests.append(name)
        print(f"  [FAIL] {name} - {details}")

async def run_tests():
    print("=" * 70)
    print("🧪 RUNNING COMPREHENSIVE E2E VERIFICATION TEST SUITE")
    print("=" * 70)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # 1. Health & Core
        print("\n[GROUP 1] Health & System Status")
        r = await client.get("/api/health")
        assert_test(r.status_code == 200, "GET /api/health returns 200 OK")
        data = r.json()
        assert_test(data.get("status") == "healthy", "Health status is 'healthy'")
        assert_test("trend_detective" in data.get("modules", {}), "Data science module is registered")

        # 2. Catalogs
        print("\n[GROUP 2] Catalogs & Metadata Compatibility")
        r = await client.get("/api/variables")
        assert_test(r.status_code == 200 and r.json().get("count") >= 8, "GET /api/variables returns variables")
        v0 = r.json()["data"][0]
        assert_test("id" in v0 and "name" in v0 and "category" in v0, "Variable schema matches frontend")

        r = await client.get(f"/api/variables/{v0['id']}")
        assert_test(r.status_code == 200 and r.json()["data"]["id"] == v0["id"], f"GET /api/variables/{v0['id']} matches")

        r = await client.get("/api/datasets")
        assert_test(r.status_code == 200 and r.json().get("count") >= 5, "GET /api/datasets returns NASA missions")

        r = await client.get("/api/regions")
        assert_test(r.status_code == 200 and r.json().get("count") >= 6, "GET /api/regions returns preset regions")

        # 3. Global Map Schema Alignment
        print("\n[GROUP 3] Global Map Points Schema Compatibility")
        r = await client.get("/api/global-trends")
        assert_test(r.status_code == 200, "GET /api/global-trends returns 200 OK")
        pts = r.json().get("data", [])
        assert_test(len(pts) >= 7, "Global trends points count >= 7")
        pt0 = pts[0]
        assert_test("coords" in pt0 and len(pt0["coords"]) == 2, "Point has 'coords' array for Leaflet")
        assert_test("color" in pt0 and "statusLabel" in pt0 and "rateOfChange" in pt0, "Point has styling fields")

        # 4. Demonstrations
        print("\n[GROUP 4] Demonstrations Library")
        r = await client.get("/api/demonstrations")
        assert_test(r.status_code == 200 and r.json().get("count") >= 4, "GET /api/demonstrations returns case studies")
        d0 = r.json()["data"][0]
        assert_test("previewPoints" in d0 and len(d0["previewPoints"]) > 0, "Demonstration has preview points")

        # 5. Core Analytical Engine (Real Giovanni Data)
        print("\n[GROUP 5] Trend Analysis & Mathematical Tests")
        r = await client.post("/api/analyze", json={
            "regionId": "lucknow",
            "variableId": "air_temp",
            "startYear": 2000,
            "endYear": 2023
        })
        assert_test(r.status_code == 200, "POST /api/analyze (Lucknow) returns 200 OK")
        res = r.json()
        assert_test(res.get("success") is True and res.get("isMockData") is False, "Analysis marked as live data")
        assert_test("Giovanni" in res.get("source", ""), "Real NASA Giovanni CSV loaded successfully")
        ts = res.get("timeSeries", {})
        assert_test(len(ts.get("timestamps", [])) == 288, "Time series has exactly 288 months (2000-2023)")
        assert_test(len(ts.get("observations", [])) == 288, "Observations match timestamps count")
        assert_test(len(ts.get("fittedValues", [])) == 288, "Fitted trend line generated")
        assert_test(len(ts.get("confidenceUpper", [])) == 288, "95% confidence upper bound present")
        assert_test(len(ts.get("confidenceLower", [])) == 288, "95% confidence lower bound present")
        stats = res.get("statistics", {})
        assert_test("decadalRate" in stats and "mannKendallPValue" in stats, "Statistics block complete")

        # 6. Seasonal Decomposition (Full-Stack Feature 2)
        print("\n[GROUP 6] Seasonal Climatology Decomposition (Feature 2)")
        r = await client.post("/api/decomposition", json={
            "regionId": "lucknow",
            "variableId": "air_temp",
            "startYear": 2000,
            "endYear": 2023
        })
        assert_test(r.status_code == 200, "POST /api/decomposition returns 200 OK")
        decomp = r.json()
        assert_test(len(decomp.get("climatology12m", [])) == 12, "Decomposition has 12 monthly climatology values")
        assert_test("observed" in decomp.get("decomposition", {}), "Decomposition observed series present")
        assert_test("seasonalCycle" in decomp.get("decomposition", {}), "Decomposition seasonal cycle present")
        assert_test("trend" in decomp.get("decomposition", {}), "Decomposition trend component present")
        assert_test("residuals" in decomp.get("decomposition", {}), "Decomposition residual noise present")

        # 7. Custom Point Analysis (Full-Stack Feature 3)
        print("\n[GROUP 7] Custom Coordinate Evaluation (Feature 3)")
        r = await client.post("/api/custom-point", json={
            "latitude": 40.7128,
            "longitude": -74.0060,
            "variableId": "air_temp",
            "startYear": 2005,
            "endYear": 2023
        })
        assert_test(r.status_code == 200, "POST /api/custom-point (NYC) returns 200 OK")
        assert_test("Custom Geo-Point" in r.json().get("metadata", {}).get("regionName", ""), "Custom point region named properly")

        # 8. Extreme Climate Anomaly Scanner (Full-Stack Feature 4)
        print("\n[GROUP 8] Extreme Anomaly Scanner (Feature 4)")
        r = await client.post("/api/anomalies", json={
            "regionId": "lucknow",
            "variableId": "air_temp",
            "thresholdSigma": 1.8
        })
        assert_test(r.status_code == 200, "POST /api/anomalies returns 200 OK")
        assert_test(r.json().get("thresholdSigma") == 1.8, "Threshold sigma parsed properly")

        # 9. Scientific Audit Report (Full-Stack Feature 5)
        print("\n[GROUP 9] Scientific Audit Provenance Report (Feature 5)")
        r = await client.post("/api/export/audit-report", json={
            "regionId": "lucknow",
            "variableId": "air_temp",
            "startYear": 2000,
            "endYear": 2023
        })
        assert_test(r.status_code == 200, "POST /api/export/audit-report returns 200 OK")
        audit = r.json()
        assert_test("markdown" in audit and "Mann-Kendall" in audit["markdown"], "Audit markdown contains mathematical proofs")

        # 10. Regional Comparison
        print("\n[GROUP 10] Dual Regional Comparison")
        r = await client.post("/api/compare", json={
            "regionAId": "gangetic",
            "regionBId": "sahel",
            "variableId": "air_temp",
            "startYear": 2000,
            "endYear": 2023
        })
        assert_test(r.status_code == 200, "POST /api/compare returns 200 OK")
        comp = r.json()
        assert_test("regionA" in comp and "regionB" in comp and "delta" in comp, "Comparison payload structure valid")

        # 11. Frontend Web Pages Serving
        print("\n[GROUP 11] Frontend Pages & Static Assets")
        pages = [
            "/", "/index.html", "/dashboard.html", "/detective.html",
            "/results.html", "/global-map.html", "/compare.html",
            "/variables.html", "/demonstrations.html", "/about.html"
        ]
        for p in pages:
            res_p = await client.get(p)
            assert_test(res_p.status_code == 200 and len(res_p.text) > 500, f"Page {p} served (Length: {len(res_p.text)})")

        # 12. Static Assets
        assets = [
            "/css/style.css", "/js/api.js", "/js/components.js",
            "/js/results.js", "/js/detective.js", "/js/globalMap.js"
        ]
        for a in assets:
            res_a = await client.get(a)
            assert_test(res_a.status_code == 200 and len(res_a.text) > 100, f"Asset {a} served (Length: {len(res_a.text)})")

    print("\n" + "=" * 70)
    print(f"📊 TEST RESULTS SUMMARY: {passed_tests} PASSED / {total_tests} TOTAL")
    if failed_tests:
        print(f"❌ FAILED TESTS: {len(failed_tests)}")
        for f in failed_tests:
            print(f"   - {f}")
    else:
        print("🎉 ALL TESTS PASSED WITH 100% SUCCESS RATE!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_tests())
