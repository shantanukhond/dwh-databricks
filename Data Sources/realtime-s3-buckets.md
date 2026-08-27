# Public S3 Buckets with Frequent Weather / Environmental Data

Sorted by update frequency, fastest to slowest. All buckets are public (NOAA Open Data Dissemination / AWS Open Data Registry) — no AWS credentials required, just use `--no-sign-request`.

| Bucket | Data | Update Frequency | Access |
|---|---|---|---|
| `noaa-nexrad-level2` | Raw weather radar scans | ~5–10 min per station | `aws s3 ls s3://noaa-nexrad-level2/ --no-sign-request` |
| `noaa-goes16` / `noaa-goes18` / `noaa-goes19` | GOES satellite imagery (visible, IR, water vapor) | Continuously updated as new data arrives; new scans every ~5–15 min | `aws s3 ls s3://noaa-goes19/ --no-sign-request` |
| `noaa-jpss` (VIIRS/ATMS instruments) | Polar-orbiting satellite data | Continuously updated; per-orbit, ~every 90 min per satellite | `aws s3 ls s3://noaa-jpss/ --no-sign-request` |
| `noaa-gmgsi-pds` | Global mosaic of geostationary satellite imagery (VIS/IR/WV composites) | Every ~3 hours | `aws s3 ls s3://noaa-gmgsi-pds/ --no-sign-request` |
| `noaa-hrrr-bdp-pds` | High-Resolution Rapid Refresh forecast model | Hourly | `aws s3 ls s3://noaa-hrrr-bdp-pds/ --no-sign-request` |
| `noaa-ofs-pds` | Coastal/ocean forecast model output | Hourly-ish (30-day rolling retention) | `aws s3 ls s3://noaa-ofs-pds/ --no-sign-request` |
| `noaa-gfs-bdp-pds` / `noaa-gfs-pds` | Global Forecast System model | Rolling four-week archive; new cycle every 6 hours | `aws s3 ls s3://noaa-gfs-bdp-pds/ --no-sign-request` |
| `openaq-data-archive` | Global air quality sensor readings | Every few hours (varies by station) | `aws s3 ls s3://openaq-data-archive/ --no-sign-request` |
| `noaa-ghcn-pds` | Global Historical Climatology Network (station temps, precip) | Daily | `aws s3 ls s3://noaa-ghcn-pds/ --no-sign-request` |
| `noaa-cdr-total-solar-irradiance-pds` | Climate Data Records (solar irradiance, etc.) | Daily to monthly | `aws s3 ls s3://noaa-cdr-total-solar-irradiance-pds/ --no-sign-request` |
| `noaa-wod-pds` | World Ocean Database (historical ocean profiles) | Quarterly | `aws s3 ls s3://noaa-wod-pds/ --no-sign-request` |

## Notes

- Exact cadence for NEXRAD/GOES/JPSS isn't published as a fixed SLA — it's continuous/event-driven, so intervals above are typical real-world figures, not guarantees.
- All buckets are readable via the AWS CLI or boto3 (Python) without an AWS account, using the `--no-sign-request` flag or `Config(signature_version=UNSIGNED)` in boto3.
- Source: [AWS Open Data Registry](https://registry.opendata.aws) / NOAA Open Data Dissemination (NODD) Program.
