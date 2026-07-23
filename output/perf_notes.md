# Performance Notes

## Test Environment

- Operating System: Windows 10
- Python Version: 3.11.9
- Database: SQLite (nifty100.db)
- Backend: FastAPI
- Frontend: Streamlit

---

## Performance Tests Performed

### 1. API Load Test

- Concurrent Requests: 10
- Status: PASS
- All requests completed successfully.
- Response time was within the acceptable limit (<10 seconds).

---

### 2. Dashboard Performance

- Company Profile page tested with multiple companies.
- Average page load time was below 3 seconds.
- Charts and tables loaded correctly.

Status: PASS

---

### 3. End-to-End Integration

- FastAPI running on Port 8000.
- Streamlit running on Port 8501.
- No port conflicts detected.
- Dashboard successfully fetched data from the API.

Status: PASS

---

## Bottlenecks Observed

No major performance bottlenecks were identified during testing.

Minor observations:

- First dashboard load may be slightly slower because data is loaded from SQLite.
- Initial API request may experience a small startup delay due to application initialization.
- Subsequent requests are noticeably faster because data and resources are already loaded.

---

## Recommendations

- Add SQLite indexes on frequently queried columns (`company_id`, `year`) to improve query performance.
- Consider API response caching for frequently accessed endpoints.
- Optimize database queries if dataset size increases.
- Use asynchronous endpoints for long-running operations if required.

---

## Overall Result

Performance testing completed successfully.

All performance objectives for Day 43 were achieved.