# API Test Cases

---

## Endpoint 1 — GET `/api/hazards` (All Layers)

### TC-1.1 — Fetch all hazard layers (no filter)
```bash
curl -X GET http://localhost:5000/api/hazards
```
**Expected:** `200 OK` — FeatureCollection with all records across all hazard types. `count` reflects total rows in `hazard_layers`.

---

### TC-1.2 — Response structure validation
```bash
curl -X GET http://localhost:5000/api/hazards
```
**Expected:** Response contains `type`, `features`, `status`, and `count` fields. Each feature has `type`, `geometry`, and `properties` with `hazard_type` and `hazard_level`.

---

### TC-1.3 — Empty database returns empty FeatureCollection
> Simulate by querying against an empty or freshly created table.

**Expected:**
```json
{
  "type": "FeatureCollection",
  "features": [],
  "status": "success",
  "count": 0
}
```

---

## Endpoint 2 — GET `/api/hazards?type={hazard_type}` (Filtered)

### TC-2.1 — Filter by `flood`
```bash
curl -X GET "http://localhost:5000/api/hazards?type=flood"
```
**Expected:** `200 OK` — Only features where `hazard_type` is `flood`. `count` reflects filtered results only.

---

### TC-2.2 — Filter by `landslide`
```bash
curl -X GET "http://localhost:5000/api/hazards?type=landslide"
```
**Expected:** `200 OK` — Only features where `hazard_type` is `landslide`.

---

### TC-2.3 — Filter by `storm_surge`
```bash
curl -X GET "http://localhost:5000/api/hazards?type=storm_surge"
```
**Expected:** `200 OK` — Only features where `hazard_type` is `storm_surge`.

---

### TC-2.4 — Case-insensitive filter (`FLOOD`)
```bash
curl -X GET "http://localhost:5000/api/hazards?type=FLOOD"
```
**Expected:** `200 OK` — Returns flood results. The query uses `ILIKE` so casing should not matter.

---

### TC-2.5 — Partial match filter (`flo`)
```bash
curl -X GET "http://localhost:5000/api/hazards?type=flo"
```
**Expected:** `200 OK` — Returns flood results due to `ILIKE %flo%` matching.

---

### TC-2.6 — Filter with unknown/nonexistent type
```bash
curl -X GET "http://localhost:5000/api/hazards?type=earthquake"
```
**Expected:**
```json
{
  "type": "FeatureCollection",
  "features": [],
  "status": "success",
  "count": 0
}
```

---

## Endpoint 3 — POST `/api/risk-assessment`

### Valid Coordinates — Cebu Locations

#### TC-3.1 — Cebu City (Capital)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3157, "longitude": 123.8854}'
```
**Location:** Cebu City (Capital)
**Expected:** `200 OK` with `success: true`, valid `risk_level`, and computed spatial features.

---

#### TC-3.2 — Mandaue City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3323, "longitude": 123.9357}'
```
**Location:** Mandaue City

---

#### TC-3.3 — Lapu-Lapu City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3103, "longitude": 123.9490}'
```
**Location:** Lapu-Lapu City

---

#### TC-3.4 — Talisay City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.2447, "longitude": 123.8481}'
```
**Location:** Talisay City

---

#### TC-3.5 — Toledo City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3776, "longitude": 123.6358}'
```
**Location:** Toledo City

---

#### TC-3.6 — Danao City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.5218, "longitude": 124.0298}'
```
**Location:** Danao City

---

#### TC-3.7 — Carcar City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.1042, "longitude": 123.6425}'
```
**Location:** Carcar City

---

#### TC-3.8 — Naga City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.2104, "longitude": 123.7578}'
```
**Location:** Naga City

---

#### TC-3.9 — Bogo City
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.0517, "longitude": 124.0044}'
```
**Location:** Bogo City

---

#### TC-3.10 — Moalboal
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.9542, "longitude": 123.4007}'
```
**Location:** Moalboal

---

#### TC-3.11 — Oslob
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.4815, "longitude": 123.4300}'
```
**Location:** Oslob

---

#### TC-3.12 — Bantayan Island
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.1965, "longitude": 123.7317}'
```
**Location:** Bantayan Island

---

#### TC-3.13 — Malapascua Island
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.3344, "longitude": 124.1165}'
```
**Location:** Malapascua Island

---

#### TC-3.14 — Badian (Kawasan Falls)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.8034, "longitude": 123.3661}'
```
**Location:** Badian (Kawasan Falls)

---

#### TC-3.15 — Liloan
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.4011, "longitude": 124.0003}'
```
**Location:** Liloan

---

#### TC-3.16 — Consolacion
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3804, "longitude": 123.9680}'
```
**Location:** Consolacion

---

#### TC-3.17 — Compostela
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.4533, "longitude": 124.0083}'
```
**Location:** Compostela

---

#### TC-3.18 — Minglanilla
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.2450, "longitude": 123.7954}'
```
**Location:** Minglanilla

---

#### TC-3.19 — Argao
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.8824, "longitude": 123.5985}'
```
**Location:** Argao

---

#### TC-3.20 — Dalaguete
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.7575, "longitude": 123.5303}'
```
**Location:** Dalaguete

---

#### TC-3.21 — Sibonga
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.0105, "longitude": 123.6212}'
```
**Location:** Sibonga

---

#### TC-3.22 — Aloguinsan
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.2222, "longitude": 123.5186}'
```
**Location:** Aloguinsan

---

#### TC-3.23 — Balamban
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.5057, "longitude": 123.7171}'
```
**Location:** Balamban

---

#### TC-3.24 — Asturias
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.5639, "longitude": 123.7171}'
```
**Location:** Asturias

---

#### TC-3.25 — Tuburan
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.7259, "longitude": 123.8267}'
```
**Location:** Tuburan

---

#### TC-3.26 — San Remigio
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.0028, "longitude": 123.9351}'
```
**Location:** San Remigio

---

#### TC-3.27 — Medellin
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.1303, "longitude": 123.9620}'
```
**Location:** Medellin

---

#### TC-3.28 — Daanbantayan
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.2721, "longitude": 124.0028}'
```
**Location:** Daanbantayan

---

#### TC-3.29 — Samboan
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.4528, "longitude": 123.3283}'
```
**Location:** Samboan

---

#### TC-3.30 — Boljoon
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.6464, "longitude": 123.4795}'
```
**Location:** Boljoon

---

**Expected response shape for all valid TC-3.x cases:**
```json
{
  "success": true,
  "data": {
    "risk_level": "<none|low|medium|high>",
    "features": {
      "distance_to_nearest_hazard": "<float, metres>",
      "overlapping_hazards": "<integer>"
    }
  }
}
```

---

### Invalid Coordinates — Expected `400 Bad Request`

**Expected response for all invalid TC-3.INV cases:**
```json
{
  "success": false,
  "error": "Invalid or non-Cebu coordinates"
}
```

---

#### TC-3.INV-1 — Metro Manila (outside Cebu bounds)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 14.5995, "longitude": 120.9842}'
```
**Reason:** Latitude 14.59 > 11.3 upper bound.

---

#### TC-3.INV-2 — Davao City (outside Cebu bounds)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 7.1907, "longitude": 125.4553}'
```
**Reason:** Both lat and lon outside Cebu bounds.

---

#### TC-3.INV-3 — Lat exactly at lower bound minus epsilon
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.3999, "longitude": 123.8000}'
```
**Reason:** Latitude 9.3999 < 9.4 lower bound.

---

#### TC-3.INV-4 — Lon exactly at upper bound plus epsilon
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3157, "longitude": 124.1001}'
```
**Reason:** Longitude 124.1001 > 124.1 upper bound.

---

#### TC-3.INV-5 — Negative latitude (Southern Hemisphere)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": -10.3157, "longitude": 123.8854}'
```
**Reason:** Negative latitude is outside Cebu bounds.

---

#### TC-3.INV-6 — Zero coordinates (Null Island)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 0.0, "longitude": 0.0}'
```
**Reason:** 0,0 is in the Atlantic Ocean — treated as falsy by `if not lat or not lon`.

---

#### TC-3.INV-7 — Missing latitude field
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"longitude": 123.8854}'
```
**Reason:** `latitude` is `None`, fails the `if not lat` check.

---

#### TC-3.INV-8 — Missing longitude field
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.3157}'
```
**Reason:** `longitude` is `None`, fails the `if not lon` check.

---

#### TC-3.INV-9 — Empty request body
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{}'
```
**Reason:** Both fields are `None`.

---

#### TC-3.INV-10 — String values instead of numbers
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": "ten", "longitude": "onehundred"}'
```
**Reason:** Non-numeric values will fail bounds comparison and throw a TypeError.

---

#### TC-3.INV-11 — Valid lat, lon swapped (lon in lat field)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 123.8854, "longitude": 10.3157}'
```
**Reason:** Swapped values — latitude 123.88 exceeds all valid bounds.

---

#### TC-3.INV-12 — Coordinates in Bohol (adjacent province, not Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.8500, "longitude": 124.1433}'
```
**Reason:** Longitude 124.1433 > 124.1 upper bound for Cebu.

---

#### TC-3.INV-13 — Coordinates in Negros Oriental (west of Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.7500, "longitude": 122.9800}'
```
**Reason:** Longitude 122.98 < 123.2 lower bound for Cebu.

---

#### TC-3.INV-14 — Leyte coordinates (north-east of Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.0000, "longitude": 124.7500}'
```
**Reason:** Longitude 124.75 > 124.1 upper bound for Cebu.

---

#### TC-3.INV-15 — Latitude above upper bound (north of Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.4000, "longitude": 123.9000}'
```
**Reason:** Latitude 11.4 > 11.3 upper bound for Cebu.

---

#### TC-3.INV-16 — Both fields null explicitly
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": null, "longitude": null}'
```
**Reason:** `None` values fail the `if not lat or not lon` guard.

---

#### TC-3.INV-17 — Non-JSON content type
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: text/plain" \
  -d '{"latitude": 10.3157, "longitude": 123.8854}'
```
**Reason:** `request.json` returns `None` when Content-Type is not `application/json`, causing `data.get()` to fail.

---

#### TC-3.INV-18 — Coordinates in the open sea west of Cebu
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.5000, "longitude": 122.5000}'
```
**Reason:** Longitude 122.5 < 123.2 lower bound.

---

#### TC-3.INV-19 — Camiguin Island (north of Cebu bounds)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.1800, "longitude": 124.7200}'
```
**Reason:** Both lat and lon outside Cebu bounds.

---

#### TC-3.INV-20 — Extremely large coordinate values
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 999.0, "longitude": 999.0}'
```
**Reason:** Far outside any valid geographic or Cebu-specific bounds.

---

#### TC-3.INV-21 — Infinity values
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 1e308, "longitude": 1e308}'
```
**Reason:** Overflow values that will fail all bounds checks.

---

#### TC-3.INV-22 — Siquijor Island (outside Cebu province)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.2000, "longitude": 123.5100}'
```
**Reason:** Latitude 9.2 < 9.4 lower bound for Cebu.

---

#### TC-3.INV-23 — Cebu lat, invalid lon (just over eastern bound)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.5000, "longitude": 124.2000}'
```
**Reason:** Longitude 124.2 > 124.1 upper bound.

---

#### TC-3.INV-24 — Valid lon, lat just below southern bound
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 9.3500, "longitude": 123.5000}'
```
**Reason:** Latitude 9.35 < 9.4 lower bound.

---

#### TC-3.INV-25 — Boolean values instead of floats
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": true, "longitude": false}'
```
**Reason:** Booleans coerce to 1 and 0 in Python — both are outside Cebu bounds and `lon=0` triggers the falsy guard.

---

#### TC-3.INV-26 — Array instead of scalar
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": [10.3157], "longitude": [123.8854]}'
```
**Reason:** List values will fail the numeric bounds comparison and raise a TypeError.

---

#### TC-3.INV-27 — Zamboanga City (Mindanao, far outside Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 6.9214, "longitude": 122.0790}'
```
**Reason:** Both coordinates far outside Cebu bounds.

---

#### TC-3.INV-28 — Iloilo City (Visayas, but not Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 10.7202, "longitude": 122.5621}'
```
**Reason:** Longitude 122.56 < 123.2 lower bound.

---

#### TC-3.INV-29 — Tacloban City, Leyte (east of Cebu)
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json" \
  -d '{"latitude": 11.2443, "longitude": 125.0039}'
```
**Reason:** Longitude 125.0 > 124.1 upper bound.

---

#### TC-3.INV-30 — Entirely missing request body
```bash
curl -X POST http://localhost:5000/api/risk-assessment \
  -H "Content-Type: application/json"
```
**Reason:** `request.json` returns `None`, causing `data.get()` to raise `AttributeError`.
