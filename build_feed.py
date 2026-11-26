import json, re, sys, urllib.request, time
URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/.github/scripts/listings.json"
INC = re.compile(r"embedded|firmware|hardware|electrical|fpga|asic|robotic|controls|machine learning|\bml\b|edge ai|computer engineer", re.I)
EXC = re.compile(r"\bphd\b|mechanical|civil|chemical|sales|marketing", re.I)
ST = set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())
def us(locs):
    return not locs or any(re.search(r"united states|\busa?\b|remote|^nyc$|^sf$", l, re.I) or l.split(",")[-1].strip() in ST for l in locs)
def ok(p):
    t = p.get("title", "")
    deg = p.get("degrees") or []
    return (p.get("active") and p.get("is_visible", True) and "Summer 2027" in p.get("terms", [])
            and not EXC.search(t) and (p.get("category") == "Hardware" or INC.search(t))
            and us(p.get("locations", [])) and (not deg or "Bachelor's" in deg))
src = sys.argv[1] if len(sys.argv) > 1 else None
data = json.load(open(src)) if src else json.load(urllib.request.urlopen(URL, timeout=60))
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
def clean(u):  # drop Simplify tracking params, keep everything else
    s = urlsplit(u)
    q = [(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True) if not (k in ("utm_source", "ref") and v == "Simplify")]
    return urlunsplit(s._replace(query=urlencode(q)))
feed = sorted(({"id": p["id"], "c": p["company_name"], "t": p["title"], "l": "; ".join(p.get("locations", [])[:2]),
                "cat": p.get("category", ""), "u": clean(p["url"]), "d": p.get("date_posted", 0)} for p in data if ok(p)),
              key=lambda x: -x["d"])
out = {"updatedAt": int(time.time()), "postings": feed}
json.dump(out, open("feed.json", "w"), separators=(",", ":"))
print(len(feed), len(json.dumps(out)))
