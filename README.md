# Internship Board

My Summer 2027 internship tracker: applications, matching postings, resume picks and fit scores.

- `index.html` — the whole app (no build step)
- `firebase-config.js` — Firebase project config (public by design)
- `firestore.rules` — database rules: each user can only read/write their own data
- `build_feed.py` — pulls matching postings from the SimplifyJobs Summer 2027 list into `feed.json`
- `.github/workflows/refresh-postings.yml` — runs `build_feed.py` every morning and commits `feed.json`

Hosted on GitHub Pages. Login and storage via Firebase (Google sign-in + Firestore).
